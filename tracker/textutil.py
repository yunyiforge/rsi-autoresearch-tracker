"""Text normalisation, keyword matching and URL helpers."""
from __future__ import annotations

import hashlib
import html
import re
import unicodedata
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

_WS = re.compile(r"\s+")
_SEP = re.compile(r"[-_/\u2010-\u2015]")
_TAG = re.compile(r"<[^>]+>")


def normalize_text(text: str | None) -> str:
    """Lowercase, strip accents, treat - _ / as spaces, collapse whitespace."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = _SEP.sub(" ", text.lower())
    return _WS.sub(" ", text).strip()


def clean_ws(text: str | None) -> str:
    return _WS.sub(" ", text or "").strip()


def strip_html(text: str | None) -> str:
    return clean_ws(html.unescape(_TAG.sub(" ", text or "")))


def truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", normalize_text(text)).strip("-") or "item"


def short_hash(text: str, n: int = 12) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]


class KeywordMatcher:
    """Matches config keywords against normalised text.

    "foo bar"  -> whole-phrase match, "foo*" -> prefix match, "re:..." -> raw regex.
    """

    def __init__(self, keywords: Iterable[str] | None):
        self.patterns: list[tuple[str, re.Pattern]] = []
        for kw in keywords or []:
            kw = str(kw)
            if kw.startswith("re:"):
                self.patterns.append((kw, re.compile(kw[3:])))
                continue
            prefix = kw.endswith("*")
            core = normalize_text(kw.rstrip("*"))
            if not core:
                continue
            pat = r"(?<![a-z0-9])" + re.escape(core) + ("" if prefix else r"(?![a-z0-9])")
            self.patterns.append((kw, re.compile(pat)))

    def find(self, normalized_text: str) -> list[str]:
        return [kw for kw, p in self.patterns if p.search(normalized_text)]

    def matches(self, normalized_text: str) -> bool:
        return any(p.search(normalized_text) for _, p in self.patterns)


_TRACKING_PARAMS = {"ref", "fbclid", "gclid", "source", "mc_cid", "mc_eid"}


def canonical_url(url: str | None) -> str:
    if not url:
        return ""
    parts = urlsplit(url.strip())
    if not parts.netloc:
        return url.strip()
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    path = parts.path or ""
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")
    query = [
        (k, v)
        for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if not k.lower().startswith("utm_") and k.lower() not in _TRACKING_PARAMS
    ]
    return urlunsplit(("https", host, path, urlencode(query), ""))


_ARXIV_RE = re.compile(r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})(?:v\d+)?", re.I)
_GITHUB_RE = re.compile(r"github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)", re.I)
_GITHUB_RESERVED = {
    "orgs", "topics", "features", "sponsors", "marketplace", "settings", "apps", "about",
    "collections", "trending", "login", "search", "explore", "site", "pricing", "readme",
}


def arxiv_id_from_url(url: str | None) -> str | None:
    m = _ARXIV_RE.search(url or "")
    return m.group(1) if m else None


def _clean_repo(owner: str, repo: str) -> str | None:
    repo = re.sub(r"\.git$", "", repo).rstrip(".")
    if not repo or owner.lower() in _GITHUB_RESERVED:
        return None
    return f"{owner}/{repo}"


def github_repo_from_url(url: str | None) -> str | None:
    m = _GITHUB_RE.search(url or "")
    return _clean_repo(*m.groups()) if m else None


def find_github_repos(text: str | None) -> list[str]:
    seen: dict[str, str] = {}
    for owner, repo in _GITHUB_RE.findall(text or ""):
        full = _clean_repo(owner, repo)
        if full and full.lower() not in seen:
            seen[full.lower()] = full
    return list(seen.values())


def to_iso(value) -> str | None:
    """Convert timestamps / ISO strings / RFC 822 dates to 'YYYY-MM-DDTHH:MM:SSZ' (UTC)."""
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        dt = datetime.fromtimestamp(value, tz=timezone.utc)
    elif isinstance(value, datetime):
        dt = value
    else:
        s = str(value).strip()
        try:
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            try:
                dt = parsedate_to_datetime(s)
            except (TypeError, ValueError, IndexError):
                return None
            if dt is None:
                return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
