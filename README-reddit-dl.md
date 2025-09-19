# reddit-dl

A focused Reddit downloader based on gallery-dl, designed specifically for downloading content from Reddit.

## Installation

```bash
pip install .
```

This will install both `gallery-dl` and `reddit-dl` commands.

## Usage

### Basic Usage

```bash
# Download from a subreddit
reddit-dl https://www.reddit.com/r/GreekCelebs/

# Download from a user profile
reddit-dl https://www.reddit.com/user/SecretKumchie/

# Download a specific post
reddit-dl https://www.reddit.com/user/ressaxxx/comments/1nhy77z/front_or_back/
```

### OAuth Setup (Recommended)

For better rate limits and access to private content:

```bash
reddit-dl oauth:reddit
```

Follow the instructions to authorize reddit-dl with your Reddit account.

### Options

reddit-dl supports all the same options as gallery-dl. For example:

```bash
# Download with custom filename format
reddit-dl -f "{subreddit}_{id}_{title}.{extension}" https://www.reddit.com/r/GreekCelebs/

# Download to specific directory
reddit-dl -d /path/to/downloads https://www.reddit.com/r/GreekCelebs/

# Limit number of downloads
reddit-dl --limit 10 https://www.reddit.com/r/GreekCelebs/
```

For full options list, see: `gallery-dl --help`

## Features

- **Reddit-only**: Only accepts Reddit URLs, ensuring focused usage
- **OAuth support**: Full Reddit OAuth implementation for authenticated access
- **Same capabilities**: All Reddit functionality from gallery-dl preserved
- **URL validation**: Clear error messages for non-Reddit URLs
- **Easy to use**: Simple, focused interface

## Supported URLs

- Subreddits: `https://www.reddit.com/r/subreddit/`
- User profiles: `https://www.reddit.com/user/username/`
- Specific posts: `https://www.reddit.com/r/sub/comments/post_id/title/`
- OAuth setup: `oauth:reddit`

## Configuration

reddit-dl uses the same configuration system as gallery-dl. You can create a configuration file at `~/.config/gallery-dl/config.json` or use command-line options.

Example configuration for Reddit downloads:

```json
{
  "extractor": {
    "reddit": {
      "refresh-token": "your_oauth_token_here",
      "archive": "reddit-archive.txt",
      "sleep": 1
    }
  }
}
```

## Security Note

reddit-dl inherits all the security features of gallery-dl. When using OAuth, your refresh token is stored securely and can be managed through the standard gallery-dl configuration.