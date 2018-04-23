from tabulate import tabulate

class Printer:
    def __init__(self, args):
        self.args = args

    def print_organization(self, organization):
        pass

    def print_user(self, user):
        base = "{} ({})".format(user.name, user.username)
        if user.email:
            base = "{} - {}".format(base, user.email)
        print(base)
        if user.bio:
            print("Bio: {}".format(user.bio))
        self.print_repos(user.repositories)

    def print_repos(self, repos):
        for repo in repos:
            self.print_repo(repo)
            self.print_authors(repo.authors)

    def print_repo(self, repo):
        print("\n{} ({}):".format(repo.name, repo.url))

    def print_authors(self, authors, identation=0):
        authors_table = [[author.name, author.email] for author in authors]
        print(self.indent(tabulate(authors_table,["Name","Email"],"rst"), identation))

    def indent(self, txt, spaces=4):
        return "\n".join("{}{}".format(" "*spaces, ln) for ln in txt.splitlines())
