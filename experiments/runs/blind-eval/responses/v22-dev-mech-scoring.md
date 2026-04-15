# v2.2 Blind Mechanistic Scoring

### blind-aiohttp-1 (1/4)
F1: MISS — Response mentions read() raises HTTPRequestEntityTooLarge but never describes the readany-based incremental consumption or byte accumulation mechanism.
F2: COVERED — Explicitly states "request.json() first awaits self.text(), rejects an unexpected mimetype by raising HTTPBadRequest when self.content_type does not match."
F3: MISS — No mention of BaseRequest.post returning empty MultiDict for non-POST-like methods or unsupported content types.
F4: MISS — Discusses multipart via MultipartReader/BodyPartReader but never mentions TemporaryFile or executor usage for file parts in BaseRequest.post.

### blind-aiohttp-2 (1/4)
F1: MISS — Describes CleanupContext bookkeeping and AppRunner hooks but never explicitly states that Application.startup/shutdown only send signals while CleanupContext handles actual resource enter/exit.
F2: COVERED — Explicitly states "Application.cleanup() also has a fallback path: the clue says it branches on whether on_cleanup is frozen, calling _on_cleanup directly otherwise."
F3: MISS — No mention of CleanupContext._on_startup accepting async context managers or async-generator callbacks, or wrapping generators.
F4: MISS — Covers reverse unwinding and CleanupError for multiple failures, but omits the key distinction that a single failure is re-raised directly (not wrapped in CleanupError).

### blind-click-1 (2/4)
F1: COVERED — States command() "Creates a new Command and uses the decorated function as the callback" with "UNWIND(reversed)" for stacked decorator metadata, and describes _param_memo collecting params.
F2: MISS — Describes Group as nesting commands but never states that decorators.group is a variant of decorators.command that defaults cls to Group.
F3: COVERED — States "Subcommands are attached through add_command(). That method Registers another Command with this group."
F4: MISS — Explicitly acknowledges "The evidence supplied does not show the exact invoke / resolve_command body." No mention of _protected_args, first-token retention, or resolve_command mapping.

### blind-click-2 (1/4)
F1: MISS — Mentions consume_value, envvar, and defaults, but explicitly states "The exact precedence among prompt/env/default is not exposed in the supplied snippets." Does not identify CLI parse or default_map as sources.
F2: MISS — Mentions type_cast_value does "conversion and validation" but never describes the single-value, fixed-nargs tuple, or variadic-nargs distinctions.
F3: MISS — No mention of Choice.convert, normalize_choice, token normalization, or case-fold.
F4: COVERED — Describes File with lazy=True returning LazyFile for deferred opening, and Path calling coerce_path_result for path-specific validation/coercion.

### blind-fiber-1 (0/4)
F1: MISS — Mentions DefaultCtx.Path can override the request path but does not describe mutating the underlying fasthttp request URI or recording the original override.
F2: MISS — No mention of RestartRouting, indexRoute reset to -1, or invoking app.next.
F3: MISS — No mention of App.next, treeStack, method/path hash scanning, skipping mounted routes, or Route.match.
F4: MISS — Infers 405-vs-404 distinction from method-specific registration but explicitly hedges ("materials do not expose the exact branch body that emits 405") and does not mention the Allow header being appended.

### blind-fiber-2 (2/4)
F1: MISS — No description of the recover middleware structure (wrapping c.Next in defer/recover) or optional stack trace emission.
F2: COVERED — States "if the recovered panic value r is already an error it returns that directly; otherwise it creates a new error using %v." Matches preserving error as-is and wrapping non-error.
F3: MISS — Mentions DefaultErrorHandler exists as a fallback but does not state that the Fiber constructor installs it when Config.ErrorHandler is nil.
F4: COVERED — Describes App.ErrorHandler with "loop/precedence behavior" finding "the appropriate handler for the given request," and explains mounted sub-apps are recursively integrated so the mounted app's error handler can run for requests under its mount path.

## Summary

| Task | Covered | Total | Score |
|------|---------|-------|-------|
| blind-aiohttp-1 | 1 | 4 | 25% |
| blind-aiohttp-2 | 1 | 4 | 25% |
| blind-click-1 | 2 | 4 | 50% |
| blind-click-2 | 1 | 4 | 25% |
| blind-fiber-1 | 0 | 4 | 0% |
| blind-fiber-2 | 2 | 4 | 50% |
| **Overall** | **7** | **24** | **29%** |
