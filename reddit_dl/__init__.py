# -*- coding: utf-8 -*-

# Copyright 2014-2025 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import sys
import logging
from gallery_dl import main as gallery_dl_main, option, output

__author__ = "Mike Fährmann"
__copyright__ = "Copyright 2014-2025 Mike Fährmann"
__license__ = "GPLv2"
__maintainer__ = "Mike Fährmann"
__email__ = "mike_faehrmann@web.de"


def main():
    """Reddit-dl main function - wrapper around gallery-dl with Reddit URL filtering"""
    try:
        # Parse arguments first to check URLs
        parser = option.build_parser()
        parser.prog = "reddit-dl"
        parser.description = "Command-line program to download images and collections from Reddit"
        
        args = parser.parse_args()
        
        # If URLs are provided, filter to only Reddit URLs
        if hasattr(args, 'urls') and args.urls:
            original_urls = args.urls[:]
            reddit_urls = []
            
            for url in original_urls:
                if url == "oauth:reddit" or "reddit.com" in url:
                    reddit_urls.append(url)
                else:
                    # Initialize logging if not done yet to show warning
                    if 'log' not in locals():
                        log = output.initialize_logging(getattr(args, 'loglevel', logging.INFO))
                    log.warning("Ignoring non-Reddit URL: %s", url)
                    log.info("reddit-dl only supports Reddit URLs and 'oauth:reddit'")
            
            if not reddit_urls:
                if 'log' not in locals():
                    log = output.initialize_logging(getattr(args, 'loglevel', logging.INFO))
                log.error("No valid Reddit URLs provided")
                log.info("reddit-dl only supports Reddit URLs (reddit.com) and 'oauth:reddit'")
                return 1
            
            # Replace args.urls with filtered URLs
            args.urls = reddit_urls
        
        # Now call the original gallery-dl main function with modified args
        # We need to modify sys.argv to match our filtered URLs
        if hasattr(args, 'urls') and args.urls:
            # Find where URLs start in sys.argv and replace them
            argv_copy = sys.argv[:]
            
            # Find the position where URLs start (after the last option)
            url_start_idx = 1
            for i, arg in enumerate(argv_copy[1:], 1):
                if not arg.startswith('-') and i > 1 and not argv_copy[i-1].startswith('-'):
                    url_start_idx = i
                    break
                elif not arg.startswith('-'):
                    url_start_idx = i
                    break
            
            # Replace sys.argv with filtered URLs
            sys.argv = argv_copy[:url_start_idx] + reddit_urls
        
        # Change program name in sys.argv[0] for gallery-dl to use
        sys.argv[0] = sys.argv[0].replace('reddit_dl', 'reddit-dl')
        
        # Call the original gallery-dl main function
        return gallery_dl_main()
        
    except KeyboardInterrupt:
        return 1
    except Exception:
        # Let gallery-dl handle other exceptions
        return gallery_dl_main()