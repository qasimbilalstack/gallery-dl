```markdown
### Save reddit submission JSON sidecars

New options (under `extractor.reddit`):

- `write_submission_json` (boolean, default: `true`):
  If enabled, saves the full Reddit submission JSON to a sidecar file for each processed submission, even when media is delegated to an external extractor. The JSON is written to `<destination-root>/<submission_json_dir>/<submission_json_filename>`, using UTF-8 encoding, `ensure_ascii=False`, and `indent=2`. Directories are created as needed. Errors are logged as warnings and do not abort downloads. By default, this feature is enabled.
- `submission_json_dir` (string, default: `""`):
  Subdirectory under the destination root where submission JSON files are saved. Empty string means files are saved in the same directory as media.
- `submission_json_filename` (string, default: `"{id}.json"`):
  Filename template for the JSON sidecar. You can use submission fields like `{id}`.

- `external_filename_prefix` (boolean, default: `true`):
  Whether to prefix external media filenames (from redgifs, imgur, etc.) with the Reddit post ID.

**Security note:** Saved JSON can include usernames and other user data. This feature is enabled by default to preserve submission metadata.
```
