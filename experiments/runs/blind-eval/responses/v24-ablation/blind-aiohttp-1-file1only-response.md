# v2.4 Ablation (File 1 Only): blind-aiohttp-1
Date: 2026-04-16

JSON goes through the request’s text path: `web_request.json` returns the body as JSON, calls `text`, and can raise `HTTPBadRequest` if JSON handling fails. [json (aiohttp/web_request.py:654-671)]

The only explicit payload-limit enforcement shown in the clue is in `web_request.read`, which is called by `text` and `post` and can raise `HTTPRequestEntityTooLarge`. That means the visible size guard sits at raw request-body read time, before higher-level consumers built on `read`. [read (aiohttp/web_request.py:624-643)]

For multipart uploads, `web_request.multipart` does not eagerly materialize the body; it delegates to `MultipartReader` and returns an async iterator. The clue also shows `multipart()` is called by `post`. [multipart (aiohttp/web_request.py:673-680)]

Inside multipart handling, a body part’s `read()` accumulates bytes by looping over `read_chunk` / `decode_iter`. Text parts call `get_charset` plus `read`; JSON parts do the same; form-url-encoded body parts choose an explicit encoding or a charset, then call `read`, and may raise `ValueError`. [read (aiohttp/multipart.py:304-322); text (aiohttp/multipart.py:459-465); json (aiohttp/multipart.py:467-473); form (aiohttp/multipart.py:475-493)]

What I cannot determine from this clue file: the exact top-level `request.post()` branching logic for non-multipart URL-encoded forms, and whether any additional multipart-specific size checks exist beyond the explicit `HTTPRequestEntityTooLarge` raised by `web_request.read`. [GAPS; multipart (aiohttp/web_request.py:673-680); read (aiohttp/web_request.py:624-643)]
