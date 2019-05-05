<p align="center"><img src="https://s9.postimg.cc/70vgwyp73/LOGO_PROPOSAL_FOR_GITMAILS_9b.png"></p>

## Development - IMPORTANT
This Gitmails version is no longer maintained. Check out the [Gitmails Shell](https://github.com/giovanifss/Gitmails-sh)
port if you want to use a version that is maintained and, hopefully, developed.

If you do not want to use the shell port and prefer the Python version, feel free to fork Gitmails and direct it to
whenever path you see fit.

## Overview
Gitmails explores that git commits contains a name and an email configured by the author and that version control
host services are being used to store a lot of projects.

What Gitmails does is:
- Query the version control host services for information about an organization, team, group, user or single repository;
- List all repositories (restricted by authentication) if not on single repository mode;
- Clone the repository or query the version control host service for the commit history;
- Analyze the commit history to identify unique authors. Authors are defined by a name and email par.

With these steps, Gitmails can collect all emails found in commit history for a specific target.

## Usage
First, you must choose the operation method: collect emails of organization, user or single repository. This can be
done by the options: `-u  --username`, `-o  --organization` or `-r  --repository`.

After specifying the operation method, you must set the target. You should pass it right after the operation method:
`python3 gitmails.py -u some_username`, `python3 gitmails.py -o some_org` or `python3 gitmails.py -r some_repo_url`.
**NOTE**: gitlab usernames are case sensitive, keep that in mind when trying to collect emails there.

With this basic configuration, Gitmails will clone all repositories for the specified target (or clone the repository in
the url) and analyze its commit history. Then, it will print the high level information of the user or organization and
finally print, in a "fancy_grid" table (from tabulate), all the Name-Email pars found during analysis.

Useful options:
- `--raw`: Will print the results in pure text, no grids, just a comma separated values;
- `-f | --file`: Will store the result in the specified file. The results will be in csv with no header format.
- `--include-repositories`: Will make Gitmails print the result with information about in which repository the
email was found.
- `-p | --path`: Specify the temporary path to clone the repositories.
- `-e | --exclude`: Ignore specified repositories. Will compare the repository name, if it matches, will ignore
the repository and go to the next.
- `--no-cleanup`: Will not remove the clonned repositories.
- `--include-forks`: Will include forked repositories in the analysis (Only for github).
- `--include-users`: If collecting an organization, will collect info about its public members (Only for github).
- `--no-[gitlab|github|bitbucket]`: Will not collect information of the specified host service.
- `--run-plugins`: Will execute plugins in the collected result.
- `--api`: Will try to collect all the information only through API, without clonning repositories.
**NOTE**: Accessing APIs without authentication will cause your IP to be throttled. Also, API only collection is usually
slower than clonning the repositories.

## Installation
To install Gitmails, you will have to execute the following steps:
- `pip3 install -r requirements.txt`
- Install pygit2 through your operating system package manager.

#### Debian problems
If you are using Debian (maybe Ubuntu too), the libgit2 package do not work with Gitmails. To solve this, you will need
to compile the libgit2 manually. The following steps should enough:
```bash
wget https://github.com/libgit2/libgit2/archive/v0.27.0.tar.gz && \
      tar xzf v0.27.0.tar.gz && \
      cd libgit2-0.27.0/ && \
      cmake . && \
      make && \
      sudo make install
ldconfig
pip3 install pygit2
```
Or execute the [debian install](debian-install.sh) script.

## Docker
You can also use the docker version of the tool by issuing the following command:
- `docker run -it giovanifss/gitmails --help`

Note that if you want to write to a file, you will need to mount a docker volume:
- `docker run -v /tmp/output:/opt -it giovanifss/gitmails -f /opt/result.txt`

## Contributing
This project is no longer maintained. If you want to contribute check out [Gitmails Shell](https://github.com/giovanifss/Gitmails-sh).

## Disclaimer
This tool collects data that can be useful for legal offensive security jobs. The authors of this
project disclaims any and all responsibility for any damages or losses caused by misuse or malicious use of this tool.
Check [LICENSE](LICENSE) for more details.
