# reposearch

a cli tool to search for repositories across different code hosting platforms.

currently searches in these services:

    github.com (GitHub)
    gitlab.org (GitLab)
    codeberg.org (Gitea)
    git.spip.net (Gitea)
    gitea.com (Gitea)
    git.teknik.io (Gitea)
    opendev.org (Gitea)
    gitea.codi.coop (Gitea)
    git.osuv.de (Gitea)
    git.koehlerweb.org (Gitea)
    gitea.vornet.cz (Gitea)
    git.luehne.de (Gitea)
    djib.fr (Gitea)
    code.antopie.org (Gitea)
    git.daiko.fr (Gitea)
    gitea.anfuchs.de (Gitea)
    git.sablun.org (Gitea)
    git.jcg.re (Gitea)

## installation

    pip install git+https://github.com/puhoy/reposearch --user

## usage

    Usage: reposearch search [OPTIONS] TERMS...
    
    Options:
      --platform [github.com|gitlab.org|codeberg.org|git.spip.net|gitea.com|git.teknik.io|opendev.org|gitea.codi.coop|git.osuv.de|git.koehlerweb.org|gitea.vornet.cz|git.luehne.de|djib.fr|code.antopie.org|git.daiko.fr|gitea.anfuchs.de|git.sablun.org|git.jcg.re]
                                      limit search to a platform
      --sort [last_commit|created_at]
                                      sort results
      --reverse TEXT                  reverse sort order
      --help                          Show this message and exit.
    
