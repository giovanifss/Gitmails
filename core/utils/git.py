from multiprocessing import Pool
from core.models.author import Author
from core.utils.helpers import Helpers
from pygit2 import Repository, GIT_SORT_TOPOLOGICAL, clone_repository


class GitUtils:

    def __init__(self, args):
        self.args = args
        Helpers.ensure_dir(self.args.path)

    def get_repo_authors_by_url(self, repo_url):
        Helpers.print_success("Clonning {}".format(repo_url))
        self.clone_repo_by_url(repo_url)
        return self.get_authors(self.get_repo_path_by_url(repo_url))

    def set_repos_authors(self, repos):
        p = Pool()
        p.map(self.clone_repo, repos)
        Helpers.print_success("Collecting authors of repositories")
        results = p.map(self.get_repo_authors, repos)
        for i in results:
            if i:
                [
                    Helpers.get_by_identifier(repos, repo_id).set_authors(authors)
                    for repo_id, authors in i.items()
                ]
        return True

    def get_repo_authors(self, repository):
        authors = self.get_authors(self.get_repo_path(repository))
        return {repository.identifier: authors}

    def get_authors(self, repo_path):
        try:
            if self.args.verbose:
                Helpers.print_success("Collecting authors in {}".format(repo_path))
            authors_set = set()
            repo = Repository(repo_path)
            for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
                authors_set.add(Author(commit.author.name, commit.author.email))
            return authors_set

        except Exception as e:
            Helpers.print_error("{}: Could not collect authors".format(repo_path))
            return None

    def clone_repo(self, repo):
        try:
            if self.args.verbose:
                Helpers.print_success("Clonning {}".format(repo.url))
            clone_repository(repo.url, self.get_repo_path(repo), bare=True)
            return True

        except ValueError as e:
            return False

        except Exception as e:
            Helpers.print_error(e)
            return False

    def clone_repo_by_url(self, repo_url):
        try:
            clone_repository(repo_url, self.get_repo_path_by_url(repo_url), bare=True)
            return True

        except Exception as e:
            Helpers.print_error(e)
            return False

    def get_repo_path(self, repository):
        return "{}/{}/{}".format(
            self.args.path,
            self.get_domain(repository.url),
            "".join(repository.name.split()),
        )

    def get_repo_path_by_url(self, repo_url):
        return "{}/{}/{}".format(
            self.args.path, self.get_domain(repo_url), self.get_repo_name(repo_url)
        )

    def get_domain(self, repo_url):
        return repo_url.lstrip("https://www.").split("/")[0]

    def get_repo_name(self, repo_url):
        return repo_url.lstrip("https://www.").split("/")[2]
