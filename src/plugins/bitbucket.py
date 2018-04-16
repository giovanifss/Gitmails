import requests

class BitbucketCollector(object):
    def __new__(self, username):
        self.repositories = []
        try:
            self.result = requests.get("https://api.bitbucket.org/2.0/repositories/" + username).json()
            if 'values' in self.result:
                for repository in self.result['values']:
                    if 'links' in repository and 'clone' in repository['links']:
                        self.repositories.append(repository['links']['clone'][0]['href'])
            return self.repositories
        except Exception as e:
            print("Could not collect bitbucket repositories")
            return False
