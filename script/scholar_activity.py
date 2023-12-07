import os
import subprocess
from datetime import datetime, timezone
from ReadmeUpdater import ReadmeUpdater

if __name__ == "__main__":
    GH_USERNAME = os.environ.get("GH_USERNAME")
    SCHOLAR_ID = os.environ.get("SCHOLAR_ID")
    LIMIT = os.environ.get("LIMIT", 5)
    COMMIT_NAME = os.environ.get("COMMIT_NAME")
    COMMIT_EMAIL = os.environ.get("COMMIT_EMAIL")

    readme_updater = ReadmeUpdater(
        scholar_id=SCHOLAR_ID,
        limit=int(LIMIT),
        commit_name=COMMIT_NAME,
        commit_email=COMMIT_EMAIL
    )
    readme_updater.update_readme()

