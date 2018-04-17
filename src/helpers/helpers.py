import os
import shutil

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
        for i in emails_repos:
            print(i)

