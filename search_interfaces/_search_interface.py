from datetime import datetime
from urllib.parse import urljoin

import click
import humanize
import requests


class SearchInterface:
    def __init__(self, base_url, search_path):
        self.base_url = base_url
        self.requests = requests.session()
        self.request_url = urljoin(self.base_url, search_path)

    def search(self, keywords: list, tags: dict):
        raise NotImplementedError


class SearchResult:
    def __init__(self, repo_name, repo_description, html_url, owner_name, last_commit, language=None, license=None):
        self.repo_name = repo_name
        self.repo_description = repo_description
        self.html_url = html_url
        self.owner_name = owner_name
        self.last_commit = last_commit
        self.language = language
        self.license = license

    def _append_to_print(self, text, key, value):
        text += click.style(key, bold=True)
        text += f'{value}\n'

    def print(self):
        self.last_commit = self.last_commit.replace(tzinfo=None)
        last_commit = humanize.naturaltime(self.last_commit)
        text = ''
        self._append_to_print(text, '', f'{self.owner_name}/{self.repo_name}')
        self._append_to_print(text, 'Last Commit:', last_commit)
        self._append_to_print(text, '-> ', self.html_url)
        self._append_to_print(text, 'Description: ', self.repo_description[:100])
        self._append_to_print(text, 'Language: ', self.language)
        self._append_to_print(text, '', '')
        return text