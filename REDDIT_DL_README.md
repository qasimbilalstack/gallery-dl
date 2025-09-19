# reddit-dl

A Reddit-focused command-line tool built on top of gallery-dl, designed specifically for downloading images and collections from Reddit.

## Overview

reddit-dl is a specialized version of gallery-dl that:
- Only accepts Reddit URLs (reddit.com) and `oauth:reddit`
- Maintains all Reddit functionality from gallery-dl
- Preserves OAuth authentication capabilities
- Filters out non-Reddit URLs with helpful warnings

## Installation

Install as part of the gallery-dl package:

```bash
python setup.py install
```

This will install both `gallery-dl` and `reddit-dl` commands.

## Usage

### Basic Usage

```bash
# Download from a Reddit user
reddit-dl https://www.reddit.com/user/SecretKumchie/

# Download from a subreddit  
reddit-dl https://www.reddit.com/r/GreekCelebs/

# Download a specific submission
reddit-dl https://www.reddit.com/user/ressaxxx/comments/1nhy77z/front_or_back/
```

### OAuth Authentication

```bash
# Set up OAuth for private/rate-limited access
reddit-dl oauth:reddit
```

### Options

reddit-dl supports all the same options as gallery-dl:

```bash
# Simulate download (don't actually download)
reddit-dl -s https://www.reddit.com/r/example/

# Custom output directory
reddit-dl -d /path/to/output https://www.reddit.com/user/example/

# Custom filename format
reddit-dl -f "{subreddit}_{id}_{title}.{extension}" https://www.reddit.com/r/example/
```

## Features

- **URL Filtering**: Automatically filters out non-Reddit URLs with helpful warnings
- **OAuth Support**: Full support for Reddit OAuth authentication via `oauth:reddit`
- **All Reddit Features**: Maintains all Reddit-specific functionality from gallery-dl
- **JSON Sidecars**: Supports Reddit submission JSON sidecar files
- **External Media**: Handles external media links with Reddit ID prefixing
- **Same Configuration**: Uses the same configuration system as gallery-dl

## Differences from gallery-dl

1. **URL Filtering**: Only accepts Reddit URLs and `oauth:reddit`
2. **Program Name**: Shows as "reddit-dl" in help and version output
3. **Description**: Tailored description for Reddit downloading
4. **Error Messages**: Specific messaging about Reddit URL requirements

## Examples

```bash
# This works - Reddit URLs
reddit-dl https://www.reddit.com/user/example/
reddit-dl https://www.reddit.com/r/example/
reddit-dl oauth:reddit

# This is filtered out with warnings
reddit-dl https://example.com https://www.reddit.com/user/example/
# Output: [warning] Ignoring non-Reddit URL: https://example.com

# Mixed URLs - only Reddit ones are processed
reddit-dl https://instagram.com/user/ https://www.reddit.com/user/example/ https://twitter.com/user/
# Only the Reddit URL will be processed
```

## Configuration

reddit-dl uses the same configuration files and options as gallery-dl. All Reddit-specific configuration options work identically:

```json
{
  "extractor": {
    "reddit": {
      "refresh-token": "your_token_here",
      "comments": 500,
      "morecomments": true
    }
  }
}
```

## Development

The reddit-dl implementation is a lightweight wrapper around gallery-dl that:
1. Parses command line arguments
2. Filters URLs to only Reddit ones
3. Calls the original gallery-dl main function
4. Maintains all original functionality

Source code structure:
- `bin/reddit-dl` - Command line entry point
- `reddit_dl/__init__.py` - Main module with URL filtering logic
- `reddit_dl/__main__.py` - Module entry point
- `setup.py` - Updated to include reddit-dl console script