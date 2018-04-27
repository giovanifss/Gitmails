class User:

    def __init__(self, username, name, email, bio, repositories):
        self.username = username
        self.name = name
        self.email = email
        self.bio = bio
        self.repositories = repositories

    def __str__(self):
        final = "Name: {} ({}):".format(self.name, self.username)
        if self.email:
            final = "{} ({})".format(final, self.email)
        if self.bio:
            final = "{} - {}".format(final, self.bio)
        if self.repositories:
            for repo in self.repositories:
                final = "{}\n{}".format(final, repo.__str__())
        return final

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
