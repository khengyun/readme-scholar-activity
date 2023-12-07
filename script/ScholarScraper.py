import time
from scholarly import scholarly

class ScholarScraper:
    def __init__(self):
        self.user_scholar_url = ""

    def get_scholar_papers(self, user_id, limit=None):
        search_query = scholarly.search_author_id(user_id)
        author = next(search_query, None)

        if author:
            papers = []

            for i, paper in enumerate(author.publications):
                if limit and i >= limit:
                    break

                title = paper.bib.get('title', 'N/A')
                authors = ', '.join(paper.bib.get('author', ['N/A']))
                citations = str(paper.citedby) if hasattr(paper, 'citedby') else 'N/A'
                year = str(paper.bib.get('year', 'N/A'))
                conference = paper.bib.get('journal', 'N/A')
                paper_url = paper.bib.get('url', 'N/A')
                abstract = paper.bib.get('abstract', 'N/A')

                paper_info = {
                    'Title': title,
                    'Authors': authors,
                    'Citations': citations,
                    'Year': year,
                    'Conference': conference,
                    'Paper_URL': paper_url,
                    'Abstract': abstract
                }

                papers.append(paper_info)

            return papers
        else:
            print(f'Error: Unable to retrieve data for user {user_id}')
            return None

    def get_user_papers(self, user_id, limit=None):
        papers = self.get_scholar_papers(user_id, limit)
        if papers:
            return {
                "user_id": user_id,
                "user_scholar_url": f'https://scholar.google.com/citations?user={user_id}&hl=en',
                "papers": papers
            }
        else:
            return {"error": f"Unable to retrieve papers for user {user_id}"}
