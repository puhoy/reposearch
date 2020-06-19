from iso8601 import iso8601

from search_interfaces._search_interface import SearchResult, SearchInterface


class GitHubSearchResult(SearchResult):
    def __init__(self, search_result_item):
        repo_name = search_result_item['name']
        owner_name = search_result_item['owner']['login']
        repo_description = search_result_item['description'] or '?'
        last_commit = iso8601.parse_date(search_result_item['updated_at'])
        language = search_result_item['language']
        license_dict = search_result_item.get('license')
        license = license_dict.get('name', None) if license_dict else None

        html_url = search_result_item['html_url']

        super().__init__(repo_name, repo_description, html_url, owner_name, last_commit, language, license)


class GitHubSearch(SearchInterface):
    # https://developer.github.com/v3/search/#search-repositories

    def __init__(self):
        super().__init__(base_url='https://api.github.com/', search_path='search/repositories')

    def search(self, keywords: list = [], tags: dict = {}):
        params = dict(
            q='+'.join(keywords)
            , **tags)
        response = self.requests.get(self.request_url, params=params)
        result = response.json()

        results = [GitHubSearchResult(item) for item in result['items']]
        return results
