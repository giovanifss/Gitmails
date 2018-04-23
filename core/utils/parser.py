from core.utils.helpers import Helpers

class Parser:
    def __init__(self, args):
        self.args = args

    def get_authors(self, target):
        authors = []
        for repo in target.repositories:
            authors.append(repo.authors)
        return set(Helpers().flatten(authors))
