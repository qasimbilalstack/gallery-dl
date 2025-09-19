# -*- coding: utf-8 -*-

import unittest
import sys
from unittest.mock import patch, MagicMock

import reddit_dl


class TestRedditDl(unittest.TestCase):

    def test_version(self):
        """Test that reddit-dl shows correct version"""
        with patch('sys.argv', ['reddit-dl', '--version']):
            with patch('sys.exit') as mock_exit:
                reddit_dl.main()
                mock_exit.assert_called_with(0)

    def test_help(self):
        """Test that reddit-dl shows help"""
        with patch('sys.argv', ['reddit-dl', '--help']):
            with patch('sys.exit') as mock_exit:
                reddit_dl.main()
                mock_exit.assert_called_with(0)

    def test_rejects_non_reddit_urls(self):
        """Test that non-Reddit URLs are rejected"""
        with patch('sys.argv', ['reddit-dl', 'https://www.example.com']):
            result = reddit_dl.main()
            self.assertEqual(result, 1)

    def test_accepts_reddit_urls(self):
        """Test that Reddit URLs are accepted"""
        with patch('sys.argv', ['reddit-dl', 'https://www.reddit.com/r/test/']):
            with patch('gallery_dl.main') as mock_gallery:
                mock_gallery.return_value = 0
                result = reddit_dl.main()
                self.assertEqual(result, 0)
                mock_gallery.assert_called_once()

    def test_accepts_oauth_reddit(self):
        """Test that oauth:reddit is accepted"""
        with patch('sys.argv', ['reddit-dl', 'oauth:reddit']):
            with patch('gallery_dl.main') as mock_gallery:
                mock_gallery.return_value = 0
                result = reddit_dl.main()
                self.assertEqual(result, 0)
                mock_gallery.assert_called_once()


if __name__ == '__main__':
    unittest.main()