from core.models.user import User
from core.utils.helpers import Helpers
from core.models.collector import Collector
from core.models.repository import Repository
from core.models.organization import Organization

# Olhar api depois

class BitbucketCollector(Collector):
    def __init__(self, args):
        self.args = args
        self.base_url = "https://api.bitbucket.org/2.0"

    def collect_user(self, username):
        url = "{}/users/{}".format(self.base_url, username)
        result = Helpers().request(url)
        if result:
            repos = self.collect_repositories("{}/repositories/{}".format(self.base_url, username))
            return User(result["username"], result["display_name"], None, result["website"], repos)
        return False

    def collect_organization(self, organization):
        url = "{}/teams/{}".format(self.base_url, organization)
        result = Helpers().request(url)
        if result:
            repos = self.collect_repositories("{}/teams/{}/repositories".format(self.base_url, organization))
            return Organization(result["display_name"], None, result["website"], repos, None)
        return False

    def collect_repositories(self, repos_url):
        repos = []
        result = Helpers().request(repos_url)
        repos.append(self.parse_repositories(result["values"]) if result else [])
        while "next" in result:
            result = Helpers().request(result["next"])
            repos.append(self.parse_repositories(result["values"]) if result else [])
        return Helpers().flatten(repos)

    def parse_repositories(self, request_result):
        return [Repository(repo["uuid"], repo["name"], repo["links"]["clone"][0]["href"], None) for repo in request_result if request_result]

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
