from iso8601 import iso8601

from search_interfaces._search_interface import SearchInterface, SearchResult


class GitLabSearchResult(SearchResult):
    def __init__(self, search_result_item):
        repo_name = search_result_item['name']
        owner_name = search_result_item['namespace']['path']
        repo_description = search_result_item.get('description', '?') or '?'
        last_commit = iso8601.parse_date(search_result_item['last_activity_at'])
        language = '?'
        license = '?'

        html_url = search_result_item['http_url_to_repo']

        super().__init__(repo_name, repo_description, html_url, owner_name, last_commit, language, license)


class GitLabSearch(SearchInterface):
    def __init__(self, base_url, api_token):
        super().__init__(base_url=base_url, search_path='/api/v4/search')
        self.api_token = api_token

    def search(self, keywords: list = [], tags: dict = {}):
        tags = {**tags, **dict(scope='projects')}
        params = dict(
            search='+'.join(keywords)
            , **tags)
        response = self.requests.get(self.request_url, params=params, headers={'PRIVATE-TOKEN': self.api_token})

        result = response.json()
        results = [GitLabSearchResult(item) for item in result]
        return results
