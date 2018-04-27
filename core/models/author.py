class Author:

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return "\t{} - {}".format(self.name, self.email)

    def __key(self):
        return (self.name, self.email)

    def __eq__(self, other):
        return self.__key() == self.__key()

    def __hash__(self):
        return hash(self.__key())
