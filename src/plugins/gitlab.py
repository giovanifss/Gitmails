import requests

class GitlabCollector(object):
    def __new__(self, username):
        self.repositories = []
        try:
            self.result = requests.get('https://gitlab.com/api/v4/users/' + username + '/projects').json()
            for repository in self.result:
                if 'web_url' in repository:
                    self.repositories.append(repository['web_url'])
            return self.repositories
        except Exception as e:
            print("Could not collect gitlab repositories")
            return False

