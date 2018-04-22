from multiprocessing import Pool
from core.models.author import Author
from core.utils.helpers import Helpers
from pygit2 import Repository, GIT_SORT_TOPOLOGICAL, clone_repository

class GitUtils:
    def __init__(self, args):
        self.args = args

    def get_authors(self, repos):
        Helpers().ensure_dir(self.args.path)
        p = Pool()
        p.map(self.clone_repo, repos)
        results = p.map(self.get_repo_authors, repos)
        for i in results:
            if i:
                [Helpers().get_by_identifier(repos, repo_id).set_authors(authors) for repo_id, authors in i.items()]
        if not self.args.no_cleanup:
            Helpers().cleanup(self.args.path)
        return True

    def get_repo_authors(self, repository):
        try:
            authors_set = set()
            repo = Repository(self.get_repo_path(repository))
            for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
                authors_set.add(Author(commit.author.name, commit.author.email))
            return {repository.identifier:authors_set}
        except Exception as e:
            print(e)
            return False

    def clone_repo(self, repo):
        try:
            clone_repository(repo.url, self.get_repo_path(repo), bare=True)
            return True
        except Exception as e:
            print(e)
            return False

    def get_repo_path(self, repository):
        return "{}/{}/{}".format(self.args.path, repository.url.lstrip("https://www.").split('/')[0], "".join(repository.name.split()))
