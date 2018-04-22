import sys
import argparse
from core.utils.printer import Printer
from core.utils.helpers import Helpers
from core.collectors.github import GithubCollector
from core.collectors.gitlab import GitlabCollector
from core.collectors.bitbucket import BitbucketCollector

parser = argparse.ArgumentParser(prog="gitmails", description="Analyze git repositories for unique emails")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-u", "--username", help="Username of the owner of the repositories")
group.add_argument("-r", "--repository", help="Direct link to a specific repository")
group.add_argument("-o", "--organization", help="Organization name owner of the repositories")
parser.add_argument("-p", "--path", help="Path to a temporary directory", default="/tmp/gitmails")
parser.add_argument("-v", "--verbose", help="Increase verbosity level", action="store_true")
parser.add_argument("--include-repositories", help="Print emails and repositories relation", action="store_true")
parser.add_argument("--include-forks", help="Include forked repositories", action="store_true")
parser.add_argument("--api", help="Collect commit emails through APIs when available", action="store_true")
parser.add_argument("--no-cleanup", help="Do not delete the repositories after analysis", action="store_true")
parser.add_argument("--raw", help="Print raw results separated by comma", action="store_true")
parser.add_argument("-f", "--file", help="Output csv result to file")

args = parser.parse_args()

def main():
    #github = GithubCollector(args)
    gitlab = GitlabCollector(args)
    #bitbucket = BitbucketCollector(args)
    user = gitlab.collect_user(args.username)
    Printer(args).print_repos(user.repositories)
    if not args.no_cleanup:
        Helpers().cleanup(args.path)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        Helpers().cleanup(args.path)
        print("\nQuiting...")
        sys.exit(1)
