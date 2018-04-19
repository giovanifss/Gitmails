class User:
    def __init__(self, username, name, email, bio, repositories):
        self.username = username
        self.name = name
        self.email = email
        self.bio = bio
        self.repositories = repositories

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
