from core.models.user import User
from core.utils.helpers import Helpers
from core.models.collector import Collector
from core.models.repository import Repository
from core.models.organization import Organization

class GithubCollector(Collector):
    def __init__(self, args):
        self.args = args
        self.base_url = "https://api.github.com"

    def collect_user(self, username):
        url = "{}/users/{}".format(self.base_url, username)
        result = Helpers().request(url)
        if result:
            repos = self.collect_repositories("{}/repos".format(url))
            return User(result["login"], result["name"], result["email"], result["bio"])
        return False

    def collect_organization(self, organization):
        url = "{}/orgs/{}".format(self.base_url, organization)
        pass

    def collect_repositories(self, repos_url):
        repos = []
        last_page = Helpers().get_last_page(repos_url)
        last_range = last_range + 1 if last_range == 0 else last_range
        for i in range(1, (last_page + 1)):
            result = Helpers().request("{}?page={}".format(repos_url, last_page))
            repos.append([Repository(repo['clone_url'], None) for repo in result if result and not (repo['fork'] and not self.args.include_forks)])
        return Helpers().flatten(repos)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

