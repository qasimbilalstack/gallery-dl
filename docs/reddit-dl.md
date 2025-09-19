# reddit-dl

reddit-dl is a focused Reddit downloader based on gallery-dl that only supports Reddit extraction. It provides all the same functionality as gallery-dl for Reddit content but in a lightweight package that excludes extractors for other sites.

## Features

reddit-dl supports all Reddit-related extractors available in gallery-dl:
- **User profiles**: Download all posts from Reddit users
- **Subreddits**: Download content from specific subreddits
- **Individual submissions**: Download specific Reddit posts and their comments
- **Home feed**: Download content from your Reddit home feed
- **OAuth authentication**: Full support for Reddit OAuth authentication

## Installation

If you have gallery-dl installed, reddit-dl is automatically available. The reddit-dl tool reuses the same gallery-dl installation and configuration.

To install gallery-dl (which includes reddit-dl):
```bash
pip install gallery-dl
```

## Usage

reddit-dl uses the same command-line interface as gallery-dl, but only supports Reddit URLs:

### Basic Usage

Download a user's posts:
```bash
reddit-dl https://www.reddit.com/user/SecretKumchie/
```

Download a subreddit:
```bash
reddit-dl https://www.reddit.com/r/GreekCelebs/
```

Download a specific submission:
```bash
reddit-dl https://www.reddit.com/user/ressaxxx/comments/1nhy77z/front_or_back/
```

### Common Options

All gallery-dl options work with reddit-dl:

```bash
# Custom filename format
reddit-dl -f "{subreddit}/{id}_{title}.{extension}" https://www.reddit.com/r/GreekCelebs/

# Custom download directory
reddit-dl -d ~/Downloads/reddit https://www.reddit.com/user/SecretKumchie/

# Limit number of posts
reddit-dl --range 1-50 https://www.reddit.com/r/GreekCelebs/

# Write metadata
reddit-dl --write-metadata https://www.reddit.com/user/SecretKumchie/

# Simulate (don't download, just show what would be downloaded)
reddit-dl --simulate https://www.reddit.com/r/GreekCelebs/
```

## Authentication with OAuth

reddit-dl supports Reddit OAuth authentication using the same configuration as gallery-dl.

### Interactive OAuth Setup

To set up OAuth authentication interactively:

```bash
reddit-dl oauth:reddit
```

This will open a browser window where you can authorize the application and grant access to your Reddit account.

### Configuration File Setup

You can also configure OAuth credentials in your gallery-dl configuration file. Create or edit `~/.config/gallery-dl/config.json`:

```json
{
    "extractor": {
        "reddit": {
            "client-id": "your_reddit_client_id",
            "client-secret": "your_reddit_client_secret",
            "user-agent": "your_custom_user_agent"
        }
    }
}
```

### Environment Variables

OAuth credentials can also be provided via environment variables:
```bash
export REDDIT_CLIENT_ID="your_reddit_client_id"
export REDDIT_CLIENT_SECRET="your_reddit_client_secret" 
export REDDIT_USER_AGENT="your_custom_user_agent"
```

## Configuration

reddit-dl uses the same configuration system as gallery-dl. All Reddit-specific configuration options are supported:

```json
{
    "extractor": {
        "reddit": {
            "comments": 500,
            "morecomments": true,
            "previews": true,
            "videos": true,
            "write-submission-json": true
        }
    }
}
```

Common Reddit configuration options:
- `comments`: Number of comments to download (default: 0)
- `morecomments`: Download additional comment threads (default: false)
- `previews`: Download preview images (default: true)
- `videos`: Download videos (default: true)
- `write-submission-json`: Save submission metadata as JSON (default: true)

## Differences from gallery-dl

reddit-dl is functionally identical to gallery-dl when used with Reddit URLs, but:

1. **Only supports Reddit**: Non-Reddit URLs will be rejected with an error
2. **Smaller footprint**: Only loads Reddit-related extractors
3. **Same configuration**: Uses the same config files and format as gallery-dl
4. **Same authentication**: OAuth setup and credentials are identical

## Examples

Here are some practical examples using the test URLs:

### Download a user's posts with metadata
```bash
reddit-dl --write-metadata -d ~/reddit-downloads https://www.reddit.com/user/SecretKumchie/
```

### Browse a subreddit with custom filename format
```bash
reddit-dl -f "{subreddit}/{date:%Y-%m-%d}_{id}_{title}.{extension}" https://www.reddit.com/r/GreekCelebs/
```

### Download a specific post with comments
```bash
reddit-dl --extractor-args "comments:100" https://www.reddit.com/user/ressaxxx/comments/1nhy77z/front_or_back/
```

### Set up OAuth and download your home feed
```bash
# First, authenticate
reddit-dl oauth:reddit

# Then download your home feed
reddit-dl https://www.reddit.com/
```

## Getting Help

For more information about available options and configuration:

```bash
# Show all command-line options
reddit-dl --help

# Show extractor-specific options
reddit-dl --extractor-info reddit

# List available keywords for URL formatting
reddit-dl --list-keywords https://www.reddit.com/r/GreekCelebs/
```

## Relationship to gallery-dl

reddit-dl is not a separate application but rather a focused interface to gallery-dl. It:
- Reuses all gallery-dl code for Reddit extraction
- Shares the same configuration files and format
- Provides identical functionality for Reddit content
- Maintains the same command-line interface

This ensures that reddit-dl stays up-to-date with gallery-dl improvements and maintains compatibility with existing configurations and workflows.