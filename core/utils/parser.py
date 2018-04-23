from core.utils.helpers import Helpers

class Parser:
    def __init__(self, args):
        self.args = args

    def get_collected_authors(self, collection):
        all_authors = []
        for c in collection:
            all_authors.append(self.get_authors(c))
        return set(Helpers().flatten(all_authors))

    def all_unique_emails(self, collection):
        all_emails = []
        for c in collection:
            all_emails.append(self.unique_emails(c))
        return set(Helpers().flatten(all_emails))

    def unique_emails(self, target):
        emails = set()
        for repo in target.repositories:
            for author in repo.authors:
                emails.add(author.email)
        return emails

    def get_authors(self, target):
        authors = []
        for repo in target.repositories:
            authors.append(repo.authors)
        return set(Helpers().flatten(authors))
