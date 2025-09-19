import json
import os
from unittest.mock import Mock
from gallery_dl.extractor.reddit import RedditExtractor


def create_mock_extractor(config_values=None):
    """Create a mock Reddit extractor for testing"""
    # Create a mock match object
    mock_match = Mock()
    mock_match.string = "https://www.reddit.com/r/test"
    mock_match.groups.return_value = ()
    
    # Create extractor instance
    extractor = RedditExtractor(mock_match)
    
    # Mock config method to return test values
    def mock_config(key, default=None):
        if config_values and key in config_values:
            return config_values[key]
        return default
    extractor.config = mock_config
    
    return extractor


def test_save_submission_json_writes_file(tmp_path):
    extractor = create_mock_extractor()
    submission = {
        "id": "abc123",
        "title": "Test post",
        "url": "https://example.com/img.jpg",
    }
    dest_root = str(tmp_path)
    out_path = extractor._save_submission_json(submission, dest_root)
    assert out_path is not None
    assert os.path.exists(out_path)
    with open(out_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["id"] == "abc123"
    assert loaded["title"] == "Test post"
    # Check that JSON is formatted (pretty-printed)
    with open(out_path, "r", encoding="utf-8") as f:
        text = f.read()
    assert text.startswith("{")
    assert "\n  " in text  # indented


def test_save_submission_json_creates_dirs(tmp_path):
    # Test with subdirectory config
    extractor = create_mock_extractor({"submission_json_dir": "foo/bar"})
    submission = {
        "id": "def456",
        "title": "Another post",
        "url": "https://example.com/2.jpg",
    }
    dest_root = str(tmp_path)
    out_path = extractor._save_submission_json(submission, dest_root)
    assert os.path.basename(os.path.dirname(out_path)) == "bar"
    assert os.path.basename(os.path.dirname(os.path.dirname(out_path))) == "foo"
    assert os.path.exists(out_path)


def test_save_submission_json_filename_template(tmp_path):
    # Test with custom filename template
    extractor = create_mock_extractor({"submission_json_filename": "reddit_{id}.json"})
    submission = {"id": "ghi789", "title": "T", "url": "u"}
    dest_root = str(tmp_path)
    out_path = extractor._save_submission_json(submission, dest_root)
    assert os.path.basename(out_path) == "reddit_ghi789.json"


def test_save_submission_json_missing_id(tmp_path):
    extractor = create_mock_extractor()
    submission = {"title": "No id"}
    dest_root = str(tmp_path)
    out_path = extractor._save_submission_json(submission, dest_root)
    assert out_path is None


def test_save_submission_json_logs_warning(tmp_path, caplog):
    # No id, should log warning
    extractor = create_mock_extractor()
    submission = {"foo": "bar"}
    dest_root = str(tmp_path)
    out_path = extractor._save_submission_json(submission, dest_root)
    assert out_path is None
    assert "Failed to write Reddit submission JSON" in caplog.text