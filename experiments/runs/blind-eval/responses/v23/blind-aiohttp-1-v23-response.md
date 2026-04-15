# v2.3 Response: blind-aiohttp-1
Date: 2026-04-15

## Summary

The aiohttp request object provides distinct methods for reading JSON, URL-encoded form data, and multipart uploads. Payload size limits are enforced at the `read()` level, which raises `HTTPRequestEntityTooLarge` when exceeded. Body processing relies on a layered pipeline: raw bytes are read, then decoded/parsed according to content type.

## JSON Body Handling

- **`json()` method** (`aiohttp/web_request.py` L654-671, source snippet): Reads the body as JSON by first calling `await self.text()` to get the raw body as a string. It then optionally validates the `Content-Type` header: if `content_type` is provided (default `"application/json"`), it checks via `is_expected_content_type(self.content_type, content_type)`. If the content type does not match, it raises `HTTPBadRequest` with message `"Attempt to decode JSON with unexpected mimetype: %s"`. Finally, it calls `loads(body)` using a configurable JSON decoder (default `DEFAULT_JSON_DECODER`).
- **Key dependency**: `json()` calls `text()`, which in turn calls `read()` (FOCUS entry: `read` at `aiohttp/web_request.py:624`, `called_by: post, text, BaseRequest`). So JSON parsing ultimately goes through the same `read()` path with its payload limit enforcement.

## URL-Encoded Form Data

- **`form()` method** (`aiohttp/multipart.py:475-493`, FOCUS): Assumes body parts contain form URL-encoded data. Its behavior is described as `BRANCH(encoding -> result, else -> result)`, meaning it branches based on encoding. It calls `get_charset` and `read` to obtain the raw data, then parses it. It raises `ValueError` on malformed data.
- **`post()` method** (SYM/FOCUS references show `read` is `called_by: post, text, BaseRequest` at `aiohttp/web_request.py:624`): The `post()` method on the request object processes form submissions, using `read()` internally.
- **`multipart()` method** (`aiohttp/web_request.py:673-680`, FOCUS): Returns a `MultipartReader` — it delegates via `DELEGATE(MultipartReader -> result)` and is `called_by: post, BaseRequest`. This shows that `post()` may use `multipart()` for multipart form data.

## Multipart Upload Handling

- **`MultipartReader`** (`aiohttp/multipart.py:639-854`, FOCUS): The main class for reading multipart bodies. It calls `read_chunk`, `readline`, `_get_boundary`, `_get_part_reader`, `_maybe_release_last_part`, `_read_boundary`, `_read_headers`, and `_read_until_first_boundary`. It raises `ValueError`, `StopAsyncIteration`, `BadHttpMessage`, and `RuntimeError`. It uses `HeadersParser` from `http` and `CIMultiDict` from `multidict`.
- **`BodyPartReader`** (`aiohttp/multipart.py:257-599`, FOCUS): Reads individual body parts within a multipart message. Has `chunk_size=8192` as a default attribute. Calls `_apply_content_transfer_decoding`, `_decode_content`, `_decode_content_async`, `_decode_content_transfer`, `_needs_content_decoding`, `_read_chunk_from_length`, `_read_chunk_from_stream`, and `decode_iter`. Raises `RuntimeError`, `StopAsyncIteration`, `ValueError`. Uses `ZLibDecompressor` from `compression_utils`.
- **`read_chunk()`** (`aiohttp/multipart.py:324-366`, source snippet): Reads body part content in chunks. Handles base64-encoded transfers by reading fragments aligned to 4-byte boundaries. Tracks `_read_bytes` and sets `_at_eof` when `_read_bytes == _length`. Validates that a proper CRLF boundary follows via `await self._content.readline() != b"\r\n"`.
- **`decode_iter()`** (`aiohttp/multipart.py:524-538`, source snippet): An async generator that applies `Content-Transfer-Encoding` decoding first (`_apply_content_transfer_decoding`), then conditionally applies `Content-Encoding` decompression via `_decode_content_async` if `_needs_content_decoding()` returns true.
- **`_decode_content_transfer()`** (`aiohttp/multipart.py:565-575`, source snippet): Supports `base64` (via `base64.b64decode`), `quoted-printable` (via `binascii.a2b_qp`), and `binary`/`8bit`/`7bit` (pass-through). Raises `RuntimeError` for unknown encodings.
- **`_needs_content_decoding()`** (`aiohttp/multipart.py:505-508`, source snippet): Returns `not self._is_form_data and CONTENT_ENCODING in self.headers` — meaning content decoding (decompression) is skipped for form data parts per RFC 7578 Section 4.8.
- **`_decode_content()`** and **`_decode_content_async()`** (`aiohttp/multipart.py:540-563`, source snippets): Support `identity` (pass-through), `deflate`, and `gzip` encodings using `ZLibDecompressor`. Both enforce a `_max_decompress_size` limit via the `max_length` parameter.

## Payload Limit Enforcement

- **`read()` method** (`aiohttp/web_request.py:624-643`, FOCUS): The primary entry point for reading the request body. It raises `HTTPRequestEntityTooLarge` (from `web_exceptions`) when the body exceeds configured limits. This is the central enforcement point for payload size limits since `json()`, `text()`, and `post()` all flow through `read()` (FOCUS: `called_by: post, text, BaseRequest`).
- **`body_exists()`** (`aiohttp/web_request.py:612-614`, FOCUS): Returns `True` if the request has an HTTP body.
- **`can_read_body()`** (`aiohttp/web_request.py:607-609`, FOCUS): Returns `True` if the request body can be read.
- **Multipart decompression limit**: `_decode_content` and `_decode_content_async` both pass `max_length=self._max_decompress_size` to `ZLibDecompressor.decompress_sync` / `decompress`, providing a decompression bomb guard for multipart parts (source snippets at `aiohttp/multipart.py` L540-563).

## Client-Side Body Construction

- **`_update_body_from_data()`** (`aiohttp/client_reqrep.py:1137-1180`, source snippet): On the client side, this method processes different body types:
  - `None` → sets empty body, sets `Content-Length: 0` for non-GET methods.
  - `FormData` instances → calls `body()` to produce the payload.
  - Other types → attempts `payload.PAYLOAD_REGISTRY.get(body)`, falling back to wrapping in `FormData` if `LookupError` is raised.
  - After setting the body, it sets `Content-Length` if the size is known, or enables chunked encoding otherwise. It then copies payload headers (e.g., `Content-Type`) to the request headers.
- **`update_body()`** (`aiohttp/client_reqrep.py:1199-1259`, source snippet): An async method that safely updates the body by first calling `await self._body.close()` on any existing payload to prevent resource leaks, then delegates to `_update_body()`. The docstring explicitly warns against setting `request.body` directly.

## Uncertainty / Limits

- The exact configuration mechanism for setting `client_max_size` (the payload size limit checked in `read()`) is not shown in the clue file or source snippets. The `AppRunner._make_request` snippet (from blind-aiohttp-2) references `client_max_size=self.app._client_max_size`, suggesting it is configured on the `Application` object, but the detailed API for setting it is not visible here.
- The `_max_decompress_size` field on `BodyPartReader` is referenced but its default value and configuration path are not shown.
- The exact behavior of `post()` for distinguishing URL-encoded vs. multipart form submissions (presumably based on `Content-Type`) is not fully visible — only that it calls both `read()` and `multipart()`.
