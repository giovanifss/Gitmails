class Repository:
    def __init__(self, url, authors):
        self.url = url
        self.authors = authors

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
