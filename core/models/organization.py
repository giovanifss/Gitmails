class Organization:
    def __init__(self, repositories, collaborators):
        self.collaborators = collaborators
        self.repositories = repositories

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
