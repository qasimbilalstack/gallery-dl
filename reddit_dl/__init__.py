# -*- coding: utf-8 -*-

# Copyright 2014-2025 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""reddit-dl: A focused Reddit downloader based on gallery-dl"""

import sys
import gallery_dl
from gallery_dl import extractor, util

__author__ = "Mike Fährmann"
__copyright__ = "Copyright 2014-2025 Mike Fährmann"
__license__ = "GPLv2"
__maintainer__ = "Mike Fährmann"
__email__ = "mike_faehrmann@web.de"
__version__ = gallery_dl.__version__


def _filter_reddit_extractors():
    """Filter extractors to only include Reddit-related ones"""
    original_list_classes = extractor._list_classes
    
    def filtered_list_classes():
        for cls in original_list_classes():
            # Include Reddit extractors and OAuth Reddit specifically
            if (cls.category == "reddit" or 
                (cls.category == "oauth" and cls.subcategory == "reddit")):
                yield cls
    
    # Replace the extractor listing function
    extractor._list_classes = filtered_list_classes
    # Also update the global function
    extractor.extractors = lambda: sorted(filtered_list_classes(), key=lambda x: x.__name__)
    
    # Update the find function to use filtered extractors
    def filtered_find(url):
        """Find a suitable extractor for the given URL (Reddit-only)"""
        for cls in filtered_list_classes():
            if match := cls.pattern.match(url):
                return cls(match)
        return None
    
    extractor.find = filtered_find


def main():
    """Main entry point for reddit-dl"""
    # Apply Reddit-only filter to extractors
    _filter_reddit_extractors()
    
    # Use gallery-dl's main function with filtered extractors
    return gallery_dl.main()


if __name__ == "__main__":
    sys.exit(main())