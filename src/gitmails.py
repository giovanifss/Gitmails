import os
from random import randint
from src.helpers.helpers import Helpers
from pygit2 import Repository, GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE, clone_repository

class Gitmails(object):
    def __new__(self, args, repositories):
        self.repo_paths = {}
        self.helper = Helpers()
        self.helper.ensure_dir(args.path)
        os.chdir(args.path)
        self.clone_repositories(self, args.path, repositories)
        self.get_emails(self)
        self.helper.cleanup(args.path)

    def clone_repositories(self, path, repositories):
        for repo in repositories:
            print("Clonning: " + repo)
            repo_name = repo.lstrip('https://www.')
            repo_name = "{}/{}".format(repo_name.split('/')[0], repo_name.split('/')[-1])
            path = "{}/{}".format(path, repo_name)
            self.repo_paths[repo] = path
            clone_repository(repo, path, bare=True)

    def get_emails(self):
        result = set()
        for repository, path in self.repo_paths.items():
            repo = Repository(path)
            print("Unique emails in {}:".format(repository))
            for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
                result.add(commit.author.name + " - " + commit.author.email)
            for i in result:
                print("\t{}".format(i))
            result = set()
