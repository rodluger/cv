#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from operator import itemgetter
import re
import ads
from utf8totex import utf8totex
from titlecase import titlecase
from tqdm import tqdm
import numpy as np
import time
import sys

__all__ = ["get_papers"]


def title_callback(word, **kwargs):
    if "\\" in word:
        return word
    else:
        return None


def format_title(arg):
    """
    Customized!

    """

    # Do the conversion
    arg = utf8totex(arg)

    # Handle subscripts
    arg = re.sub("<SUB>(.*?)</SUB>", r"$_\1$", arg)

    # Fudge O2 paper
    arg = re.sub("O2Buildup", r"O$_2$ Buildup", arg)

    # Capitalize!
    arg = titlecase(arg, callback=title_callback)

    return arg


def format_authors(authors):
    """
    Customized!

    """

    # Do the conversion
    authors = list(map(utf8totex, authors))

    # Abbreviate names. This drops middle
    # initials -- should eventually fix this.
    for i, author in enumerate(authors):
        match = re.match("^(.*?),\s(.*?)$", author)
        if match is not None:
            first, last = match.groups()
            authors[i] = "%s, %s." % (first, last[0])

    return authors


def manual_exclude(paper):
    """Manual exclusions."""
    # Remove DDS talks
    if paper.pub == "LPI Contributions":
        return True

    # Remove Laura's duplicate
    if "The Contribution of M-Dwarf Flares" in format_title(paper.title[0]) and paper.doi is None:
        return True

    # Remove DS Tuc duplicate
    if "Four Newborn Planets" in format_title(paper.title[0]) and paper.doi is None:
        return True

    return False


def get_papers(author, count_cites=True):
    papers = list(
        ads.SearchQuery(
            author=author,
            fl=[
                "id",
                "title",
                "author",
                "doi",
                "year",
                "pubdate",
                "pub",
                "volume",
                "page",
                "identifier",
                "doctype",
                "citation_count",
                "bibcode",
                "citation",
            ],
            max_pages=100,
        )
    )
    dicts = []

    # Count the citations as a function of time
    citedates = []

    # Save bibcodes for later
    bibcodes = []

    # Save papers that cite me
    if os.path.exists("papers_that_cite_me.json"):
        with open("papers_that_cite_me.json", "r") as f:
            papers_that_cite_me = json.load(f)
    else:
        papers_that_cite_me = {}

    for paper in tqdm(papers):

        if not (
            ("Luger, Rodrigo" in paper.author)
            or ("Luger, R." in paper.author)
            or ("Luger, R" in paper.author)
        ):
            continue

        if manual_exclude(paper):
            continue

        aid = [
            ":".join(t.split(":")[1:])
            for t in paper.identifier
            if t.startswith("arXiv:")
        ]
        for t in paper.identifier:
            if len(t.split(".")) != 2:
                continue
            try:
                list(map(int, t.split(".")))
            except ValueError:
                pass
            else:
                aid.append(t)
        try:
            page = int(paper.page[0])
        except ValueError:
            page = None
            if paper.page[0].startswith("arXiv:"):
                aid.append(":".join(paper.page[0].split(":")[1:]))
        except TypeError:
            page = None

        # Get citation dates
        if count_cites and paper.citation is not None:
            for i, bibcode in enumerate(paper.citation):
                try:
                    if bibcode in papers_that_cite_me.keys():
                        date = papers_that_cite_me[bibcode]
                    else:
                        cite = list(ads.SearchQuery(bibcode=bibcode, fl=["pubdate"]))[0]
                        date = int(cite.pubdate[:4]) + int(cite.pubdate[5:7]) / 12.0
                        papers_that_cite_me[bibcode] = date
                    citedates.append(date)
                except IndexError:
                    pass

        # Save bibcode
        bibcodes.append(paper.bibcode)

        dicts.append(
            dict(
                doctype=paper.doctype,
                authors=format_authors(paper.author),
                year=paper.year,
                pubdate=paper.pubdate,
                doi=paper.doi[0] if paper.doi is not None else None,
                title=format_title(paper.title[0]),
                pub=paper.pub,
                volume=paper.volume,
                page=page,
                arxiv=aid[0] if len(aid) else None,
                citations=paper.citation_count,
                url="http://adsabs.harvard.edu/abs/" + paper.bibcode,
            )
        )

    if count_cites:
        # Sort the cite dates
        citedates = sorted(citedates)
        np.savetxt("citedates.txt", citedates, fmt="%.3f")

    # Save bibcodes
    with open("bibcodes.txt", "w") as f:
        for bibcode in bibcodes:
            print(bibcode, file=f)

    # Save papers that cite me
    with open("papers_that_cite_me.json", "w") as f:
        json.dump(papers_that_cite_me, f)

    return sorted(dicts, key=itemgetter("pubdate"), reverse=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clobber":
        clobber = True
    else:
        clobber = False
    if clobber or not os.path.exists("pubs.json"):
        papers = get_papers("Luger, R", count_cites=True)
        with open("pubs.json", "w") as f:
            json.dump(papers, f, sort_keys=True, indent=2, separators=(",", ": "))
    else:
        print("Using cached pubs.")
