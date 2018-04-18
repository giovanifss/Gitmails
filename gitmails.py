import os
import sys
import argparse
from src.gitmails import Gitmails
from src.helpers.helpers import Helpers

parser = argparse.ArgumentParser(prog="bla", description="Analyze git repositories for unique emails")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-u", "--username", help="The username of the user")
group.add_argument("-r", "--repository", help="The link to a repository")
group.add_argument("-o", "--organization", help="The organization name")
parser.add_argument("-p", "--path", help="Path to a temporary directory", default="/tmp/gitmails")
parser.add_argument("-v", "--verbose", help="Print repositories information", action="store_true")
parser.add_argument("--include-forks", help="Include forked repositories", action="store_true")
parser.add_argument("--no-cleanup", help="Do not delete the repositories after analysis", action="store_true", default=False)

args = parser.parse_args()
if args.username:
    args.path = "{}/{}".format(args.path, args.username)
if args.repository:
    args.path = "{}/{}".format(args.path, args.repository.split('/')[3])
if args.organization:
    args.path = "{}/{}".format(args.path, args.organization)

def updater(m,plugin):
    try:
        plugin = "{}Collector".format(plugin.capitalize())
        hehe = getattr(m,plugin)(args.username)
        return hehe
    except Exception as e:
        print(str(e),plugin)

def main():
    repo_links = []
    if args.username:
        path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path)
        files = os.listdir('src/plugins')
        plugins = [plugin for plugin in files if '__' not in plugin]
        plugins = [plugin.replace('.py','') for plugin in plugins if '.pyc' not in plugin]
        for plugin in plugins:
            m = __import__ ('src.plugins.%s' % (plugin),fromlist=[plugin])
            repo_links.append(updater(m, plugin))
        repo_links = Helpers().flatten(repo_links)
    else:
        repo_links = [args.repository]
    if not repo_links:
        print("No repositories found")
    else:
        Gitmails(args, repo_links)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nQuiting...")
        Helpers().cleanup(args.path)
        sys.exit(0)
