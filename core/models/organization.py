class Organization:

    def __init__(self, name, email, blog, repositories, members):
        self.name = name
        self.email = email
        self.blog = blog
        self.repositories = repositories
        self.members = members

    def __str__(self):
        final = "Org Name: {}".format(self.name)
        if self.email:
            final = "{} ({})".format(final, self.email)
        if self.members:
            final = "{} ({} Members)".format(final, len(self.members))
        if self.blog:
            final = "{} - {}".format(final, self.blog)
        if self.repositories:
            for repo in self.repositories:
                final = "{}\n{}".format(final, repo.__str__())
        return final

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
