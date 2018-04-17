import re
import requests
from src.helpers.helpers import Helpers

class GithubCollector(object):
    def __new__(self, username):
        self.repositories = []
        self.helper = Helpers()
        github_url = 'https://api.github.com/users/' + username + '/repos'
        last_page = self.get_last_page(self, github_url)
        if last_page:
            for i in range(1, (last_page + 1)):
                repos = self.get_repositories(self, github_url + "?page=" + str(i))
                if repos:
                    self.repositories.append(repos)
        return self.helper.flatten(self.repositories)

    def get_last_page(self, url):
        try:
            r = requests.head(url)
            last_url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2})).+?(?=>)', r.headers['Link'])[-1]
            return int(last_url.split('=')[-1])
        except Exception as e:
            return 1

    def get_repositories(self, url):
        repositories = []
        try:
            result = requests.get(url).json()
            for repository in result:
                if 'fork' in repository and not repository['fork'] and 'clone_url' in repository:
                    repositories.append(repository['clone_url'])
            return repositories
        except Exception as e:
            print("Could not collect github repositories")
            return False
