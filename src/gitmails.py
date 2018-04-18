import os
from random import randint
from multiprocessing import Pool
from src.helpers.helpers import Helpers
from pygit2 import Repository, GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE, clone_repository

class Gitmails():
    def __init__(self, args, repositories):
        self.repo_paths = {}
        self.path = args.path
        self.verbose = args.verbose
        self.helper = Helpers()
        self.helper.ensure_dir(args.path)
        os.chdir(args.path)
        p = Pool()
        results = p.map(self.clone_repositories, repositories)
        self.repo_paths = {k: v for d in results for k, v in d.items()}
        if self.verbose:
            self.helper.print_verbose_emails(self.get_emails())
        else:
            print("Collecting emails...")
            self.helper.print_emails(self.get_emails())
        if not args.no_cleanup:
            self.helper.cleanup(args.path)

    def clone_repositories(self, repository):
        if not self.verbose:
            print("Clonning repositories..")
        try:
            if self.verbose:
                print("Clonning: " + repository)
            repo_name = repository.lstrip('https://www.')
            repo_name = "{}/{}".format(repo_name.split('/')[0], repo_name.split('/')[-1])
            p = "{}/{}".format(self.path, repo_name)
            clone_repository(repository, p, bare=True)
            self.repo_paths[repository] = p
            return self.repo_paths
        except Exception as e:
            if self.verbose:
                print("Could not clone " + repository)

    def get_emails(self):
        emails = {}
        for repository, path in self.repo_paths.items():
            result = set()
            repo = Repository(path)
            for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
                result.add(commit.author.name + " - " + commit.author.email)
            for i in result:
                if i in emails:
                    emails[i] = emails[i] + [repository]
                else:
                    emails[i] = [repository]
            result = set()
        return emails
