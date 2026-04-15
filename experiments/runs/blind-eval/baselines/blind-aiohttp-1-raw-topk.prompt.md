# Baseline Evaluation: Raw Source Files
# Task: blind-aiohttp-1

You are a senior software engineer. You have been given raw source code
excerpts from a repository. Answer the question using ONLY the source
code below. Do not use any external knowledge about the framework.

--- SOURCE CODE ---
## aiohttp\formdata.py (score: 3.0)
```
import io
from collections import deque
from collections.abc import Iterable
from typing import Any
from urllib.parse import urlencode

from multidict import MultiDict, MultiDictProxy

from . import hdrs, multipart, payload
from .helpers import guess_filename
from .payload import Payload

__all__ = ("FormData",)


class FormData:
    """Helper class for form body generation.

    Supports multipart/form-data and application/x-www-form-urlencoded.
    """

    def __init__(
        self,
        fields: Iterable[Any] = (),
        quote_fields: bool = True,
        charset: str | None = None,
        boundary: str | None = None,
        *,
        default_to_multipart: bool = False,
    ) -> None:
        self._boundary = boundary
        self._writer = multipart.MultipartWriter("form-data", boundary=self._boundary)
        self._fields: list[Any] = []
        self._is_multipart = default_to_multipart
        self._quote_fields = quote_fields
        self._charset = charset

        if isinstance(fields, dict):
            fields = list(fields.items())
        elif not isinstance(fields, (list, tuple)):
            fields = (fields,)
        self.add_fields(*fields)

    @property
    def is_multipart(self) -> bool:
        return self._is_multipart

    def add_field(
        self,
        name: str,
        value: Any,
        *,
        content_type: str | None = None,
        filename: str | None = None,
    ) -> None:
        if isinstance(value, (io.IOBase, bytes, bytearray, memoryview)):
            self._is_multipart = True

        type_options: MultiDict[str] = MultiDict({"name": name})
        if filename is not None and not isinstance(filename, str):
            raise TypeError("filename must be an instance of str. Got: %s" % filename)
        if filename is None and isinstance(value, io.IOBase):
            filename = guess_filename(value, name)
        if filename is not None:
            type_options["filename"] = filename
            self._is_multipart = True

        headers = {}
        if content_type is not None:
            if not isinstance(content_type, str):
                raise TypeError(
                    "content_type must be an instance of str. Got: %s" % content_type
                )
            if "\r" in content_type or "\n" in content_type:
                raise ValueError(
                    "Newline or carriage return detected in headers. "
                    "Potential header injection attack."
                )
            headers[hdrs.CONTENT_TYPE] = content_type
            self._is_multipart = True

        self._fields.append((type_options, headers, value))

    def add_fields(self, *fields: Any) -> None:
        to_add: deque[Any] = deque(fields)

        while to_add:
            rec = to_add.popleft()

            if isinstance(rec, io.IOBase):
                k = guess_filename(rec, "unknown")
                self.add_field(k, rec)  # type: ignore[arg-type]

            elif isinstance(rec, (MultiDictProxy, MultiDict)):
                to_add.extend(rec.items())

            elif isinstance(rec, (list, tuple)) and len(rec) == 2:
                k, fp = rec
                self.add_field(k, fp)

            else:
                raise TypeError(
                    "Only io.IOBase, multidict and (name, file) "
                    "pairs allowed, use .add_field() for passing "
                    f"more complex parameters, got {rec!r}"
                )

    def _gen_form_urlencoded(self) -> payload.BytesPayload:
        # form data (x-www-form-urlencoded)
        data = []
        for type_options, _, value in self._fields:
            if not isinstance(value, str):
                raise TypeError(f"expected str, got {value!r}")
            data.append((type_options["name"], value))

        charset = self._charset if self._charset is not None else "utf-8"

        if charset == "utf-8":
            content_type = "application/x-www-form-urlencoded"
        else:
            content_type = "application/x-www-form-urlencoded; charset=%s" % charset

        return payload.BytesPayload(
            urlencode(data, doseq=True, encoding=charset).encode(),
            content_type=content_type,
        )

    def _gen_form_data(self) -> multipart.MultipartWriter:
        """Encode a list of fields using the multipart/form-data MIME format"""
        for dispparams, headers, value in self._fields:
            try:
                if hdrs.CONTENT_TYPE in headers:
                    part = payload.get_payload(
                        value,
                        content_type=headers[hdrs.CONTENT_TYPE],
                        headers=headers,
                        encoding=self._charset,
                    )
                else:
                    part = payload.get_payload(
                        value, headers=headers, encoding=self._charset
                    )
            except Exception as exc:
                raise TypeError(
                    "Can not serialize value type: %r\n "
                    "headers: %r\n value: %r" % (type(value), headers, value)
                ) from exc

            if dispparams:
                part.set_content_disposition(
                    "form-data", quote_fields=self._quote_fields, **dispparams
                )
                # FIXME cgi.FieldStorage doesn't likes body parts with
                # Content-Length which were sent via chunked transfer encoding
                assert part.headers is not None
                part.headers.popall(hdrs.CONTENT_LENGTH, None)

            self._writer.append_payload(part)

        self._fields.clear()
        return self._writer

    def __call__(self) -> Payload:
        if self._is_multipart:
            return self._gen_form_data()
        else:
            return self._gen_form_urlencoded()

```

