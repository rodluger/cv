#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import json
from datetime import date
from operator import itemgetter

__all__ = ["format_pub"]

JOURNAL_MAP = {
    "ArXiv e-prints": "ArXiv",
    "Monthly Notices of the Royal Astronomical Society": "\\mnras",
    "The Astrophysical Journal": "\\apj",
    "The Astronomical Journal": "\\aj",
    "Publications of the Astronomical Society of the Pacific": "\\pasp",
    "IAU General Assembly": "IAU",
    "American Astronomical Society Meeting Abstracts": "AAS",
}


def format_pub(args):
    ind, pub = args

    cites = pub["citations"]
    if cites == 0 or cites is None:
        cites = "\\textemdash"
    if pub["doctype"] == "article":
        fmt = "\\item[{{\\color{{numcolor}}\\scriptsize\\bfseries{0}}}] ".format(cites)
    else:
        fmt = "\\item[{{\\color{{numcolor}}\\scriptsize{0}}}] ".format(cites)
    n = [i for i in range(len(pub["authors"])) if "Luger, R" in pub["authors"][i]][0]
    pub["authors"][n] = "\\textbf{Luger, R.}"
    if len(pub["authors"]) > 5:
        fmt += ", ".join(pub["authors"][:4])
        fmt += ", \etal"
        if n >= 4:
            fmt += "\\ (including\\ \\textbf{Luger, R.})"
    elif len(pub["authors"]) > 1:
        fmt += ", ".join(pub["authors"][:-1])
        fmt += ", \\& " + pub["authors"][-1]
    else:
        fmt += pub["authors"][0]

    fmt += ", {0}".format(pub["year"])

    title = pub["title"]
    title = title.replace("\u2500", "-")
    title = title.replace("TRAPPIST-1", "TRAP\\-PIST-1")
    if pub["doi"] is not None:
        fmt += ", \\doi{{{0}}}{{{1}}}".format(pub["doi"], title)
    elif pub["arxiv"] is not None:
        fmt += ", \\arxiv{{{0}}}{{{1}}}".format(pub["arxiv"], title)
    elif pub["url"] is not None:
        fmt += ", \\link{{{0}}}{{{1}}}".format(pub["url"], title)
    else:
        fmt += ", \\emph{{{0}}}".format(title)

    if not pub["pub"] is None:
        fmt += ", " + JOURNAL_MAP.get(pub["pub"].strip("0123456789# "), pub["pub"])

    if pub["pub"] == "ArXiv e-prints":
        fmt += ":{0}".format(pub["arxiv"])

    if pub["volume"] is not None:
        fmt += ", \\textbf{{{0}}}".format(pub["volume"])

    if pub["page"] is not None:
        fmt += ", {0}".format(pub["page"])

    return fmt


def format_talk(args):
    ind, talk = args

    fmt = "\\item"
    n = [i for i in range(len(talk["authors"])) if "Luger, R" in talk["authors"][i]][0]
    talk["authors"][n] = "\\textbf{Luger, R.}"
    if len(talk["authors"]) > 5:
        fmt += ", ".join(talk["authors"][:4])
        fmt += ", \etal"
        if n >= 4:
            fmt += "\\ (including\\ \\textbf{Luger, R.})"
    elif len(talk["authors"]) > 1:
        fmt += ", ".join(talk["authors"][:-1])
        fmt += ", \\& " + talk["authors"][-1]
    else:
        fmt += talk["authors"][0]

    if not talk["url"] is None:
        fmt += ", \\link{{{0}}}{{{1}}}".format(talk["url"], talk["title"])
    else:
        fmt += ", \\emph{{{0}}}".format(talk["title"])

    fmt += ", {0}".format(talk["event"])
    fmt += ", {0}".format(talk["location"])

    YMD = [int(i) for i in talk["pubdate"].split("-")]
    if len(YMD) == 3:
        fmt += ", {0}".format(date(*YMD).strftime("%B %d, %Y"))
    else:
        YMD += [1]
        fmt += ", {0}".format(date(*YMD).strftime("%B %Y"))
    return fmt


if __name__ == "__main__":

    # Get pubs
    with open("pubs.json", "r") as f:
        pubs = json.load(f)
    with open("pubs_manual.json", "r") as f:
        pubs_manual = json.load(f)
    pubs = sorted(pubs + pubs_manual, key=itemgetter("pubdate"), reverse=True)
    pubs = [p for p in pubs if p["doctype"] in ["article", "eprint"]]
    ref = [p for p in pubs if p["doctype"] == "article"]
    unref = [p for p in pubs if p["doctype"] == "eprint"]

    # Compute citation stats
    ntotal = len(ref) + len(unref)
    npapers = len(ref)
    nfirst = sum(1 for p in pubs if "Luger, R" in p["authors"][0])
    tmp = [p["citations"] if p["citations"] is not None else 0 for p in pubs]
    cites = sorted(tmp, reverse=True)
    ncitations = sum(cites)
    hindex = sum(c >= i for i, c in enumerate(cites))
    summary = (
        "Total Pubs & \\textbf{{{0}}}\\\\"
        "Refereed & \\textbf{{{1}}}\\\\"
        "First Author & \\textbf{{{2}}}\\\\"
        "Citations & \quad \\textbf{{{3}}}\\\\"
        "h-index & \\textbf{{{4}}}"
    ).format(ntotal, npapers, nfirst, ncitations, hindex)
    summary = (
        "\\begin{table}\\begin{tabular}{rr}" + summary + "\\end{tabular}\\end{table}"
    )
    with open("pubs_summary.tex", "w") as f:
        f.write(summary)

    # Write pubs
    pubs = list(map(format_pub, zip(range(len(pubs), 0, -1), pubs)))
    with open("pubs.tex", "w") as f:
        f.write("\n\n".join(pubs))

    # Get talks
    with open("talks.json", "r") as f:
        talks = json.load(f)
    talks = sorted(talks, key=itemgetter("pubdate"), reverse=True)
    talks = list(map(format_talk, zip(range(len(talks), 0, -1), talks)))
    with open("talks.tex", "w") as f:
        f.write("\n\n".join(talks))
