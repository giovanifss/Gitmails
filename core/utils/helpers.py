import os
import re
import sys
import shutil
import requests
from core.models.author import Author


class Helpers:

    @classmethod
    def request(self, url, method="get", accepts=[200], headers=None, data=None):
        action = getattr(requests, method)
        try:
            result = action(url, headers=headers, data=data)
            if result.text and result.status_code in accepts:
                return result.json()

            elif method == "head":
                return result

            return self.analyze_request(result)

        except Exception as e:
            self.print_error(e)
            return False

    @classmethod
    def analyze_request(self, request):
        try:
            self.print_error(
                "gitmails: {} [{}]: {}".format(
                    request.url,
                    request.status_code,
                    request.json()["message"].split("(")[0].rstrip(),
                )
            )
        except Exception as e:
            self.print_error(
                "gitmails: {} [{}]".format(request.url, request.status_code)
            )
        return False

    @classmethod
    def get_last_page(self, url):
        try:
            result = self.request(url, method="head")
            last_url = re.findall(
                "https?://(?:[-\w.]|(?:%[\da-fA-F]{2})).+?(?=>)", result.headers["Link"]
            )[
                -1
            ]
            return int(last_url.split("=")[-1])

        except Exception as e:
            # self.print_error(e)
            return 0

    @classmethod
    def flatten(self, lst):
        result = []
        if lst:
            for sublist in lst:
                if sublist:
                    for item in sublist:
                        result.append(item)
        return result

    @classmethod
    def get_by_identifier(self, repos, repo_id):
        for repository in repos:
            if repository.identifier == repo_id:
                return repository

        return False

    @classmethod
    def parse_git_author(self, string):
        if string:
            splitted = string.split("<")
            return Author(splitted[0].rstrip(), splitted[1].rstrip(">"))

        return False

    @classmethod
    def print_error(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    @classmethod
    def print_warning(self, string, jumpline=False):
        result = "[!] {}".format(string)
        if jumpline:
            result = "\n{}".format(result)
        print(result)

    @classmethod
    def print_success(self, string, jumpline=False):
        result = "[+] {}".format(string)
        if jumpline:
            result = "\n{}".format(result)
        print(result)

    @classmethod
    def ensure_dir(self, file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    @classmethod
    def cleanup(self, path):
        shutil.rmtree(path, ignore_errors=True)

    @classmethod
    def write_authors_file(self, filename, authors):
        with open(filename, "w") as f:
            print("\n[!] Writing results to file {}".format(filename))
            for a in authors:
                f.write("{},{}\n".format(a.name, a.email))
