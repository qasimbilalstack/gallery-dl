# -*- coding: utf-8 -*-

# Copyright 2017-2025 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Reddit extractors module"""

import os
import sys
import importlib
from . import reddit, oauth

# Set modules list to only include reddit
modules = ["reddit"]

def extractors():
    """Return list of Reddit extractors"""
    extractors = []
    
    # Reddit extractors
    extractors.extend([
        reddit.RedditSubredditExtractor,
        reddit.RedditUserExtractor,
        reddit.RedditSubmissionExtractor,
        reddit.RedditHomeExtractor,
        reddit.RedditImageExtractor,
    ])
    
    # OAuth extractors
    extractors.extend([
        oauth.OAuthReddit,
    ])
    
    return extractors

def find(url):
    """Find extractor for given URL"""
    for extractor in extractors():
        match = extractor.pattern.search(url)
        if match:
            return extractor, match
    return None, None