from core.models.user import User
from core.utils.git import GitUtils
from core.utils.helpers import Helpers
from core.models.collector import Collector
from core.models.repository import Repository
from core.models.organization import Organization


class GithubCollector(Collector):

    def __init__(self, args):
        self.args = args
        self.collector_name = "github"
        self.base_url = "https://api.github.com"

    def collect_user(self, username, with_repositories=True):
        Helpers.print_success(
            "Collecting information of {} in Github".format(username)
        )
        url = "{}/users/{}".format(self.base_url, username)
        result = Helpers.request(url)
        if result:
            repos = None
            if with_repositories:
                repos = self.collect_repositories("{}/repos".format(url))
            return User(
                result["login"], result["name"], result["email"], result["bio"], repos
            )

        return False

    def collect_organization(self, organization):
        email = None
        blog = None
        name = None
        Helpers.print_success(
            "Collecting information of {} in Github".format(organization)
        )
        url = "{}/orgs/{}".format(self.base_url, organization)
        result = Helpers.request(url)
        if result:
            members = self.collect_members("{}/members".format(url))
            repos = self.collect_repositories("{}/repos".format(url))
            if "email" in result:
                email = result["email"]
            if "blog" in result:
                blog = result["blog"]
            if "name" in result:
                name = result["name"]
            else:
                name = result["login"]
            return Organization(name, email, blog, repos, members)

        pass

    def collect_members(self, members_url):
        members = []
        if self.args.verbose:
            Helpers.print_success("Collecting members")
        last_page = Helpers.get_last_page(members_url)
        last_page = last_page + 1 if last_page == 0 else last_page
        for i in range(1, (last_page + 1)):
            result = Helpers.request("{}?page={}".format(members_url, i))
            if result:
                if self.args.include_users:
                    members.append(
                        list(
                            filter(
                                bool,
                                [
                                    self.collect_user(
                                        mem["login"], with_repositories=False
                                    )
                                    for mem in result
                                ],
                            )
                        )
                    )
                else:
                    members.append(
                        [User(mem["login"], None, None, None, None) for mem in result]
                    )
        return Helpers.flatten(members)

    def collect_repositories(self, repos_url):
        repos = []
        if self.args.verbose:
            Helpers.print_success("Collecting repositories")
        last_page = Helpers.get_last_page(repos_url)
        last_page = last_page + 1 if last_page == 0 else last_page
        for i in range(1, (last_page + 1)):
            result = Helpers.request("{}?page={}".format(repos_url, i))
            repos.append(self.parse_repositories(result) if result else [])
        repos = Helpers.flatten(repos)
        self.collect_authors(repos)
        return repos

    def collect_authors(self, repos):
        if self.args.verbose:
            Helpers.print_success("Collecting authors")
        return GitUtils(self.args).set_repos_authors(repos)

    def parse_repositories(self, request_result):
        repos = []
        if request_result:
            for repo in request_result:
                if repo["name"] in self.args.exclude:
                    continue

                if not (repo["fork"] and not self.args.include_forks):
                    repos.append(
                        Repository(repo["id"], repo["name"], repo["clone_url"], None)
                    )
        return repos

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
