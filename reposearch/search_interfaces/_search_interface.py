from datetime import datetime
from urllib.parse import urljoin

import click
import humanize
import requests


class SearchInterface:
    name = ''

    def __init__(self, base_url, search_path):
        self.base_url = base_url
        self.requests = requests.session()
        self.request_url = urljoin(self.base_url, search_path)

    def search(self, keywords: list, tags: dict):
        raise NotImplementedError


class SearchResult:
    def __init__(self, repo_name, repo_description, html_url, owner_name, last_commit, created_at, language=None, license=None):
        self.repo_name = repo_name
        self.repo_description = repo_description
        self.html_url = html_url
        self.owner_name = owner_name
        self.last_commit = last_commit
        self.created_at = created_at
        self.language = language
        self.license = license

        self.text = ''

    def _append_to_print(self, key, value):
        self.text += click.style(key, bold=True)
        self.text += f'{value}\n'

    def print(self):
        self.last_commit = self.last_commit.replace(tzinfo=None)
        self.created_at = self.created_at.replace(tzinfo=None)
        last_commit = humanize.naturaltime(self.last_commit)
        created_at = humanize.naturaltime(self.created_at)


        self._append_to_print(f'{self.owner_name} / {self.repo_name}', '')
        self._append_to_print('  Last commit: ', last_commit)
        self._append_to_print('  Created: ', created_at)
        self._append_to_print('  -> ', self.html_url)
        self._append_to_print('  Description: ', self.repo_description[:100])
        self._append_to_print('  Language: ', self.language)
        
        return self.text
