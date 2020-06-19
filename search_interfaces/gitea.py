from iso8601 import iso8601

from search_interfaces._search_interface import SearchInterface, SearchResult


# https://try.gitea.io/api/swagger#/repository/repoSearch

class GiteaSearchResult(SearchResult):
    """
    {
      "allow_merge_commits": true,
      "allow_rebase": true,
      "allow_rebase_explicit": true,
      "allow_squash_merge": true,
      "archived": true,
      "avatar_url": "string",
      "clone_url": "string",
      "created_at": "2020-06-19T14:42:45.957Z",
      "default_branch": "string",
      "description": "string",
      "empty": true,
      "external_tracker": {
        "external_tracker_format": "string",
        "external_tracker_style": "string",
        "external_tracker_url": "string"
      },
      "external_wiki": {
        "external_wiki_url": "string"
      },
      "fork": true,
      "forks_count": 0,
      "full_name": "string",
      "has_issues": true,
      "has_pull_requests": true,
      "has_wiki": true,
      "html_url": "string",
      "id": 0,
      "ignore_whitespace_conflicts": true,
      "internal": true,
      "internal_tracker": {
        "allow_only_contributors_to_track_time": true,
        "enable_issue_dependencies": true,
        "enable_time_tracker": true
      },
      "mirror": true,
      "name": "string",
      "open_issues_count": 0,
      "open_pr_counter": 0,
      "original_url": "string",
      "owner": {
        "avatar_url": "string",
        "created": "2020-06-19T14:42:45.957Z",
        "email": "user@example.com",
        "full_name": "string",
        "id": 0,
        "is_admin": true,
        "language": "string",
        "last_login": "2020-06-19T14:42:45.957Z",
        "login": "string"
      },
      "permissions": {
        "admin": true,
        "pull": true,
        "push": true
      },
      "private": true,
      "release_counter": 0,
      "size": 0,
      "ssh_url": "string",
      "stars_count": 0,
      "template": true,
      "updated_at": "2020-06-19T14:42:45.957Z",
      "watchers_count": 0,
      "website": "string"
    }
    """

    def __init__(self, search_result_item):
        repo_name = search_result_item['name']
        owner_name = search_result_item['owner']['login']
        repo_description = search_result_item['description'] or '?'
        last_commit = iso8601.parse_date(search_result_item['updated_at'])
        language = '?'
        license_dict = search_result_item.get('license')
        license = license_dict.get('name', None) if license_dict else None

        html_url = search_result_item['html_url']

        super().__init__(repo_name, repo_description, html_url, owner_name, last_commit, language, license)


class GiteaSearch(SearchInterface):
    def __init__(self, base_url):
        super().__init__(base_url=base_url, search_path='api/v1/repos/search')

    def search(self, keywords: list = [], tags: dict = {}):
        params = dict(
            q='+'.join(keywords)
            , **tags)
        response = self.requests.get(self.request_url, params=params)

        result = response.json()
        results = [GiteaSearchResult(item) for item in result['data']]
        return results
