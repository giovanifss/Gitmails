from core.models.user import User
from core.models.collector import Collector
from core.models.organization import Organization

class GitlabCollector(Collector):
    def __init__(self, args):
        self.args = args
        self.base_url = "https://gitlab.com/api/v4/"

    def collect_user(self, username):
        pass

    def collect_organization(self, organization):
        org = self.args.organization
        pass

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
