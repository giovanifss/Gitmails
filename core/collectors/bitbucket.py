from core.models.user import User
from core.utils.git import GitUtils
from core.utils.helpers import Helpers
from core.models.collector import Collector
from core.models.repository import Repository
from core.models.organization import Organization


class BitbucketCollector(Collector):

    def __init__(self, args):
        self.args = args
        self.collector_name = "bitbucket"
        self.base_url = "https://api.bitbucket.org/2.0"

    def collect_user(self, username):
        Helpers.print_success(
            "Collecting information of {} in Bitbucket".format(username)
        )
        url = "{}/users/{}".format(self.base_url, username)
        result = Helpers.request(url)
        if result:
            repos = self.collect_repositories(
                "{}/repositories/{}".format(self.base_url, username)
            )
            return User(
                result["username"],
                result["display_name"],
                None,
                result["website"],
                repos,
            )

        return False

    def collect_organization(self, organization):
        Helpers.print_success(
            "Collecting information of {} in Bitbucket".format(organization)
        )
        url = "{}/teams/{}".format(self.base_url, organization)
        result = Helpers.request(url)
        if result:
            repos = self.collect_repositories(
                "{}/teams/{}/repositories".format(self.base_url, organization)
            )
            return Organization(
                result["display_name"], None, result["website"], repos, None
            )

        return False

    def collect_repositories(self, repos_url):
        repos = []
        if self.args.verbose:
            Helpers.print_success("Collecting repositories")
        result = Helpers.request(repos_url)
        repos.append(self.parse_repositories(result["values"]) if result else [])
        while "next" in result:
            result = Helpers.request(result["next"])
            repos.append(self.parse_repositories(result["values"]) if result else [])
        repos = Helpers.flatten(repos)
        if not self.args.api:
            self.set_authors(repos)
        return repos

    def set_authors(self, repos):
        if self.args.verbose:
            Helpers.print_success("Collecting authors")
        return GitUtils(self.args).set_repos_authors(repos)

    def parse_repositories(self, request_result):
        repos = []
        if request_result:
            for repo in request_result:
                authors = None
                if self.args.api:
                    authors = self.get_contributors(repo["links"]["commits"]["href"])
                repos.append(
                    Repository(
                        repo["uuid"],
                        repo["name"],
                        repo["links"]["clone"][0]["href"],
                        authors,
                    )
                )
        return repos

    def get_contributors(self, commit_url):
        authors = []
        result = Helpers.request(commit_url)
        authors.append(self.parse_commits(result["values"]) if result else [])
        while "next" in result:
            result = Helpers.request(result["next"])
            authors.append(self.parse_commits(result["values"]) if result else [])
        return Helpers.flatten(authors)

    def parse_commits(self, request_result):
        return set(
            [
                Helpers.parse_git_author(commit["author"]["raw"])
                for commit in request_result
                if request_result
            ]
        )

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
