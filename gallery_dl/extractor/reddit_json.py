"""
Helper to save reddit submission JSON sidecars.

Writes readable UTF-8 JSON (ensure_ascii=False, indent=2), creates directories
as needed, logs errors as warnings and returns the written path on success.
"""

import json
from pathlib import Path


def save_submission_json(
    submission, dest_root, subdir="json", filename_template="{id}.json", logger=None
):
    """
    Save the full Reddit submission JSON to a sidecar file.

    Args:
        submission (dict): The Reddit submission data.
        dest_root (str or Path): The root directory for output.
        subdir (str): Subdirectory under dest_root to save JSON files.
        filename_template (str): Filename template, e.g., "{id}.json".
        logger (logging.Logger, optional): Logger for warnings/errors.

    Returns:
        Path: The path to the written JSON file, or None on failure.
    """
    try:
        sub_id = submission.get("id")
        if not sub_id:
            raise ValueError("Submission dict missing 'id'")
        filename = filename_template.format(**submission)
        out_dir = Path(dest_root) / subdir
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / filename
        # Write atomically to avoid concurrency issues
        tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
        with tmp_path.open("w", encoding="utf-8") as fp:
            json.dump(submission, fp, ensure_ascii=False, indent=2)
            fp.write("\n")
        tmp_path.replace(out_path)
        return out_path
    except Exception as exc:
        msg = f"Failed to write Reddit submission JSON: {exc}"
        if logger:
            logger.warning(msg)
        else:
            print(msg)
        return None
