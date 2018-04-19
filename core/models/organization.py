class Organization:
    def __init__(self, name, email, blog, repositories, members):
        self.name = name
        self.email = email
        self.blog = blog
        self.repositories = repositories
        self.members = members

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
