from ScholarScraper import ScholarScraper
import os, git
import subprocess
from datetime import datetime, timezone

class ReadmeUpdater:
    def __init__(self, scholar_id, limit=5, commit_name=None, commit_email=None, target_file="README.md", commit_msg="Update README"):
        self.scholar_id = scholar_id
        self.limit = limit
        self.commit_name = commit_name
        self.commit_email = commit_email
        self.target_file = target_file
        self.commit_msg = commit_msg
        self.scholar_scraper = ScholarScraper()

    def execute_command(self, command, args):
        subprocess.run([command] + args, check=True)

    def get_current_datetime_str(self):
        current_datetime = datetime.now(timezone.utc)
        return current_datetime.strftime("%Y-%m-%d %H:%M:%S %Z")

    def generate_html_content(self, papers_data, current_date_time_str):
        html_content = f'\n## 🧑‍🏫 Top {len(papers_data["papers"])} Publications'
        html_content += "\n\n<table id=\"scholar-table\" style=\"position: relative;\">\n"
        html_content += "  <tr>\n"
        html_content += "    <th>Title</th>\n"
        html_content += "    <th>Authors</th>\n"
        html_content += "    <th>Citations</th>\n"
        html_content += "    <th>Year</th>\n"
        html_content += "  </tr>\n"

        for paper in papers_data["papers"]:
            html_content += (
                f"  <tr>\n     <td><a  href=\"{paper['Paper_URL']}\">{paper['Title']}</a></td>\n"
                f"    <td>{paper['Authors']}</td>\n    <td>{paper['Citations']}</td>\n"
                f"    <td>{paper['Year']}</td>\n  </tr>\n"
            )

        html_content += f"  <tr>\n    <td align=\"center\"   colspan=\"4\" id=\"show-more-cell\" "
        html_content += f"style=\"text-align:center; font-size: larger; position: relative;\" "
        html_content += f"title=\"Last Updated: {current_date_time_str}\">\n"
        html_content += f"<em><a href=\"{papers_data['user_scholar_url']}\" style=\"display: inline-block;\">Show more</a></em></td>\n  </tr>\n</table>\n\n"

        return html_content

    def update_readme(self):
        papers_data = self.scholar_scraper.get_user_papers(self.scholar_id, self.limit)
        current_date_time_str = self.get_current_datetime_str()

        with open(self.target_file, "r", encoding="utf-8") as readme_file:
            readme_content = readme_file.read()

        start_marker = "<!-- SCHOLAR-LIST:START -->"
        end_marker = "<!-- SCHOLAR-LIST:END -->"
        start_pos = readme_content.find(start_marker) + len(start_marker)
        end_pos = readme_content.find(end_marker)

        html_content = self.generate_html_content(papers_data, current_date_time_str)

        new_readme_content = (
            readme_content[:start_pos] + html_content + readme_content[end_pos:]
        )

        # Print the updated content before writing to the file

        with open(self.target_file, "w", encoding="utf-8") as readme_file:
            readme_file.write(new_readme_content)

        print("Changes written to README file.")

        self.show_current_github_repo_info()

    def get_current_github_repo_info(self):
        """
        Get information about the current GitHub repository.
        :return: A dictionary containing repository information.
        """
        try:
            repo = git.Repo(os.getcwd(), search_parent_directories=True)
            repo_info = {
                "Repository Name": repo.remotes.origin.url.split("/")[-1].replace(".git", ""),
                "Owner": repo.remotes.origin.url.split("/")[-2],
                "Branch": repo.active_branch.name,
                "URL": repo.remotes.origin.url,
            }
            return repo_info
        except Exception as e:
            print(f"Failed to retrieve current GitHub repository information: {e}")
            return None

    def show_current_github_repo_info(self):
        """
        Display information about the current GitHub repository.
        """
        repo_info = self.get_current_github_repo_info()

        if repo_info:
            print(f"Current GitHub Repository Information:")
            for key, value in repo_info.items():
                print(f"{key}: {value}")
        else:
            print("Unable to display current GitHub repository information.")



