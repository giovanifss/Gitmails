class Collector():

    def __init__(self, args):
        raise NotImplementedError

    def collect_user(self):
        raise NotImplementedError

    def collect_organization(self):
        raise NotImplementedError

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
