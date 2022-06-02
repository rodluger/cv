import urllib
from urllib.request import Request, urlopen
import json
import os
import sys


__all__ = ["get_all_stars"]


def get_all_repos(minstars=3, maxpages=10):
    params = []
    for user in ["rodluger", "showyourwork"]:
        for page in range(1, maxpages + 1):
            req = Request(
                "https://api.github.com/users/%s/repos?page=%d&per_page=100"
                % (user, page)
            )
            req.add_header("Accept", "application/vnd.github.v3.star+json")
            API_KEY = os.getenv("GH_API_KEY", None)
            if API_KEY is not None:
                req.add_header("Authorization", "token %s" % API_KEY)
            content = urlopen(req).read()
            par = json.loads(content)
            if len(par) == 0:
                break
            else:
                params += par
    
    repos = []
    for param in params:
        if int(param["stargazers_count"]) > minstars:
            repos.append(param["name"])

    return repos


def get_repo_stars(repo, maxpages=10):
    params = []
    for page in range(1, maxpages + 1):
        req = Request(
            "https://api.github.com/repos/rodluger/%s/stargazers?page=%d&per_page=100"
            % (repo, page)
        )
        req.add_header("Accept", "application/vnd.github.v3.star+json")
        API_KEY = os.getenv("GH_API_KEY", None)
        if API_KEY is not None:
            req.add_header("Authorization", "token %s" % API_KEY)
        content = urlopen(req).read()
        par = json.loads(content)
        if len(par) == 0:
            break
        else:
            params += par
    return params


def get_all_stars(clobber=False):
    if clobber or not os.path.exists("stars.json"):
        stars = []
        repos = get_all_repos()
        for repo in repos:
            stars += get_repo_stars(repo)
        with open("stars.json", "w") as json_file:
            json.dump(stars, json_file)
    else:
        print("Using cached stars.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clobber":
        clobber = True
    else:
        clobber = False
    get_all_stars(clobber=clobber)
