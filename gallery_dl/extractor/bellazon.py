# -*- coding: utf-8 -*-

# Copyright 2025 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://www.bellazon.com/"""

from .common import Extractor, Message
from .. import text, exception

BASE_PATTERN = r"(?:https?://)?(?:www\.)?bellazon\.com/main"


class BellazonExtractor(Extractor):
    """Base class for bellazon extractors"""

    category = "bellazon"
    root = "https://www.bellazon.com/main"
    directory_fmt = (
        "{category}",
        "{thread[section]}",
        "{thread[title]} ({thread[id]})",
    )
    filename_fmt = "{post[id]}_{num:>02}_{id}.{extension}"
    archive_fmt = "{post[id]}/{filename}"

    def items(self):
        extract_urls = text.re(r'<a ([^>]*?href="([^"]+)".*?)</a>').findall
        native = f"{self.root}/"

        for post in self.posts():
            urls = extract_urls(post["content"])
            data = {"post": post}
            post["count"] = data["count"] = len(urls)

            yield Message.Directory, data
            for data["num"], (info, url) in enumerate(urls, 1):
                url = text.unescape(url)
                if url.startswith(native):
                    if not (alt := text.extr(info, ' alt="', '"')) or (
                        alt.startswith("post-") and "_thumb." in alt
                    ):
                        name = url
                    else:
                        name = text.unescape(alt)
                    dc = text.nameext_from_url(name, data.copy())
                    dc["id"] = text.extr(info, 'data-fileid="', '"')
                    if ext := text.extr(info, 'data-fileext="', '"'):
                        dc["extension"] = ext
                    yield Message.Url, url, dc
                else:
                    yield Message.Queue, url, data

    def _pagination(self, base, pnum=None):
        base = f"{self.root}{base}"

        if pnum is None:
            url = f"{base}/"
            pnum = 1
        else:
            url = f"{base}/page/{pnum}/"
            pnum = None

        while True:
            page = self.request(url).text

            yield page

            if (
                pnum is None
                or ' rel="next" ' not in page
                or text.extr(page, ' rel="next" data-page=\'', "'") == str(pnum)
            ):
                return
            pnum += 1
            url = f"{base}/page/{pnum}/"

    def _parse_thread(self, page):
        schema = self._extract_jsonld(page)
        author = schema["author"]
        stats = schema["interactionStatistic"]
        url_t = schema["url"]
        url_a = author["url"]

        path = text.split_html(text.extr(page, '<nav class="ipsBreadcrumb', "</nav>"))[
            2:-1
        ]

        thread = {
            "url": url_t,
            "path": path,
            "title": schema["headline"],
            "views": stats[0]["userInteractionCount"],
            "posts": stats[1]["userInteractionCount"],
            "date": text.parse_datetime(schema["datePublished"]),
            "date_updated": text.parse_datetime(schema["dateModified"]),
            "description": text.unescape(schema["text"]),
            "section": path[-2],
            "author": author["name"],
            "author_url": url_a,
        }

        thread["id"], _, thread["slug"] = url_t.rsplit("/", 2)[1].partition("-")
        thread["author_id"], _, thread["author_slug"] = url_a.rsplit("/", 2)[
            1
        ].partition("-")

        return thread

    def _parse_post(self, html):
        extr = text.extract_from(html)

        post = {
            "id": extr('id="elComment_', '"'),
            "author_url": extr(" href='", "'"),
            "date": text.parse_datetime(extr("datetime='", "'")),
            "content": extr("<!-- Post content -->", "\n\t\t</div>"),
        }

        if (pos := post["content"].find(">")) >= 0:
            post["content"] = post["content"][pos + 1 :].strip()

        post["author_id"], _, post["author_slug"] = (
            post["author_url"].rsplit("/", 2)[1].partition("-")
        )

        return post


class BellazonPostExtractor(BellazonExtractor):
    subcategory = "post"
    pattern = (
        rf"{BASE_PATTERN}(/topic/\d+-[\w-]+(?:/page/\d+)?)" rf"/?#findComment-(\d+)"
    )
    example = "https://www.bellazon.com/main/topic/123-SLUG/#findComment-12345"

    def posts(self):
        path, post_id = self.groups
        page = self.request(f"{self.root}{path}").text

        pos = page.find(f'id="elComment_{post_id}')
        if pos < 0:
            raise exception.NotFoundError("post")
        html = text.extract(page, "<article ", "</article>", pos - 100)[0]

        self.kwdict["thread"] = self._parse_thread(page)
        return (self._parse_post(html),)


class BellazonThreadExtractor(BellazonExtractor):
    subcategory = "thread"
    pattern = rf"{BASE_PATTERN}(/topic/\d+-[\w-]+)(?:/page/(\d+))?"
    example = "https://www.bellazon.com/main/topic/123-SLUG/"

    def posts(self):
        for page in self._pagination(*self.groups):
            if "thread" not in self.kwdict:
                self.kwdict["thread"] = self._parse_thread(page)
            for html in text.extract_iter(page, "<article ", "</article>"):
                yield self._parse_post(html)


class BellazonForumExtractor(BellazonExtractor):
    subcategory = "forum"
    pattern = rf"{BASE_PATTERN}(/forum/\d+-[\w-]+)(?:/page/(\d+))?"
    example = "https://www.bellazon.com/main/forum/123-SLUG/"

    def items(self):
        data = {"_extractor": BellazonThreadExtractor}
        for page in self._pagination(*self.groups):
            for row in text.extract_iter(page, '<li data-ips-hook="topicRow"', "</"):
                yield Message.Queue, text.extr(row, 'href="', '"'), data
