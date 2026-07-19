#!/usr/bin/env python3
"""Validate local README assets and check stable public links conservatively."""
from __future__ import annotations

import html
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

# Dynamic image services are deliberately non-critical and are prone to bot blocks,
# cache delays or rate limits. Their URLs are syntax-checked but not fetched in CI.
SKIP_HOSTS = {
    "www.linkedin.com",
    "readme-typing-svg.demolab.com",
    "img.shields.io",
    "komarev.com",
    "skillicons.dev",
    "github-readme-stats.vercel.app",
    "github-readme-streak-stats.herokuapp.com",
}
URL_RE = re.compile(r'''(?:href|src|srcset)=["']([^"']+)|\[[^\]]+\]\(([^)]+)\)''')


def extract_targets(text: str) -> list[str]:
    values: list[str] = []
    for match in URL_RE.finditer(text):
        value = next(group for group in match.groups() if group)
        value = html.unescape(value.strip().split()[0])
        if value not in values:
            values.append(value)
    return values


def check_http(url: str) -> tuple[bool, str]:
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if host in SKIP_HOSTS:
        return True, "skipped (dynamic or bot-blocked service)"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "AlirezaYegane-profile-link-check/2.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return 200 <= response.status < 400, str(response.status)
    except urllib.error.HTTPError as exc:
        return exc.code in {401, 403, 405, 429}, f"HTTP {exc.code} (non-fatal access control/rate limit)"
    except Exception as exc:
        return False, str(exc)


def main() -> int:
    local_only = "--local-only" in sys.argv[1:]
    text = README.read_text(encoding="utf-8")
    failed = False
    for target in extract_targets(text):
        if target.startswith(("mailto:", "#")):
            print(f"OK   {target}")
            continue
        if target.startswith(("http://", "https://")):
            if local_only:
                print(f"OK   {target} — skipped in local-only mode")
                continue
            ok, detail = check_http(target)
            print(f"{'OK' if ok else 'FAIL'} {target} — {detail}")
            failed |= not ok
            time.sleep(0.05)
            continue
        local_target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        local = ROOT / local_target
        ok = local.exists()
        print(f"{'OK' if ok else 'FAIL'} {target} — local asset")
        failed |= not ok
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
