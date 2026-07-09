#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []
        self.ids: list[str] = []
        self.images_without_alt: list[str] = []
        self.h1_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.append(element_id)
        if tag == "h1":
            self.h1_count += 1
        if tag == "img" and "alt" not in values:
            self.images_without_alt.append(values.get("src") or "<missing src>")
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.references.append((attribute, value))


def local_target(root: Path, page: Path, raw_value: str) -> Path | None:
    value = raw_value.strip()
    if not value or value.startswith("#"):
        return None
    if value.startswith("//"):
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None
    clean_path = unquote(parsed.path)
    if not clean_path:
        return None
    target = root / clean_path.lstrip("/") if clean_path.startswith("/") else page.parent / clean_path
    if clean_path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target.resolve()


def audit(root: Path, expected_asset_version: str | None) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    pages = sorted(root.rglob("*.html"))
    for page in pages:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        relative = page.relative_to(root)

        duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
        if duplicates:
            errors.append(f"{relative}: duplicate ids: {', '.join(duplicates)}")
        if parser.h1_count != 1:
            errors.append(f"{relative}: expected one h1, found {parser.h1_count}")
        for src in parser.images_without_alt:
            errors.append(f"{relative}: image missing alt: {src}")

        for attribute, value in parser.references:
            target = local_target(root, page, value)
            if target is not None:
                try:
                    target.relative_to(root)
                except ValueError:
                    errors.append(f"{relative}: {attribute} outside site root: {value}")
                else:
                    if not target.exists():
                        errors.append(f"{relative}: broken {attribute}: {value}")
                if expected_asset_version and ("assets/site.css" in value or "assets/site.js" in value):
                    if urlsplit(value).query != f"v={expected_asset_version}":
                        errors.append(
                            f"{relative}: shared asset version must be {expected_asset_version}: {value}"
                        )

    print(f"HTML pages checked: {len(pages)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="docs")
    parser.add_argument("--asset-version")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"Error: site root is not a directory: {args.root}", file=sys.stderr)
        return 2
    errors = audit(root, args.asset_version)
    if errors:
        for error in errors:
            print(error)
        print(f"Errors: {len(errors)}")
        return 1
    print("Errors: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
