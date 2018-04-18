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
        if not self.verbose:
            print("[+] Clonning repositories... (This process can take a while)")
        p = Pool()
        results = p.map(self.clone_repositories, repositories)
        if results:
            self.repo_paths = {k: v for d in results for k, v in d.items()}
            print("[+] Collecting emails...")
            emails = self.get_emails()
            if args.include_repositories:
                self.helper.print_verbose_emails(emails)
            elif args.raw:
                self.helper.print_raw_emails(emails)
            else:
                self.helper.print_emails(emails)
            if args.file:
                self.helper.print_to_file(emails, args.file)
            if not args.no_cleanup:
                self.helper.cleanup(args.path)

    def clone_repositories(self, repository):
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
            print(e)
            print("gitmails: Could not clone " + repository)
            return False

    def get_emails(self):
        emails = {}
        for repository, path in self.repo_paths.items():
            result = set()
            repo = Repository(path)
            try:
                for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
                    result.add("{} - {}".format(commit.author.name, commit.author.email))
                for i in result:
                    if i in emails:
                        emails[i] = emails[i] + [repository]
                    else:
                        emails[i] = [repository]
            except Exception as e:
                print("gitmails: Could not collect emails for {}".format(repository))
            result = set()
        return emails
