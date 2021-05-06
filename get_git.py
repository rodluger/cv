import urllib
from urllib.request import Request, urlopen
import json
import os

__all__ = ["get_all_stars"]


def get_repo_stars(repo, maxpages=5):
    params = []
    for page in range(1, maxpages + 1):
        req = Request(
            "https://api.github.com/repos/rodluger/%s/stargazers?page=%d&per_page=100"
            % (repo, page)
        )
        req.add_header("Accept", "application/vnd.github.v3.star+json")
        req.add_header("Authorization", "token %s" % os.getenv("GITHUB_API_KEY", ""))
        content = urlopen(req).read()
        par = json.loads(content)
        if len(par) == 0:
            break
        else:
            params += par
    return params


def get_all_stars(
    repos=[
        "starry_process",
        "starry",
        "everest",
        "planetplanet",
        "cortex",
        "Limbdark.jl",
    ]
):
    stars = []
    for repo in repos:
        stars += get_repo_stars(repo)
    with open("stars.json", "w") as json_file:
        json.dump(stars, json_file)


def get_repo_stats(repo):
    req = Request(
        "https://api.github.com/repos/rodluger/%s/stats/participation" % (repo)
    )
    content = urlopen(req).read()
    par = json.loads(content)
    # TODO


if __name__ == "__main__":
    try:
        get_all_stars()
    except urllib.error.HTTPError:
        # DEBUG: Investigate this...
        print("HTTPError in `get_git.py`")
        pass
