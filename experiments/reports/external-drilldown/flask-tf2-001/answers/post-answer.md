Changing RequestContext.push to async would hit more than just the context class itself.

The immediate breakpoints are the places that call push or rely on the synchronous context-manager protocol:

- Flask.wsgi_app is the primary framework entrypoint that directly calls ctx.push() before dispatching the request. If push becomes async def, this path can no longer stay as a plain synchronous WSGI flow without adding a sync bridge.
- RequestContext.__enter__ currently calls self.push() synchronously. That means every with ctx, with app.request_context(...), and with app.test_request_context(...) usage becomes invalid unless Flask also adds __aenter__/__aexit__ or some wrapper.
- copy_current_request_context depends on with ctx: internally, so copied request-context wrappers would need to become async-aware too.
- stream_with_context also uses with ctx: to preserve the request context while streaming, so streaming helpers would be affected.
- FlaskClient.session_transaction uses with ctx: twice, so the testing client would need changes as well.

There is also an immediate lifecycle dependency inside push itself:

- push calls _get_session(), which calls app.session_interface.open_session(...). So custom session backends are part of the blast radius, because session opening currently happens synchronously during context activation.
- push then calls match_request(), so URL matching still assumes the context is fully installed before request dispatch starts.

Beyond those direct callers, if you want a real end-to-end async request-context activation instead of a sync shim, the request pipeline becomes async-aware too:

- Flask.full_dispatch_request
- preprocess_request and all before_request handlers
- dispatch_request / view dispatch
- finalize_request
- process_response and all after_request handlers
- teardown flow during ctx.pop()

Those functions do not call push directly, but they all assume the request context, session, and routing state are already established synchronously before they run. Once push becomes awaitable, that assumption moves.

One important nuance from this tree: RequestContext is not a separate class anymore, it is effectively merged into AppContext. So this change affects the shared request/app-context implementation, not an isolated legacy request-only class.

Tools used:

- read_file to inspect the prompt, task metadata, and the relevant Flask source around ctx.push, wsgi_app, request dispatch, session handling, and context helpers.
- grep_search to verify actual call sites of push() and with ctx usage across the Flask source and tests, instead of relying only on the projection.

What changed after drill-down:

- The clue correctly pointed to wsgi_app, session opening, and broader async-awareness, but drill-down showed the direct framework caller is Flask.wsgi_app, while several other source paths reach push indirectly through __enter__.
- Drill-down surfaced additional source-level components not obvious from the clue alone: copy_current_request_context, stream_with_context, and FlaskClient.session_transaction.
- The code inspection clarified that the real immediate dependency inside push is synchronous session_interface.open_session(...) plus request matching, which makes session backends part of the first-order impact.
- The current Flask tree merges RequestContext into AppContext, which makes the blast radius broader than a single legacy class name suggests.

Remaining uncertainty:

- The exact downstream blast radius depends on implementation strategy. If Flask keeps WSGI sync and wraps async push with ensure_sync/async_to_sync, fewer lifecycle methods need signature changes. If the goal is native async context activation, much more of the request pipeline must change.
- I verified framework source and tests in this repo clone, but not third-party extensions that may manually call ctx.push() or rely on with app.test_request_context() semantics.

Final confidence: medium