from core.plugins.hibp import HIBP
from core.utils.helpers import Helpers
from core.utils.printer import Printer
from core.collectors.github import GithubCollector
from core.collectors.gitlab import GitlabCollector
from core.collectors.bitbucket import BitbucketCollector

class Gitmails:
    def __init__(self, args):
        self.args = args
        self.collectors = self.get_collectors()

    def execute(self):
        collected = self.collect(self.get_collectors())
        Printer(self.args).print(collected)
        self.apply_plugins(self.get_plugins(), collected)
        return collected

    def collect(self, collectors):
        collected = []
        if self.args.username:
            collected = self.collect_users(self.args.username, collectors)
        elif self.args.organization:
            collected = self.collect_organizations(self.args.organization, collectors)
        else:
            pass
        if not collected:
            Helpers().print_error("gitmails: Could not collect any information")
            return False
        return collected

    def collect_users(self, username, collectors):
        result = []
        for c in collectors:
            user = c.collect_user(username)
            if user:
                result.append(user)
                continue
            Helpers().print_error("gitmails: Could not collect user information")
        return result

    def collect_organizations(self, organization, collectors):
        result = []
        for c in collectors:
            org = c.collect_organization(organization)
            if org:
                result.append(org)
                continue
            Helpers().print_error("gitmails: Could not collect organization information")
        return result

    def get_collectors(self):
        collectors = []
        if not self.args.no_github:
            collectors.append(GithubCollector(self.args))
        if not self.args.no_gitlab:
            collectors.append(GitlabCollector(self.args))
        if not self.args.no_bitbucket:
            collectors.append(BitbucketCollector(self.args))
        return collectors

    def apply_plugins(self, plugins, collected):
        for p in plugins:
            p.execute(collected)

    def get_plugins(self):
        return [HIBP(self.args)]
