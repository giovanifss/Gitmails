class Repository:
    def __init__(self, identifier, url, authors):
        self.identifier = identifier
        self.url = url
        self.authors = authors

    def set_authors(self, authors):
        self.authors = authors

    def __str__(self):
        final = "\t{} (ID: {}):".format(self.url, self.identifier)
        for author in self.authors:
            final = "{}\n\t{}".format(final, author.__str__())
        return final

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
