"""Minimal HTTP client (stdlib only) with retries and GitHub-style rate-limit handling."""
from __future__ import annotations

import gzip
import http.client
import json
import socket
import time
import urllib.error
import urllib.request
from urllib.parse import urlencode


class HttpError(Exception):
    def __init__(self, message: str, code: int | None = None):
        super().__init__(message)
        self.code = code


class HttpClient:
    def __init__(self, user_agent: str, timeout: float = 30, retries: int = 3,
                 backoff: float = 2.0, max_wait: float = 90):
        self.user_agent = user_agent
        self.timeout = timeout
        self.retries = retries
        self.backoff = backoff
        self.max_wait = max_wait
        self.request_count = 0

    def get(self, url: str, params: dict | None = None, headers: dict | None = None) -> bytes:
        if params:
            url = url + ("&" if "?" in url else "?") + urlencode(params)
        hdrs = {"User-Agent": self.user_agent}
        hdrs.update(headers or {})
        for attempt in range(self.retries + 1):
            self.request_count += 1
            req = urllib.request.Request(url, headers=hdrs)
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    body = resp.read()
                # Some servers send gzip bodies without a Content-Encoding header.
                return gzip.decompress(body) if body[:2] == b"\x1f\x8b" else body
            except urllib.error.HTTPError as e:
                wait = self._retry_wait(e, attempt)
                if wait is not None and attempt < self.retries:
                    time.sleep(wait)
                    continue
                raise HttpError(f"HTTP {e.code} for {url}", e.code) from e
            except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError,
                    http.client.HTTPException) as e:
                if attempt < self.retries:
                    time.sleep(self.backoff * (2 ** attempt))
                    continue
                raise HttpError(f"{type(e).__name__}: {e} for {url}") from e
        raise HttpError(f"giving up on {url}")

    def get_json(self, url: str, params: dict | None = None, headers: dict | None = None):
        return json.loads(self.get(url, params=params, headers=headers).decode("utf-8"))

    def _retry_wait(self, e: urllib.error.HTTPError, attempt: int) -> float | None:
        h = e.headers or {}
        retry_after = h.get("Retry-After")
        if retry_after and str(retry_after).isdigit():
            return min(float(retry_after), self.max_wait)
        if h.get("X-RateLimit-Remaining") == "0" and h.get("X-RateLimit-Reset"):
            try:
                return min(max(float(h["X-RateLimit-Reset"]) - time.time(), 1) + 1, self.max_wait)
            except ValueError:
                pass
        if e.code == 429 or e.code >= 500:
            return self.backoff * (2 ** attempt)
        return None
