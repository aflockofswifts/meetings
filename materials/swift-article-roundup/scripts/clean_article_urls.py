#!/usr/bin/env python3
"""Clean tracking parameters from article URLs or markdown links."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TRACKING_NAMES = {
    "campaign",
    "email",
    "fbclid",
    "feature",
    "ga_source",
    "gclid",
    "igshid",
    "isfreemail",
    "j",
    "mkt_tok",
    "msclkid",
    "post_id",
    "publication_id",
    "r",
    "ref",
    "ref_src",
    "source",
    "spm",
    "token",
    "trk",
}

TRACKING_PREFIXES = (
    "utm_",
    "mc_",
    "li_",
    "pk_",
    "wt_",
    "_hs",
)

YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "youtu.be",
    "music.youtube.com",
}

YOUTUBE_KEEP = {
    "v",
    "list",
    "t",
    "start",
    "index",
    "time_continue",
}

MARKDOWN_URL_RE = re.compile(r"(\]\()([^)\s]+)(\))")


def is_tracking_param(name: str) -> bool:
    lowered = name.lower()
    return lowered in TRACKING_NAMES or any(lowered.startswith(prefix) for prefix in TRACKING_PREFIXES)


def clean_url(url: str) -> str:
    split = urlsplit(url)
    host = split.netloc.lower()
    is_youtube = host in YOUTUBE_HOSTS

    kept_params = []
    for name, value in parse_qsl(split.query, keep_blank_values=True):
        lowered = name.lower()
        if is_tracking_param(lowered):
            continue
        if is_youtube:
            if lowered in YOUTUBE_KEEP:
                kept_params.append((name, value))
            continue
        kept_params.append((name, value))

    cleaned_query = urlencode(kept_params, doseq=True)
    return urlunsplit((split.scheme, split.netloc, split.path, cleaned_query, ""))


def clean_markdown(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return f"{match.group(1)}{clean_url(match.group(2))}{match.group(3)}"

    return MARKDOWN_URL_RE.sub(replace, text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Remove tracking parameters from URLs.")
    parser.add_argument("urls", nargs="*", help="URLs to clean")
    parser.add_argument("--markdown", type=Path, help="Rewrite markdown links in a file in place")
    args = parser.parse_args()

    if args.markdown:
        text = args.markdown.read_text()
        args.markdown.write_text(clean_markdown(text))
        return 0

    if not args.urls:
        for line in sys.stdin:
            print(clean_url(line.strip()))
        return 0

    for url in args.urls:
        print(clean_url(url))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
