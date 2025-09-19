import json
from gallery_dl.extractor.reddit_json import save_submission_json


def test_save_submission_json_writes_file(tmp_path):
    submission = {
        "id": "abc123",
        "title": "Test post",
        "url": "https://example.com/img.jpg",
    }
    dest_root = tmp_path
    out_path = save_submission_json(submission, dest_root)
    assert out_path is not None
    assert out_path.exists()
    with out_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == submission
    # Check formatting (pretty, not compact)
    text = out_path.read_text("utf-8")
    assert text.startswith("{")
    assert "\n  " in text  # indented


def test_save_submission_json_creates_dirs(tmp_path):
    submission = {
        "id": "def456",
        "title": "Another post",
        "url": "https://example.com/2.jpg",
    }
    dest_root = tmp_path
    out_path = save_submission_json(submission, dest_root, subdir="foo/bar")
    assert out_path.parent.name == "bar"
    assert out_path.parent.parent.name == "foo"
    assert out_path.exists()


def test_save_submission_json_filename_template(tmp_path):
    submission = {"id": "ghi789", "title": "T", "url": "u"}
    dest_root = tmp_path
    out_path = save_submission_json(
        submission, dest_root, filename_template="reddit_{id}.json"
    )
    assert out_path.name == "reddit_ghi789.json"


def test_save_submission_json_missing_id(tmp_path):
    submission = {"title": "No id"}
    dest_root = tmp_path
    out_path = save_submission_json(submission, dest_root)
    assert out_path is None


def test_save_submission_json_logs_warning(tmp_path, capsys):
    # No id, should print warning
    submission = {"foo": "bar"}
    dest_root = tmp_path
    out_path = save_submission_json(submission, dest_root)
    assert out_path is None
    captured = capsys.readouterr()
    assert "Failed to write Reddit submission JSON" in captured.out
