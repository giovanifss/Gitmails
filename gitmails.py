import sys
import argparse
from core.gitmails import Gitmails
from core.utils.helpers import Helpers

parser = argparse.ArgumentParser(
    prog="gitmails", description="Analyze git repositories for unique emails"
)
flow_group = parser.add_mutually_exclusive_group(required=True)
flow_group.add_argument(
    "-u", "--username", help="Username of the owner of the repositories"
)
flow_group.add_argument(
    "-r", "--repository", help="Direct link to a specific repository"
)
flow_group.add_argument(
    "-o", "--organization", help="Organization name owner of the repositories"
)
parser.add_argument(
    "-p", "--path", help="Path to a temporary directory", default="/tmp/gitmails"
)
parser.add_argument("-f", "--file", help="Output csv result to file")
parser.add_argument(
    "-e",
    "--exclude",
    nargs="+",
    help="Name of repositories to be excluded from analysis",
    default=[],
)
parser.add_argument(
    "--no-github", help="Do not collect Github information", action="store_true"
)
parser.add_argument(
    "--no-gitlab", help="Do not collect Gitlab information", action="store_true"
)
parser.add_argument(
    "--no-bitbucket", help="Do not collect Bitbucket information", action="store_true"
)
parser.add_argument(
    "--run-plugins", help="Run plugins in the collected result", action="store_true"
)
parser.add_argument(
    "--include-forks", help="Include forked repositories", action="store_true"
)
parser.add_argument(
    "--include-users",
    help="Collect information about organization members",
    action="store_true",
)
parser.add_argument(
    "--api",
    help="Collect commit emails through APIs when available. Avoid clonning repositories.",
    action="store_true",
)
parser.add_argument(
    "--no-cleanup",
    help="Do not delete the repositories after analysis",
    action="store_true",
)
parser.add_argument(
    "-v", "--verbose", help="Increase verbosity level", action="store_true"
)
print_group = parser.add_mutually_exclusive_group(required=False)
print_group.add_argument(
    "--raw", help="Print raw results separated by comma", action="store_true"
)
print_group.add_argument(
    "--include-repositories",
    help="Print emails and repositories relation",
    action="store_true",
)

args = parser.parse_args()


def main():
    collected = Gitmails(args).execute()
    if not args.no_cleanup:
        Helpers.cleanup(args.path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Helpers.cleanup(args.path)
        print("\nQuiting...")
        sys.exit(1)
