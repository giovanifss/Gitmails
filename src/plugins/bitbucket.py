import requests

class BitbucketCollector(object):
    def __new__(self, args):
        self.repositories = []
        if args.username:
            url = "https://api.bitbucket.org/2.0/repositories/{}".format(args.username)
        if args.organization:
            url = "https://api.bitbucket.org/2.0/teams/{}/repositories".format(args.organization)
        try:
            self.result = requests.get(url).json()
            if 'values' in self.result:
                for repository in self.result['values']:
                    if 'links' in repository and 'clone' in repository['links']:
                        self.repositories.append(repository['links']['clone'][0]['href'])
            return self.repositories
        except Exception as e:
            print("gitmails: Could not collect bitbucket repositories")
            return False
