from core.models.user import User
from core.models.collector import Collector
from core.models.organization import Organization

# Olhar api depois

class BitbucketCollector(Collector):
    def __init__(self, args):
        self.args = args
        self.base_url = "https://api.bitbucket.org/2.0"

    def collect_user(self, username):
        url = "{}/repositories/{}".format(self.base_url, username)
        pass

    def collect_organization(self, organization):
        url = "{}/teams/{}/repositories".format(self.base_url, username)
        pass

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
