import os
import shutil
from tabulate import tabulate

class Helpers(object):
    def ensure_dir(self, file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    def cleanup(self, path):
        shutil.rmtree(path, ignore_errors=True)

    def flatten(self, lst):
        if not lst:
            return []
        else:
            return [item for sublist in lst for item in sublist]

    def print_verbose_emails(self, emails_repos):
        for email, repositories in emails_repos.items():
            print("\n\n{} found in:".format(email))
            for i in repositories:
                print("\t{}".format(i))

    def print_emails(self, emails_repos):
        data = [i for i in emails_repos]
        email = [d.split(' - ') for d in data]
        print(tabulate(email,["Name","Email"],"fancy_grid"))

    def print_raw_emails(self, emails_repos):
        data = [i for i in emails_repos]
        email = [d.replace(' - ', ',') for d in data]
        for i in email:
            print(i)

    def print_to_file(self, emails_repos, file_name):
        data = [i for i in emails_repos]
        email = [d.replace(' - ', ',') for d in data]
        with open(file_name, 'a') as f:
            for i in email:
                f.write(i + "\n")
