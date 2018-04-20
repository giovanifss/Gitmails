class Author:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return "\t{} - {}".format(self.name, self.email)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
