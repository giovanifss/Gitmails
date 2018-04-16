import os
from random import randint
from src.helpers.helpers import Helpers
from pygit2 import Repository, GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE, clone_repository

class Gitmails(object):
    def __new__(self, args, repositories):
        self.helper = Helpers()
        self.helper.ensure_dir(args.path)
        os.chdir(args.path)
        self.clone_repositories(self, args.path, repositories)
        emails = self.get_emails(self, args.path)
        self.helper.cleanup(args.path)
        return emails

    def clone_repositories(self, path, repositories):
        i = randint(0,100000)
        for repo in repositories:
            print("Clonning: " + repo)
            clone_repository(repo, ('{}/{}'.format(path, str(i))), bare=True)
            i = randint(0,100000)

    def get_emails(self, path):
        result = set()
        for item in os.listdir(path):
            if os.path.isdir(os.path.join(path, item)):
                repo = Repository(os.path.join(path, item))
                for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
                    result.add(commit.author.name + " - " + commit.author.email)
        return result
