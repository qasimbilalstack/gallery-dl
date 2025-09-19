# -*- coding: utf-8 -*-

# Copyright 2025 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://simpcity.cr/"""

from .common import Extractor, Message
from .. import text, exception

BASE_PATTERN = r"(?:https?://)?(?:www\.)?simpcity\.(?:cr|su)"


class SimpcityExtractor(Extractor):
    """Base class for simpcity extractors"""

    category = "simpcity"
    root = "https://simpcity.cr"

    def items(self):
        extract_urls = text.re(r'<(?:a [^>]*?href|iframe [^>]*?src)="([^"]+)').findall

        for post in self.posts():
            urls = extract_urls(post["content"])
            data = {"post": post}
            post["count"] = data["count"] = len(urls)
            for data["num"], url in enumerate(urls, 1):
                yield Message.Queue, url, data

    def request_page(self, url):
        try:
            return self.request(url).text
        except exception.HttpError as exc:
            if exc.status == 403 and b">Log in<" in exc.response.content:
                msg = text.extr(exc.response.text, "blockMessage--error", "</")
                raise exception.AuthRequired(
                    "'authenticated cookies'", None, msg.rpartition(">")[2].strip()
                )
            raise

    def _pagination(self, base, pnum=None):
        base = f"{self.root}{base}"

        if pnum is None:
            url = base
            pnum = 1
        else:
            url = f"{base}/page-{pnum}"
            pnum = None

        while True:
            page = self.request_page(url)

            yield page

            if pnum is None or "pageNav-jump--next" not in page:
                return
            pnum += 1
            url = f"{base}/page-{pnum}"

    def _parse_thread(self, page):
        schema = self._extract_jsonld(page)["mainEntity"]
        author = schema["author"]
        stats = schema["interactionStatistic"]
        url_t = schema["url"]
        url_a = author["url"]

        thread = {
            "id": url_t[url_t.rfind(".") + 1 : -1],
            "url": url_t,
            "title": schema["headline"],
            "date": text.parse_datetime(schema["datePublished"]),
            "views": stats[0]["userInteractionCount"],
            "posts": stats[1]["userInteractionCount"],
            "tags": (schema["keywords"].split(", ") if "keywords" in schema else ()),
            "section": schema["articleSection"],
            "author": author["name"],
            "author_id": url_a[url_a.rfind(".") + 1 : -1],
            "author_url": url_a,
        }

        return thread

    def _parse_post(self, html):
        extr = text.extract_from(html)

        post = {
            "author": extr('data-author="', '"'),
            "id": extr('data-content="post-', '"'),
            "author_url": extr('itemprop="url" content="', '"'),
            "date": text.parse_datetime(extr('datetime="', '"')),
            "content": extr(
                '<div itemprop="text">', '<div class="js-selectToQuote'
            ).strip(),
        }

        url_a = post["author_url"]
        post["author_id"] = url_a[url_a.rfind(".") + 1 : -1]

        return post


class SimpcityPostExtractor(SimpcityExtractor):
    subcategory = "post"
    pattern = rf"{BASE_PATTERN}/(?:threads/[^/?#]+/post-|posts/)(\d+)"
    example = "https://simpcity.cr/threads/TITLE.12345/post-54321"

    def posts(self):
        post_id = self.groups[0]
        url = f"{self.root}/posts/{post_id}/"
        page = self.request_page(url)

        pos = page.find(f'data-content="post-{post_id}"')
        if pos < 0:
            raise exception.NotFoundError("post")
        html = text.extract(page, "<article ", "</article>", pos - 200)[0]

        self.kwdict["thread"] = self._parse_thread(page)
        return (self._parse_post(html),)


class SimpcityThreadExtractor(SimpcityExtractor):
    subcategory = "thread"
    pattern = rf"{BASE_PATTERN}(/threads/(?:[^/?#]+\.)?\d+)(?:/page-(\d+))?"
    example = "https://simpcity.cr/threads/TITLE.12345/"

    def posts(self):
        for page in self._pagination(*self.groups):
            if "thread" not in self.kwdict:
                self.kwdict["thread"] = self._parse_thread(page)
            for html in text.extract_iter(page, "<article ", "</article>"):
                yield self._parse_post(html)


class SimpcityForumExtractor(SimpcityExtractor):
    subcategory = "forum"
    pattern = rf"{BASE_PATTERN}(/forums/(?:[^/?#]+\.)?\d+)(?:/page-(\d+))?"
    example = "https://simpcity.cr/forums/TITLE.123/"

    def items(self):
        data = {"_extractor": SimpcityThreadExtractor}
        for page in self._pagination(*self.groups):
            for path in text.extract_iter(page, ' uix-href="', '"'):
                yield Message.Queue, f"{self.root}{text.unquote(path)}", data
