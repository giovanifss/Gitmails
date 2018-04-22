import os
import re
import sys
import shutil
import requests
from core.models.author import Author

class Helpers:
    def request(self, url, method="get", accepts=[200], headers=None, data=None):
        action = getattr(requests, method)
        try:
            result = action(url, headers=headers, data=data)
            if result.text and result.status_code in accepts:
                return result.json()
            return result
        except Exception as e:
            self.print_error(e)
            return False

    def get_last_page(self, url):
        try:
            result = self.request(url, method="head")
            last_url = re.findall("https?://(?:[-\w.]|(?:%[\da-fA-F]{2})).+?(?=>)", result.headers["Link"])[-1]
            return int(last_url.split('=')[-1])
        except Exception as e:
            #self.print_error(e)
            return 0

    def flatten(self, lst):
        if not lst:
            return []
        else:
            return [item for sublist in lst for item in sublist]

    def get_by_identifier(self, repos, repo_id):
        for repository in repos:
            if repository.identifier == repo_id:
                return repository
        return False

    def parse_git_author(self, string):
        if string:
            splitted = string.split('<')
            return Author(splitted[0].rstrip(), splitted[1].rstrip('>'))
        return False

    def print_error(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    def ensure_dir(self, file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    def cleanup(self, path):
        shutil.rmtree(path, ignore_errors=True)
