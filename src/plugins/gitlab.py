import requests

class GitlabCollector(object):
    def __new__(self, args):
        self.repositories = []
        if args.username:
            url = 'https://gitlab.com/api/v4/users/{}/projects'.format(args.username)
        if args.organization:
            url = 'https://gitlab.com/api/v4/groups/{}/projects'.format(args.organization)
        try:
            self.result = requests.get(url).json()
            for repository in self.result:
                if 'web_url' in repository:
                    self.repositories.append(repository['web_url'])
            return self.repositories
        except Exception as e:
            print("gitmails: Could not collect gitlab repositories")
            return False

