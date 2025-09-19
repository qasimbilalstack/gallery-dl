#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import reddit_dl
import gallery_dl.extractor as extractor


class TestRedditDL(unittest.TestCase):
    """Test reddit-dl functionality"""

    def setUp(self):
        """Reset extractor state before each test"""
        # Store original functions
        self.original_list_classes = extractor._list_classes
        self.original_extractors = extractor.extractors
        self.original_find = extractor.find

    def tearDown(self):
        """Restore original extractor state after each test"""
        extractor._list_classes = self.original_list_classes
        extractor.extractors = self.original_extractors
        extractor.find = self.original_find

    def test_filter_reddit_extractors(self):
        """Test that filtering works correctly"""
        # Apply reddit filter
        reddit_dl._filter_reddit_extractors()
        
        # Get all extractors
        extractors_list = list(extractor.extractors())
        extractor_names = [e.__name__ for e in extractors_list]
        
        # Should only have Reddit-related extractors
        expected_reddit_extractors = {
            'RedditUserExtractor',
            'RedditSubredditExtractor', 
            'RedditSubmissionExtractor',
            'RedditHomeExtractor',
            'RedditImageExtractor',
            'OAuthReddit'
        }
        
        # Check that all expected Reddit extractors are present
        for expected in expected_reddit_extractors:
            self.assertIn(expected, extractor_names, 
                         f"{expected} should be available in reddit-dl")
        
        # Check that non-Reddit extractors are filtered out
        non_reddit_extractors = {
            'TwitterUserExtractor',
            'InstagramUserExtractor', 
            'FlickrUserExtractor',
            'OAuthFlickr',
            'OAuthPixiv'
        }
        
        for non_reddit in non_reddit_extractors:
            self.assertNotIn(non_reddit, extractor_names,
                           f"{non_reddit} should be filtered out in reddit-dl")

    def test_url_recognition(self):
        """Test that reddit-dl recognizes the specified test URLs"""
        # Apply reddit filter
        reddit_dl._filter_reddit_extractors()
        
        test_cases = [
            {
                'url': 'https://www.reddit.com/user/SecretKumchie/',
                'expected_extractor': 'RedditUserExtractor'
            },
            {
                'url': 'https://www.reddit.com/r/GreekCelebs/',
                'expected_extractor': 'RedditSubredditExtractor'
            },
            {
                'url': 'https://www.reddit.com/user/ressaxxx/comments/1nhy77z/front_or_back/',
                'expected_extractor': 'RedditSubmissionExtractor'
            }
        ]
        
        for case in test_cases:
            with self.subTest(url=case['url']):
                extractor_instance = extractor.find(case['url'])
                self.assertIsNotNone(extractor_instance, 
                                   f"Should find extractor for {case['url']}")
                self.assertEqual(extractor_instance.__class__.__name__, 
                               case['expected_extractor'],
                               f"Wrong extractor for {case['url']}")

    def test_oauth_reddit_support(self):
        """Test that OAuth Reddit is supported"""
        # Apply reddit filter
        reddit_dl._filter_reddit_extractors()
        
        # Check that oauth:reddit URL is recognized
        oauth_extractor = extractor.find('oauth:reddit')
        self.assertIsNotNone(oauth_extractor, "Should support oauth:reddit")
        self.assertEqual(oauth_extractor.__class__.__name__, 'OAuthReddit')

    @patch('gallery_dl.main')
    def test_main_function_calls_gallery_dl_main(self, mock_gallery_main):
        """Test that reddit_dl.main() calls gallery_dl.main() with filtering applied"""
        mock_gallery_main.return_value = 0
        
        result = reddit_dl.main()
        
        # Should call gallery_dl.main
        mock_gallery_main.assert_called_once()
        
        # Should return the result from gallery_dl.main
        self.assertEqual(result, 0)
        
        # Verify filtering was applied by checking extractor list
        extractors_list = list(extractor.extractors())
        extractor_names = [e.__name__ for e in extractors_list]
        
        # Should only have Reddit extractors
        self.assertTrue(all('Reddit' in name or name == 'OAuthReddit' 
                          for name in extractor_names),
                       "All extractors should be Reddit-related after main() call")

    def test_non_reddit_urls_not_supported(self):
        """Test that non-Reddit URLs are not supported after filtering"""
        # Apply reddit filter
        reddit_dl._filter_reddit_extractors()
        
        non_reddit_urls = [
            'https://twitter.com/user',
            'https://www.instagram.com/user/',
            'https://www.flickr.com/photos/user/',
            'https://example.com/image.jpg'
        ]
        
        for url in non_reddit_urls:
            with self.subTest(url=url):
                extractor_instance = extractor.find(url)
                self.assertIsNone(extractor_instance,
                                f"Should not find extractor for non-Reddit URL {url}")


if __name__ == '__main__':
    unittest.main()