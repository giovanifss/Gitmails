import requests

class GithubCollector(object):
    def __new__(self, username):
        self.repositories = []
        try:
            self.result = requests.get('https://api.github.com/users/' + username + '/repos').json()
            for repository in self.result:
                if 'fork' in repository and not repository['fork'] and 'clone_url' in repository:
                    self.repositories.append(repository['clone_url'])
            return self.repositories
        except Exception as e:
            print("Could not collect github repositories")
            return False
