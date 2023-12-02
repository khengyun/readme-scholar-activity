import time, requests
from bs4 import BeautifulSoup

class ScholarScraper:
    def __init__(self):
        self.base_url = "https://scholar.google.com"
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.user_scholar_url = ""

    def _retry_request(self, url, max_retries=3):
        for attempt in range(max_retries):
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                return response
            else:
                print(
                    f'Retry {attempt + 1}/{max_retries}. Status code: {response.status_code}'
                )
                time.sleep(5 * (attempt + 1))  # Increase the delay with each retry

        return None

    def get_scholar_papers(self, user_id, limit=None):
        url = f'{self.base_url}/citations?user={user_id}&hl=en'
        self.user_scholar_url = url
        response = self._retry_request(url)

        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            papers = []

            paper_elements = soup.find_all('tr', {'class': 'gsc_a_tr'})

            for i, paper_element in enumerate(paper_elements):
                if limit and i >= limit:
                    break

                title_element = paper_element.find('a', {'class': 'gsc_a_at'})
                authors_element = paper_element.find('div', {'class': 'gs_gray'})
                citation_element = paper_element.find('a', {'class': 'gsc_a_ac'})
                year_element = paper_element.find('span', {'class': 'gsc_a_h'})

                title = title_element.text.strip() if title_element else 'N/A'
                authors = authors_element.text.strip() if authors_element else 'N/A'
                citations = citation_element.text.strip() if citation_element else 'N/A'
                year = year_element.text.strip() if year_element else 'N/A'

                conference_element = paper_element.find('div', {'class': 'gs_gray'})
                conference = conference_element.text.strip() if conference_element else 'N/A'
                paper_url = title_element.get('href') if title_element else 'N/A'

                paper_info = {
                    'Title': title,
                    'Authors': authors,
                    'Citations': citations,
                    'Year': year,
                    'Conference': conference,
                    'Paper_URL': self.base_url + paper_url
                }

                papers.append(paper_info)

            return papers
        else:
            print(f'Error: Unable to retrieve data from {url}')
            return None

    def get_user_papers(self, user_id, limit=None):
        papers = self.get_scholar_papers(user_id, limit)
        if papers:
            return {
                "user_id": user_id,
                "user_scholar_url": self.user_scholar_url,
                "papers": papers
            }
        else:
            return {"error": f"Unable to retrieve papers for user {user_id}"}
