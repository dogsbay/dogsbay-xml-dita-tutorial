#!/usr/bin/env python3
"""Check local HTML links, fragment IDs, images, and styles in a build directory."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.base = None
        self.duplicates = []
        self.feed(path.read_text(encoding='utf-8', errors='replace'))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        value = attrs.get('id')
        if value:
            if value in self.ids:
                self.duplicates.append(value)
            self.ids.add(value)
        if tag == 'a' and attrs.get('name'):
            self.ids.add(attrs['name'])
        if tag == 'base' and 'href' in attrs:
            self.base = attrs['href']
        for attr in ('href', 'src'):
            if tag != 'base' and attrs.get(attr) is not None:
                self.links.append((self.getpos()[0], attrs[attr]))


def check(root):
    root = root.resolve()
    files = sorted(set(root.rglob('*.html')) | set(root.rglob('*.htm')))
    if not files:
        return ['No HTML files found; build the deliverables first.'], 0
    pages = {p.resolve(): Page(p) for p in files}
    failures = []
    for file, page in list(pages.items()):
        location = file.relative_to(root)
        if page.base is not None:
            failures.append(f'{location}: base href is unsupported; check this page with a browser-based crawler')
            continue
        for duplicate in page.duplicates:
            failures.append(f'{location}: duplicate id {duplicate!r}')
        for line, raw in page.links:
            try:
                url = urlsplit(raw)
            except ValueError:
                failures.append(f'{location}:{line}: malformed URL: {raw}')
                continue
            if url.scheme or url.netloc:
                continue
            pathname = unquote(url.path)
            target = ((root / pathname.lstrip('/')) if pathname.startswith('/') else file.parent / pathname).resolve() if pathname else file
            if not target.is_relative_to(root):
                failures.append(f'{location}:{line}: target escapes build directory: {raw}')
                continue
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_file():
                failures.append(f'{location}:{line}: missing target: {raw}')
            elif url.fragment and target.suffix.lower() in ('.html', '.htm'):
                fragment = unquote(url.fragment).split(':~:text=', 1)[0]
                if target not in pages:
                    pages[target] = Page(target)
                if fragment and fragment not in pages[target].ids:
                    failures.append(f'{location}:{line}: missing fragment: {raw}')
    return failures, len(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path, help='Common build root containing all deliverables, usually out/')
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error('build directory does not exist')
    failures, count = check(args.directory)
    for failure in failures:
        print(failure)
    print(f'{count} HTML pages checked; {len(failures)} failures')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
