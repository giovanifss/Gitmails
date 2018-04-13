import os
import argparse
import requests
import shutil
from pygit2 import Repository, GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE, clone_repository
from subprocess import call, STDOUT

parser = argparse.ArgumentParser(prog="bla", description="Analyze git repositories for unique emails")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-u", "--username", help="The username of the user")
group.add_argument("-r", "--repository", help="The link to a repository")
parser.add_argument("-p", "--path", help="Path to a temporary directory", default="/tmp/gitmail")
parser.add_argument("--github", help="Analyze Github repositories", action="store_true")
parser.add_argument("--gitlab", help="Analyze Gitlab repositories", action="store_true")
parser.add_argument("--bitbucket", help="Analyze BitBucket repositories", action="store_true")
parser.add_argument("--include-forks", help="Include forked repositories", action="store_true")
args = parser.parse_args()

def ensure_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def flatten(l):
    return [item for sublist in l for item in sublist]

def collect_github(username, include_forks):
    repositories = []
    for repository in requests.get('https://api.github.com/users/' + username + '/repos').json():
        if not repository['fork'] and not include_forks:
            if 'clone_url' in repository:
                repositories.append(repository['clone_url'])
    return repositories

def collect_gitlab(username):
    repositories = []
    for repository in requests.get('https://gitlab.com/api/v4/users/' + username + '/projects').json():
        if 'web_url' in repository:
            repositories.append(repository['web_url'])
    return repositories

def collect_bitbucket(username):
    repositories = []
    for repository in requests.get("https://api.bitbucket.org/2.0/repositories/" + username).json()['values']:
        if 'links' in repository:
            if 'clone' in repository['links']:
                repositories.append(repository['links']['clone'][0]['href'])
    return repositories

def collect_repositories(args):
    repositories = []
    if args.github:
        repositories.append(collect_github(args.username, args.include_forks))
    if args.gitlab:
        repositories.append(collect_gitlab(args.username))
    if args.bitbucket:
        repositories.append(collect_bitbucket(args.username))
    return flatten(repositories)

def clone_repositories(repositories):
    i = 0
    for repo in repositories:
        print("Clonning: " + repo)
        clone_repository(repo, (args.path + "/" + str(i)), bare=True)
        i += 1

def get_emails(path):
    result = set()
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(args.path, item)):
            repo = Repository(os.path.join(args.path, item))
            for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
                result.add(commit.author.name + " - " + commit.author.email)
    return result

def main():
    ensure_dir(args.path)
    repos = [args.repository] if args.username == None else collect_repositories(args)
    clone_repositories(repos)
    for i in get_emails(args.path):
        print(i)
    shutil.rmtree(args.path, ignore_errors=True)

if __name__ == "__main__":
    main()
