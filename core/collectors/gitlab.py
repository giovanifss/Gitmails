from core.models.user import User
from core.models.author import Author
from core.models.collector import Collector
from core.models.organization import Organization

class GitlabCollector(Collector):
    def __init__(self, args):
        self.args = args
        self.base_url = "https://gitlab.com/api/v4"

    def collect_user(self, username):
        userid = self.get_userid(username)
        url = "{}/users/{}".format(self.base_url, userid)
        result = Helpers().request(url)
        if result:
            repos = self.collect_repositories("{}/users/{}/projects").format(url, userid)
            return User(result["username"], result["name"], None, result["bio"], repos)
        return False

    def collect_organization(self, organization):
        org = self.args.organization
        pass

    def collect_repositories(self, repos_url):
        result = Helpers().request(repos_url)
        reposids = [repo["id"] for repo in result if result]
        authors = [self.repository_collaborators(repoid) for repoid in reposids if reposids]
        if authors:
            # Identify unique authors
            pass
        return False

    def repository_collaborators(self, repoid):
        url = "{}/projects/{}/repository/contributors".format(self.base_url, repoid)
        result = Helpers().request(url)
        return [Author(contributor["name"], contributor["email"], [repoid]) for contributor in result if result]

    def get_userid(self, username):
        url = "{}/users?username={}".format(self.base_url, username)
        result = Helpers().request(url)
        if result:
            return result[0]["id"]
        return False

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
