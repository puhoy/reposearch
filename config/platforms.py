from reposearch.search_interfaces.gitea import GiteaSearch
from reposearch.search_interfaces.github import GitHubSearch
from reposearch.search_interfaces.gitlab import GitLabSearch

platforms_by_name = {
    'github.com': GitHubSearch(),
    'gitlab.org': GitLabSearch('https://gitlab.com',
                               api_token='G3gsxHg73wydwTMyFYWx'),  # new, empty user, read-only api
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
    'git.jcg.re': GiteaSearch('https://git.jcg.re')
}