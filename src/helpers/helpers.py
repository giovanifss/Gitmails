import os
import shutil

class Helpers(object):
    def ensure_dir(self, file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    def cleanup(self, path):
        shutil.rmtree(path, ignore_errors=True)

    def print_emails(self, repo, emails):
        print("\nUnique emails found in {}".format(repo))
        for i in emails:
            print("\t{}".format(i))
        print("\n")
