# Baseline Evaluation: Plain Summary
# Task: blind-aiohttp-1

You are a senior software engineer. You have been given a brief summary
of a repository's structure. Answer the question using ONLY this summary.
Do not use any external knowledge about the framework.

--- REPOSITORY SUMMARY ---
Repository: aiohttp

Directory structure:
  aiohttp/ (63 files)
  CHANGES/ (125 files)
  CHANGES.rst
  CODE_OF_CONDUCT.md
  CONTRIBUTING.rst
  CONTRIBUTORS.txt
  docs/ (54 files)
  examples/ (27 files)
  LICENSE.txt
  Makefile
  MANIFEST.in
  pyproject.toml
  README.rst
  requirements/ (27 files)
  setup.cfg
  setup.py
  tests/ (90 files)
  tools/ (9 files)
  vendor/ (1 files)

Source files (89 python files):
  aiohttp\__init__.py (6KB)
  aiohttp\_cookie_helpers.py (13KB)
  aiohttp\_websocket\__init__.py (0KB)
  aiohttp\_websocket\helpers.py (4KB)
  aiohttp\_websocket\models.py (3KB)
  aiohttp\_websocket\reader.py (0KB)
  aiohttp\_websocket\reader_c.py (18KB)
  aiohttp\_websocket\reader_py.py (18KB)
  aiohttp\_websocket\writer.py (10KB)
  aiohttp\abc.py (7KB)
  aiohttp\base_protocol.py (2KB)
  aiohttp\client.py (56KB)
  aiohttp\client_exceptions.py (10KB)
  aiohttp\client_middleware_digest_auth.py (17KB)
  aiohttp\client_middlewares.py (1KB)
  aiohttp\client_proto.py (12KB)
  aiohttp\client_reqrep.py (48KB)
  aiohttp\client_ws.py (19KB)
  aiohttp\compression_utils.py (12KB)
  aiohttp\connector.py (62KB)
  aiohttp\cookiejar.py (21KB)
  aiohttp\formdata.py (5KB)
  aiohttp\hdrs.py (4KB)
  aiohttp\helpers.py (33KB)
  aiohttp\http.py (1KB)
  aiohttp\http_exceptions.py (2KB)
  aiohttp\http_parser.py (38KB)
  aiohttp\http_websocket.py (1KB)
  aiohttp\http_writer.py (12KB)
  aiohttp\log.py (0KB)
  ... and 59 more files
--- END SUMMARY ---

QUESTION: If a handler reads incoming data from different body formats, what does the request object actually do for JSON, URL-encoded forms, and multipart uploads, and where are payload limits enforced?

Provide a detailed answer based solely on the summary above.
If the summary doesn't contain enough information, say what you CAN and CANNOT determine.