## aiohttp\multipart.py (score: 3.0)
```
import base64
import binascii
import json
import re
import sys
import uuid
import warnings
from collections import deque
from collections.abc import AsyncIterator, Iterator, Mapping, Sequence
from types import TracebackType
from typing import TYPE_CHECKING, Any, Union, cast
from urllib.parse import parse_qsl, unquote, urlencode

from multidict import CIMultiDict, CIMultiDictProxy

from .abc import AbstractStreamWriter
from .compression_utils import (
    DEFAULT_MAX_DECOMPRESS_SIZE,
    ZLibCompressor,
    ZLibDecompressor,
)
from .hdrs import (
    CONTENT_DISPOSITION,
    CONTENT_ENCODING,
    CONTENT_LENGTH,
    CONTENT_TRANSFER_ENCODING,
    CONTENT_TYPE,
)
from .helpers import CHAR, TOKEN, parse_mimetype, reify
from .http import HeadersParser
from .http_exceptions import BadHttpMessage
from .log import internal_logger
from .payload import (
    JsonPayload,
    LookupError,
    Order,
    Payload,
    StringPayload,
    get_payload,
    payload_type,
)
from .streams import StreamReader

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing import TypeVar

    Self = TypeVar("Self", bound="BodyPartReader")

__all__ = (
    "MultipartReader",
    "MultipartWriter",
    "BodyPartReader",
    "BadContentDispositionHeader",
    "BadContentDispositionParam",
    "parse_content_disposition",
    "content_disposition_filename",
)


if TYPE_CHECKING:
    from .client_reqrep import ClientResponse


class BadContentDispositionHeader(RuntimeWarning):
    pass


class BadContentDispositionParam(RuntimeWarning):
    pass


def parse_content_disposition(
    header: str | None,
) -> tuple[str | None, dict[str, str]]:
    def is_token(string: str) -> bool:
        return bool(string) and TOKEN >= set(string)

    def is_quoted(string: str) -> bool:
        return string[0] == string[-1] == '"'

    def is_rfc5987(string: str) -> bool:
        return is_token(string) and string.count("'") == 2

    def is_extended_param(string: str) -> bool:
        return string.endswith("*")

    def is_continuous_param(string: str) -> bool:
        pos = string.find("*") + 1
        if not pos:
            return False
        substring = string[pos:-1] if string.endswith("*") else string[pos:]
        return substring.isdigit()

    def unescape(text: str, *, chars: str = "".join(map(re.escape, CHAR))) -> str:
        return re.sub(f"\\\\([{chars}])", "\\1", text)

    if not header:
        return None, {}

    disptype, *parts = header.split(";")
    if not is_token(disptype):
        warnings.warn(BadContentDispositionHeader(header))
        return None, {}

    params: dict[str, str] = {}
    while parts:
        item = parts.pop(0)

        if not item:  # To handle trailing semicolons
            warnings.warn(BadContentDispositionHeader(header))
            continue

        if "=" not in item:
            warnings.warn(BadContentDispositionHeader(header))
            return None, {}

        key, value = item.split("=", 1)
        key = key.lower().strip()
        value = value.lstrip()

        if key in params:
            warnings.warn(BadContentDispositionHeader(header))
            return None, {}

        if not is_token(key):
            warnings.warn(BadContentDispositionParam(item))
            continue

        elif is_continuous_param(key):
            if is_quoted(value):
                value = unescape(value[1:-1])
            elif not is_token(value):
                warnings.warn(BadContentDispositionParam(item))
                continue

        elif is_extended_param(key):
            if is_rfc5987(value):
                encoding, _, value = value.split("'", 2)
                encoding = encoding or "utf-8"
            else:
                warnings.warn(BadContentDispositionParam(item))
                continue

            try:
                value = unquote(value, encoding, "strict")
            except UnicodeDecodeError:  # pragma: nocover
                warnings.warn(BadContentDispositionParam(item))
                continue

        else:
            failed = True
            if is_quoted(value):
                failed = False
                value = unescape(value[1:-1].lstrip("\\/"))
            elif is_token(value):
                failed = False
            elif parts:
                # maybe just ; in filename, in any case this is just
                # one case fix, for proper fix we need to redesign parser
                _value = f"{value};{parts[0]}"
                if is_quoted(_value):
                    parts.pop(0)
                    value = unescape(_value[1:-1].lstrip("\\/"))
                    failed = False

            if failed:
                warnings.warn(BadContentDispositionHeader(header))
                return None, {}

        params[key] = value

    return disptype.lower(), params


def content_disposition_filename(
    params: Mapping[str, str], name: str = "filename"
) -> str | None:
    name_suf = "%s*" % name
    if not params:
        return None
    elif name_suf in params:
        return params[name_suf]
    elif name in params:
        return params[name]
    else:
        parts = []
        fnparams = sorted(
            (key, value) for key, value in params.items() if key.startswith(name_suf)
        )
        for num, (key, value) in enumerate(fnparams):
            _, tail = key.split("*", 1)
            if tail.endswith("*"):
                tail = tail[:-1]
            if tail == str(num):
                parts.append(value)
            else:
                break
        if not parts:
            return None
        value = "".join(parts)
        if "'" in value:
            encoding, _, value = value.split("'", 2)
            encoding = encoding or "utf-8"
            return unquote(value, encoding, "strict")
        return value


class MultipartResponseWrapper:
    """Wrapper around the MultipartReader.

    It takes care about
    underlying connection and close it when it needs in.
    """

    def __init__(
        self,
        resp: "ClientResponse",
        stream: "MultipartReader",
    ) -> None:
        self.resp = resp
        self.stream = stream

    def __aiter__(self) -> "MultipartResponseWrapper":
        return self

    async def __anext__(
        self,
    ) -> Union["MultipartReader", "BodyPartReader"]:
        part = await self.next()
        if part is None:
            raise StopAsyncIteration
        return part

    def at_eof(self) -> bool:
        """Returns True when all response data had been read."""
        return self.resp.content.at_eof()

    async def next(
        self,
    ) -> Union["MultipartReader", "BodyPartReader"] | None:
        """Emits next multipart reader object."""
        item = await self.stream.next()
        if self.stream.at_eof():
            await self.release()
        return item

    async def release(self) -> None:
        """Release the connection gracefully.

        All remaining content is read to the void.
        """
        self.resp.release()


class BodyPartReader:
    """Multipart reader for single body part."""

    chunk_size = 8192

    def __init__(
        self,
        boundary: bytes,
        headers: "CIMultiDictProxy[str]",
        content: StreamReader,
        *,
        subtype: str = "mixed",
        default_charset: str | None = None,
        max_decompress_size: int = DEFAULT_MAX_DECOMPRESS_SIZE,
    ) -> None:
        self.headers = headers
        self._boundary = boundary
        self._boundary_len = len(boundary) + 2  # Boundary + \r\n
        self._content = content
        self._default_charset = default_charset
        self._at_eof = False
        self._is_form_data = subtype == "form-data"
        # https://datatracker.ietf.org/doc/html/rfc7578#section-4.8
        length = None if self._is_form_data else self.headers.get(CONTENT_LENGTH, None)
        self._length = int(length) if length is not None else None
        self._read_bytes = 0
        self._unread: deque[bytes] = deque()
        self._prev_chunk: bytes | None = None
        self._content_eof = 0
        self._cache: dict[str, Any] = {}
        self._max_decompress_size = max_decompress_size

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> bytes:
        part = await self.next()
        if part is None:
            raise StopAsyncIteration
        return part

    async def next(self) -> bytes | None:
        item = await self.read()
        if not item:
            return None
        return item

    async def read(self, *, decode: bool = False) -> bytes:
        """Reads body part data.

        decode: Decodes data following by encoding
                method from Content-Encoding header. If it missed
                data remains untouched
        """
        if self._at_eof:
            return b""
        data = bytearray()
        while not self._at_eof:
            data.extend(await self.read_chunk(self.chunk_size))
        # https://github.com/python/mypy/issues/17537
        if decode:  # type: ignore[unreachable]
            decoded_data = bytearray()
            async for d in self.decode_iter(data):
                decoded_data.extend(d)
            return decoded_data
        return data

    async def read_chunk(self, size: int = chunk_size) -> bytes:
        """Reads body part content chunk of the specified size.

        size: chunk size
        """
        if self._at_eof:
            return b""
        if self._length:
            chunk = await self._read_chunk_from_length(size)
        else:
            chunk = await self._read_chunk_from_stream(size)

        # For the case of base64 data, we must read a fragment of size with a
        # remainder of 0 by dividing by 4 for string without symbols \n or \r
        encoding = self.headers.get(CONTENT_TRANSFER_ENCODING)
        if encoding and encoding.lower() == "base64":
            stripped_chunk = b"".join(chunk.split())
            remainder = len(stripped_chunk) % 4

            while remainder != 0 and not self.at_eof():
                over_chunk_size = 4 - remainder
                over_chunk = b""

                if self._prev_chunk:
                    over_chunk = self._prev_chunk[:over_chunk_size]
                    self._prev_chunk = self._prev_chunk[len(over_chunk) :]

                if len(over_chunk) != over_chunk_size:
                    over_chunk += await self._content.read(4 - len(over_chunk))

                if not over_chunk:
                    self._at_eof = True

                stripped_chunk += b"".join(over_chunk.split())
                chunk += over_chunk
                remainder = len(stripped_chunk) % 4

        self._read_bytes += len(chunk)
        if self._read_bytes == self._length:
            self._at_eof = True
        if self._at_eof and await self._content.readline() != b"\r\n":
            raise ValueError("Reader did not read all the data or it is malformed")
        return chunk

    async def _read_chunk_from_length(self, size: int) -> bytes:
        # Reads body part content chunk of the specified size.
        # The body part must has Content-Length header with proper value.
        assert self._length is not None, "Content-Length required for chunked read"
        chunk_size = min(size, self._length - self._read_bytes)
        chunk = await self._content.read(chunk_size)
        if self._content.at_eof():
            self._at_eof = True
        return chunk

    async def _read_chunk_from_stream(self, size: int) -> bytes:
        # Reads content chunk of body part with unknown length.
        # The Content-Length header for body part is not necessary.
        assert (
            size >= self._boundary_len
        ), "Chunk size must be greater or equal than boundary length + 2"
        first_chunk = self._prev_chunk is None
        if first_chunk:
            # We need to re-add the CRLF that got removed from headers parsing.
            self._prev_chunk = b"\r\n" + await self._content.read(size)

        chunk = b""
        # content.read() may return less than size, so we need to loop to ensure
        # we have enough data to detect the boundary.
        while len(chunk) < self._boundary_len:
            chunk += await self._content.read(size)
            self._content_eof += int(self._content.at_eof())
            if self._content_eof > 2:
                raise ValueError("Reading after EOF")
            if self._content_eof:
                break
        if len(chunk) > size:
            self._content.unread_data(chunk[size:])
            chunk = chunk[:size]

        assert self._prev_chunk is not None
        window = self._prev_chunk + chunk
        sub = b"\r\n" + self._boundary
        if first_chunk:
            idx = window.find(sub)
        else:
            idx = window.find(sub, max(0, len(self._prev_chunk) - len(sub)))
        if idx >= 0:
            # pushing boundary back to content
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                self._content.unread_data(window[idx:])
            self._prev_chunk = self._prev_chunk[:idx]
            chunk = window[len(self._prev_chunk) : idx]
            if not chunk:
                self._at_eof = True
        result = self._prev_chunk[2 if first_chunk else 0 :]  # Strip initial CRLF
        self._prev_chunk = chunk
        return result

    async def readline(self) -> bytes:
        """Reads body part by line by line."""
        if self._at_eof:
            return b""

        if self._unread:
            line = self._unread.popleft()
        else:
            line = await self._content.readline()

        if line.startswith(self._boundary):
            # the very last boundary may not come with \r\n,
            # so set single rules for everyone
            sline = line.rstrip(b"\r\n")
            boundary = self._boundary
            last_boundary = self._boundary + b"--"
            # ensure that we read exactly the boundary, not something alike
            if sline == boundary or sline == last_boundary:
                self._at_eof = True
                self._unread.append(line)
                return b""
        else:
            next_line = await self._content.readline()
            if next_line.startswith(self._boundary):
                line = line[:-2]  # strip CRLF but only once
            self._unread.append(next_line)

        return line

    async def release(self) -> None:
        """Like read(), but reads all the data to the void."""
        if self._at_eof:
            return
        while not self._at_eof:
            await self.read_chunk(self.chunk_size)

    async def text(self, *, encoding: str | None = None) -> str:
        """Like read(), but assumes that body part contains text data."""
        data = await self.read(decode=True)
        # see https://www.w3.org/TR/html5/forms.html#multipart/form-data-encoding-algorithm
        # and https://dvcs.w3.org/hg/xhr/raw-file/tip/Overview.html#dom-xmlhttprequest-send
        encoding = encoding or self.get_charset(default="utf-8")
        return data.decode(encoding)

    async def json(self, *, encoding: str | None = None) -> dict[str, Any] | None:
        """Like read(), but assumes that body parts contains JSON data."""
        data = await self.read(decode=True)
        if not data:
            return None
        encoding = encoding or self.get_charset(default="utf-8")
        return cast(dict[str, Any], json.loads(data.decode(encoding)))

    async def form(self, *, encoding: str | None = None) -> list[tuple[str, str]]:
        """Like read(), but assumes that body parts contain form urlencoded data."""
        data = await self.read(decode=True)
        if not data:
            return []
        if encoding is not None:
            real_encoding = encoding
        else:
            real_encoding = self.get_charset(default="utf-8")
        try:
            decoded_data = data.rstrip().decode(real_encoding)
        except UnicodeDecodeError:
            raise ValueError("data cannot be decoded with %s encoding" % real_encoding)

        return parse_qsl(
            decoded_data,
            keep_blank_values=True,
            encoding=real_encoding,
        )

    def at_eof(self) -> bool:
        """Returns True if the boundary was reached or False otherwise."""
        return self._at_eof

    def _apply_content_transfer_decoding(self, data: bytes) -> bytes:
        """Apply Content-Transfer-Encoding decoding if header is present."""
        if CONTENT_TRANSFER_ENCODING in self.headers:
            return self._decode_content_transfer(data)
        return data

    def _needs_content_decoding(self) -> bool:
        """Check if Content-Encoding decoding should be applied."""
        # https://datatracker.ietf.org/doc/html/rfc7578#section-4.8
        return not self._is_form_data and CONTENT_ENCODING in self.headers

    def decode(self, data: bytes) -> bytes:
        """Decodes data synchronously.

        Decodes data according the specified Content-Encoding
        or Content-Transfer-Encoding headers value.

        Note: For large payloads, consider using decode_iter() instead
        to avoid blocking the event loop during decompression.
        """
        data = self._apply_content_transfer_decoding(data)
        if self._needs_content_decoding():
            return self._decode_content(data)
        return data

    async def decode_iter(self, data: bytes) -> AsyncIterator[bytes]:
        """Async generator that yields decoded data chunks.

        Decodes data according the specified Content-Encoding
        or Content-Transfer-Encoding headers value.

        This method offloads decompression to an executor for large payloads
        to avoid blocking the event loop.
        """
        data = self._apply_content_transfer_decoding(data)
        if self._needs_content_decoding():
            async for d in self._decode_content_async(data):
                yield d
        else:
            yield data

    def _decode_content(self, data: bytes) -> bytes:
        encoding = self.headers.get(CONTENT_ENCODING, "").lower()
        if encoding == "identity":
            return data
        if encoding in {"deflate", "gzip"}:
            return ZLibDecompressor(
                encoding=encoding,
                suppress_deflate_header=True,
            ).decompress_sync(data, max_length=self._max_decompress_size)

        raise RuntimeError(f"unknown content encoding: {encoding}")

    async def _decode_content_async(self, data: bytes) -> AsyncIterator[bytes]:
        encoding = self.headers.get(CONTENT_ENCODING, "").lower()
        if encoding == "identity":
            yield data
        elif encoding in {"deflate", "gzip"}:
            d = ZLibDecompressor(
                encoding=encoding,
                suppress_deflate_header=True,
            )
            yield await d.decompress(data, max_length=self._max_decompress_size)
        else:
            raise RuntimeError(f"unknown content encoding: {encoding}")

    def _decode_content_transfer(self, data: bytes) -> bytes:
        encoding = self.headers.get(CONTENT_TRANSFER_ENCODING, "").lower()

        if encoding == "base64":
            return base64.b64decode(data)
        elif encoding == "quoted-printable":
            return binascii.a2b_qp(data)
        elif encoding in ("binary", "8bit", "7bit"):
            return data
        else:
            raise RuntimeError(f"unknown content transfer encoding: {encoding}")

    def get_charset(self, default: str) -> str:
        """Returns charset parameter from Content-Type header or default."""
        ctype = self.headers.get(CONTENT_TYPE, "")
        mimetype = parse_mimetype(ctype)
        return mimetype.parameters.get("charset", self._default_charset or default)

    @reify
    def name(self) -> str | None:
        """Returns name specified in Content-Disposition header.

        If the header is missing or malformed, returns None.
        """
        _, params = parse_content_disposition(self.headers.get(CONTENT_DISPOSITION))
        return content_disposition_filename(params, "name")

    @reify
    def filename(self) -> str | None:
        """Returns filename specified in Content-Disposition header.

        Returns None if the header is missing or malformed.
        """
        _, params = parse_content_disposition(self.headers.get(CONTENT_DISPOSITION))
        return content_disposition_filename(params, "filename")


@payload_type(BodyPartReader, order=Order.try_first)
class BodyPartReaderPayload(Payload):
    _value: BodyPartReader
    # _autoclose = False (inherited) - Streaming reader that may have resources

    def __init__(self, value: BodyPartReader, *args: Any, **kwargs: Any) -> None:
        super().__init__(value, *args, **kwargs)

        params: dict[str, str] = {}
        if value.name is not None:
            params["name"] = value.name
        if value.filename is not None:
            params["filename"] = value.filename

        if params:
            self.set_content_disposition("attachment", True, **params)

    def decode(self, encoding: str = "utf-8", errors: str = "strict") -> str:
        raise TypeError("Unable to decode.")

    async def as_bytes(self, encoding: str = "utf-8", errors: str = "strict") -> bytes:
        """Raises TypeError as body parts should be consumed via write().

        This is intentional: BodyPartReader payloads are designed for streaming
        large data (potentially gigabytes) and must be consumed only once via
        the write() method to avoid memory exhaustion. They cannot be buffered
        in memory for reuse.
        """
        raise TypeError("Unable to read body part as bytes. Use write() to consume.")

    async def write(self, writer: AbstractStreamWriter) -> None:
        field = self._value
        while chunk := await field.read_chunk(size=2**18):
            async for d in field.decode_iter(chunk):
                await writer.write(d)


class MultipartReader:
    """Multipart body reader."""

    #: Response wrapper, used when multipart readers constructs from response.
    response_wrapper_cls = MultipartResponseWrapper
    #: Multipart reader class, used to handle multipart/* body parts.
    #: None points to type(self)
    multipart_reader_cls: type["MultipartReader"] | None = None
    #: Body part reader class for non multipart/* content types.
    part_reader_cls = BodyPartReader

    def __init__(
        self,
        headers: Mapping[str, str],
        content: StreamReader,
        *,
... (truncated)
```
--- END SOURCE CODE ---

QUESTION: If a handler reads incoming data from different body formats, what does the request object actually do for JSON, URL-encoded forms, and multipart uploads, and where are payload limits enforced?

Provide a detailed answer citing specific functions/files from the source.
