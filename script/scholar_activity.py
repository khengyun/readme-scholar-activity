import os
import subprocess
from datetime import datetime, timezone
from ReadmeUpdater import ReadmeUpdater



def list_tree(path='.'):
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for file in files:
            file_path = os.path.join(root, file)
            print('{}{}'.format(subindent, file_path))



if __name__ == "__main__":
    # list_tree()
    # os.chdir("/action/workspace/")
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

