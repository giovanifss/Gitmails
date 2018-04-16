import os
import argparse
from src.gitmails import Gitmails

parser = argparse.ArgumentParser(prog="bla", description="Analyze git repositories for unique emails")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-u", "--username", help="The username of the user")
group.add_argument("-r", "--repository", help="The link to a repository")
parser.add_argument("-p", "--path", help="Path to a temporary directory", default="/tmp/gitmails")
parser.add_argument("--include-forks", help="Include forked repositories", action="store_true")

args = parser.parse_args()
if args.username:
    args.path = "{}/{}".format(args.path, args.username)

def updater(m,plugin):
    try:
        plugin = "{}Collector".format(plugin.capitalize())
        result = Gitmails(args, getattr(m,plugin)(args.username))
        if result:
            print("\nUnique emails in git history:")
            for i in result:
                print("\t{}".format(i))
    except Exception as e:
        print(str(e),plugin)

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)
    files = os.listdir('src/plugins')
    plugins = [plugin for plugin in files if '__' not in plugin]
    plugins = [plugin.replace('.py','') for plugin in plugins if '.pyc' not in plugin]
    for plugin in plugins:
        m = __import__ ('src.plugins.%s' % (plugin),fromlist=[plugin])
        updater(m, plugin)

if __name__ == '__main__':
    main()
