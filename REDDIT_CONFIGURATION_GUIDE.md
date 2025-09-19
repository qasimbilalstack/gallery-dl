# Reddit Download Organization

## Configuration-Based Approach (Recommended)

Instead of modifying the source code directly, you can use configuration settings to organize your Reddit downloads exactly as needed. This approach is more flexible and doesn't require code changes.

### Example Configuration

Create a configuration file (e.g., `reddit-config.json`) with the following settings:

```json
{
    "extractor": {
        "base-directory": "./gallery-dl/",
        
        "reddit": {
            "write_submission_json": true,
            "submission_json_dir": "",
            "submission_json_filename": "{id}.json",
            "external_filename_prefix": true,
            "parent-directory": true,
            "parent-metadata": "_reddit"
        },
        
        "reddit.user": {
            "directory": ["{category}", "{author}"]
        },
        
        "reddit.subreddit": {
            "directory": ["{category}", "{subreddit}"]
        },
        
        "reddit>*": {
            "directory": [],
            "filename": "{_reddit[id]}_{filename}"
        }
    }
}
```

### What This Configuration Does

1. **JSON Sidecars**: Saves Reddit submission JSON files alongside media files
2. **Directory Organization**:
   - Subreddit downloads: `./gallery-dl/reddit/Hotwife/`
   - User downloads: `./gallery-dl/reddit/stolenones/`
3. **External Media**: External content (from redgifs, imgur, etc.) is saved in the same directory as Reddit content
4. **Filename Prefixing**: External media files are prefixed with the Reddit post ID

### Usage

```bash
# Use the configuration file
gallery-dl --config reddit-config.json https://www.reddit.com/r/Hotwife

# Or copy the settings to your main configuration file
```

### Configuration Explanation

- `reddit.user.directory`: Controls directory structure for user URLs
  - `{category}` = "reddit"
  - `{author}` = username (e.g., "stolenones")
  
- `reddit.subreddit.directory`: Controls directory structure for subreddit URLs
  - `{category}` = "reddit" 
  - `{subreddit}` = subreddit name (e.g., "Hotwife")
  
- `reddit>*`: Settings for external extractors called from Reddit
  - `directory: []` = Use parent directory (no subdirectories)
  - `filename: "{_reddit[id]}_{filename}"` = Prefix with Reddit post ID

- `parent-directory: true`: Child extractors use Reddit's directory
- `parent-metadata: "_reddit"`: Pass Reddit metadata to child extractors

### Benefits of Configuration Approach

1. **No Code Changes**: Works with any gallery-dl version
2. **Flexible**: Easy to modify directory structure without recompiling
3. **Maintainable**: Configuration survives updates
4. **Portable**: Can share configuration files between systems
5. **Safe**: No risk of breaking the application

### Alternative: Direct Code Modification

If you prefer to modify the source code directly, you can add `directory_fmt` attributes to the extractor classes in `gallery_dl/extractor/reddit.py`. However, this is not recommended as it makes the code harder to maintain and update.