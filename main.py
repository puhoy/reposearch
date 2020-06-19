import datetime
import json
from typing import List
from urllib.parse import urljoin

import click
import humanize
import iso8601
import requests

from search_interfaces._search_interface import SearchResult
from search_interfaces.gitea import GiteaSearch
from search_interfaces.github import GitHubSearch
from search_interfaces.gitlab import GitLabSearch


@click.group()
def cli():
    pass


@cli.command()
@click.argument('terms', nargs=-1)
def search(terms):
    results: List[SearchResult] = []
    for forge in forges.values():
        results += forge.search(keywords=terms)
    results = sorted(results, key=lambda r: r.last_commit, reverse=True)
    click.echo_via_pager('\n'.join([result.print() for result in results]))


forges = {
    'github.com': GitHubSearch(),
    'bitbucket.com': GitLabSearch('https://gitlab.com', api_token='G3gsxHg73wydwTMyFYWx'),
    'codeberg.org': GiteaSearch('https://codeberg.org')
}

if __name__ == '__main__':
    cli()
