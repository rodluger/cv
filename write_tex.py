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
    fmt = "\\item[{{\\color{{numcolor}}\\scriptsize{0}}}] ".format(
                                                            pub["citations"])
    n = [i for i in range(len(pub["authors"]))
         if "Luger, R" in pub["authors"][i]][0]
    pub["authors"][n] = "\\textbf{Luger, Rodrigo}"
    if len(pub["authors"]) > 5:
        fmt += ", ".join(pub["authors"][:4])
        fmt += ", \etal"
        if n >= 4:
            fmt += "\\ (incl.\\ \\textbf{RL})"
    elif len(pub["authors"]) > 1:
        fmt += ", ".join(pub["authors"][:-1])
        fmt += ", \\& " + pub["authors"][-1]
    else:
        fmt += pub["authors"][0]

    fmt += ", {0}".format(pub["year"])

    if pub["doi"] is not None:
        fmt += ", \\doi{{{0}}}{{{1}}}".format(pub["doi"], pub["title"])
    else:
        fmt += ", " + pub["title"]

    if not pub["pub"] in [None, "ArXiv e-prints"]:
        fmt += ", " + JOURNAL_MAP.get(pub["pub"].strip("0123456789# "),
                                      pub["pub"])

    if pub["volume"] is not None:
        fmt += ", \\textbf{{{0}}}".format(pub["volume"])

    if pub["page"] is not None:
        fmt += ", {0}".format(pub["page"])

    if pub["arxiv"] is not None:
        fmt += " (\\arxiv{{{0}}})".format(pub["arxiv"])

    return fmt


if __name__ == "__main__":
    with open("pubs.json", "r") as f:
        pubs = json.load(f)
    pubs = sorted(pubs, key=itemgetter("pubdate"), reverse=True)
    pubs = [p for p in pubs if p["doctype"] in ["article", "eprint"]]
    ref = [p for p in pubs if p["doctype"] == "article"]
    unref = [p for p in pubs if p["doctype"] == "eprint"]

    # Compute citation stats
    npapers = len(ref)
    nfirst = sum(1 for p in pubs if "Luger, R" in p["authors"][0])
    cites = sorted((p["citations"] for p in pubs), reverse=True)
    ncitations = sum(cites)
    hindex = sum(c >= i for i, c in enumerate(cites))

    summary = (("refereed: {1} / first author: {2} / citations: {3} / "
               "h-index: {4} ({0})")
               .format(date.today(), npapers, nfirst, ncitations, hindex))
    with open("pubs_summary.tex", "w") as f:
        f.write(summary)

    pubs = list(map(format_pub, zip(range(len(pubs), 0, -1), pubs)))
    with open("pubs.tex", "w") as f:
        f.write("\n\n".join(pubs))
