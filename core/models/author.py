class Author:
    def __init__(self, name, email, repositories):
        self.name = name
        self.email = email
        self.repositories = repositories

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
