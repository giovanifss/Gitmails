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
            return User(result["login"], result["name"], result["email"], result["bio"], repos)
        return False

    def collect_organization(self, organization):
        url = "{}/orgs/{}".format(self.base_url, organization)
        result = Helpers().request(url)
        if result:
            members = self.collect_members("{}/members".format(url))
            repos = self.collect_repositories("{}/repos".format(url))
            return Organization(result["name"], result["email"], result["blog"], repos, members)
        pass

    def collect_members(self, members_url):
        members = []
        last_page = Helpers().get_last_page(members_url)
        last_page = last_page + 1 if last_page == 0 else last_page
        for i in range(1, (last_page + 1)):
            result = Helpers().request("{}?page={}".format(members_url, last_page))
            members.append(list(filter(bool, [self.collect_user(mem["login"]) for mem in result if result])))
        return Helpers().flatten(members)

    def collect_repositories(self, repos_url):
        repos = []
        last_page = Helpers().get_last_page(repos_url)
        last_page = last_page + 1 if last_page == 0 else last_page
        for i in range(1, (last_page + 1)):
            result = Helpers().request("{}?page={}".format(repos_url, last_page))
            repos.append(self.parse_repositories(result)) if result else []
        return Helpers().flatten(repos)

    def parse_repositories(self, request_result):
        return [Repository(repo["id"], repo["name"], repo["clone_url"], None) for repo in request_result if request_result and not (repo["fork"] and not self.args.include_forks)]

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

