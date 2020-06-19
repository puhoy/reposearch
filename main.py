from typing import List

import click

from search_interfaces._search_interface import SearchResult
from search_interfaces.gitea import GiteaSearch
from search_interfaces.github import GitHubSearch
from search_interfaces.gitlab import GitLabSearch


@click.group()
def cli():
    pass


@cli.command()
@click.argument('terms', nargs=-1)
@click.option('--platform', default=None)
def search(terms, platform):
    results: List[SearchResult] = []
    if platform:
        platforms = [platforms_by_name.get(platform, None)]
        if not platforms:
            click.echo(f'please choose from {", ".join(platforms_by_name.keys())}')
    else:
        platforms = platforms_by_name.values()

    # todo: make async
    for forge in platforms:
        results += forge.search(keywords=terms)

    # todo:
    # sort by latest_commit, project age, levenshtein distance to repo_name, open_issues, open_prs
    # filter is_fork, archived, is_private
    results = sorted(results, key=lambda r: r.last_commit, reverse=True)
    click.echo_via_pager('\n'.join([result.print() for result in results]))


platforms_by_name = {
    'github.com': GitHubSearch(),
    'gitlab.org': GitLabSearch('https://gitlab.com', api_token='G3gsxHg73wydwTMyFYWx'),
    'codeberg.org': GiteaSearch('https://codeberg.org'),
    'git.spip.net': GiteaSearch('https://git.spip.net'),
    'gitea.com': GiteaSearch('https://gitea.com'),
    'git.teknik.io': GiteaSearch('https://git.teknik.io'),
    'opendev.org': GiteaSearch('https://opendev.org'),
    'gitea.codi.coop': GiteaSearch('https://gitea.codi.coop'),
    'git.osuv.de': GiteaSearch('https://git.osuv.de'),
    'git.koehlerweb.org': GiteaSearch('https://git.koehlerweb.org'),
    'gitea.vornet.cz': GiteaSearch('https://gitea.vornet.cz'),
    'git.luehne.de': GiteaSearch('https://git.luehne.de'),
    'djib.fr': GiteaSearch('https://djib.fr'),
    'code.antopie.org': GiteaSearch('https://code.antopie.org'),
    'git.daiko.fr': GiteaSearch('https://git.daiko.fr'),
    'gitea.anfuchs.de': GiteaSearch('https://gitea.anfuchs.de'),
    'git.sablun.org': GiteaSearch('https://git.sablun.org'),
    'git.jcg.re': GiteaSearch('https://git.jcg.re'),
    #'bitbucket.com': BitBucketSearch('search_user','Hd8UVCbbf8szbhYeqtdx')
}

if __name__ == '__main__':
    cli()
