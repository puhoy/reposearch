from concurrent import futures
from typing import List

import click

from config.platforms import platforms_by_name
from reposearch.search_interfaces._search_interface import SearchResult, SearchInterface


def fetch_concurrently(keywords, platforms: List[SearchInterface]):
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


@click.group()
def cli():
    pass


@cli.command()
def list_platforms():
    for platform_name, platform_search in platforms_by_name.items():
        click.echo(f'{platform_name} ({platform_search.name})')


@cli.command()
@click.argument('terms', nargs=-1, required=True)
@click.option('--platform', type=click.Choice(list(platforms_by_name.keys())), default=None, help='limit search to a platform')
@click.option('--sort', type=click.Choice(['last_commit', 'created_at']), default='last_commit', help='sort results')
@click.option('--reverse', default=True, help='reverse sort order')
def search(terms, platform, sort, reverse):
    if platform:
        platforms = [platforms_by_name.get(platform, None)]
        if not platforms:
            click.echo(f'please choose from {", ".join(platforms_by_name.keys())}')
    else:
        platforms = platforms_by_name.values()
    results: List[SearchResult]
    results, errors = fetch_concurrently(keywords=terms, platforms=platforms)

    # todo:
    # sort by levenshtein distance to repo_name, open_issues, open_prs
    # filter is_fork, archived, is_private
    if sort == 'last_commit':
        results = sorted(results, key=lambda r: r.last_commit, reverse=reverse)
    elif sort == 'created_at':
        results = sorted(results, key=lambda r: r.created_at, reverse=reverse)

    intro = f'showing results for {" ".join(terms)}'
    errors_formatted = '\n'.join(
        [click.style(f'could not get results from {base_url}: {error}\n', fg='red') for base_url, error in errors])
    results_formatted = '\n'.join([result.print() for result in results])

    click.echo_via_pager(f'{intro}\n\n{errors_formatted}\n{results_formatted}')


if __name__ == '__main__':
    cli()
