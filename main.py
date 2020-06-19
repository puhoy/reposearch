from concurrent import futures
from typing import List

import click

from search_interfaces._search_interface import SearchResult, SearchInterface
from search_interfaces.gitea import GiteaSearch
from search_interfaces.github import GitHubSearch
from search_interfaces.gitlab import GitLabSearch


@click.group()
def cli():
    pass


def download(keywords, platforms: List[SearchInterface]):
    with futures.ThreadPoolExecutor(max_workers=20) as executor:
        to_do = []
        for platform in platforms:
            future = executor.submit(platform.search, keywords)
            to_do.append(future)

        results = []
        errors = []
        for future in futures.as_completed(to_do):
            success, base_url, result = future.result(timeout=5)
            if success:
                results += result
            else:
                errors.append((base_url, result))
        return results, errors


@cli.command()
@click.argument('terms', nargs=-1, required=True)
@click.option('--platform', default=None)
@click.option('--sort', type=click.Choice(['last_commit', 'created_at']), default='last_commit')
@click.option('--reverse', default=True)
def search(terms, platform, sort, reverse):
    if platform:
        platforms = [platforms_by_name.get(platform, None)]
        if not platforms:
            click.echo(f'please choose from {", ".join(platforms_by_name.keys())}')
    else:
        platforms = platforms_by_name.values()
    results: List[SearchResult]
    results, errors = download(keywords=terms, platforms=platforms)

    # todo:
    # sort by latest_commit, project age, levenshtein distance to repo_name, open_issues, open_prs
    # filter is_fork, archived, is_private
    if sort == 'last_commit':
        results = sorted(results, key=lambda r: r.last_commit, reverse=reverse)
    elif sort == 'created_at':
        results = sorted(results, key=lambda r: r.created_at, reverse=reverse)

    errors_formatted = '\n'.join([click.style(f'could not get results from {base_url}: {error}\n', fg='red') for base_url, error in errors])
    results_formatted = '\n'.join([result.print() for result in results])

    click.echo_via_pager(f'{errors_formatted}\n{results_formatted}')


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
    # 'bitbucket.com': BitBucketSearch('search_user','Hd8UVCbbf8szbhYeqtdx')
}

if __name__ == '__main__':
    cli()
