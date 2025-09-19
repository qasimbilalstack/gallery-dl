# -*- coding: utf-8 -*-

# Copyright 2014-2025 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import sys
import logging
from . import version

__author__ = "Mike Fährmann"
__copyright__ = "Copyright 2014-2025 Mike Fährmann"
__license__ = "GPLv2"
__maintainer__ = "Mike Fährmann"
__email__ = "mike_faehrmann@web.de"
__version__ = version.__version__


def main():
    """Simplified main function that delegates to gallery-dl with Reddit focus"""
    try:
        # Handle help and version before delegating to gallery-dl
        if "--help" in sys.argv or "-h" in sys.argv:
            print("reddit-dl - Reddit downloader based on gallery-dl")
            print("Usage: reddit-dl [OPTIONS] URL [URL...]")
            print("")
            print("Supported URLs:")
            print("  - https://www.reddit.com/r/subreddit/")
            print("  - https://www.reddit.com/user/username/")
            print("  - https://www.reddit.com/r/sub/comments/post_id/")
            print("")
            print("OAuth setup:")
            print("  reddit-dl oauth:reddit")
            print("")
            print("For full options, see: gallery-dl --help")
            sys.exit(0)
        
        # Show version
        if "--version" in sys.argv:
            print(f"reddit-dl {__version__}")
            sys.exit(0)
            
        # Check if URL is Reddit-related by examining command line arguments properly
        args = sys.argv[1:]
        urls = []
        skip_next = False
        
        for i, arg in enumerate(args):
            if skip_next:
                skip_next = False
                continue
                
            if arg.startswith('-'):
                # Check if this option takes a value
                if i + 1 < len(args) and not args[i + 1].startswith('-'):
                    skip_next = True
                continue
            
            # This should be a URL
            urls.append(arg)
        
        if urls:
            for url in urls:
                if not (url.startswith('oauth:reddit') or 
                       'reddit.com' in url or 
                       url == 'noop'):
                    print(f"Error: reddit-dl only supports Reddit URLs. Got: {url}")
                    return 1
        
        # Import gallery-dl and use it as the backend
        import gallery_dl
        
        # Run gallery-dl with the same arguments
        return gallery_dl.main()
        
    except KeyboardInterrupt:
        raise SystemExit("\nKeyboardInterrupt")
    except Exception as exc:
        print(f"Error: {exc}")
        return 1