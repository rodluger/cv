#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function
import json
from dateutil import parser
from datetime import datetime
import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
from operator import itemgetter

lato = fm.FontProperties(fname="fonts/Lato-Regular.ttf")


__all__ = ["make_plots"]


def plot_cites(ax, year1=2015):
    """Plot citation dates histogram."""
    citedates = np.loadtxt("citedates.txt")[1:]
    hist, bin_edges = np.histogram(citedates, bins=15)
    cdf = np.cumsum(hist)
    bins = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    ax.plot(bins, cdf, ".", color="C1", ms=3)
    ax.plot(bins, cdf, "-", color="C1", lw=3, alpha=0.5)
    plt.setp(
        ax.get_xticklabels(), rotation=30, fontsize=10, fontproperties=lato, alpha=0.75
    )
    plt.setp(
        ax.get_yticklabels(), rotation=30, fontsize=10, fontproperties=lato, alpha=0.75
    )
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontsize(10)
    ax.set_ylabel("citations", fontsize=16)
    ax.set_xlabel("year", fontsize=16)
    ax.set_xlim(year1, datetime.now().year + datetime.now().month / 12)


def plot_metrics(ax, year1=2015):
    with open("metrics.json") as json_file:
        metrics = json.load(json_file)
    for i, metric in enumerate(["h", "g", "i10"]):
        x, y = np.array(sorted(metrics["time series"][metric].items()), dtype=float).T
        inds = x >= 2015
        x = x[inds]
        y = y[inds]

        # HACK to add a little more resolution.
        # TODO: Re-think this...
        fac = 2
        xi = np.repeat(x, fac) + np.tile(np.linspace(0, 1, fac, endpoint=False), len(x))
        yi = np.interp(xi, x + 0.5, y)

        ax.plot(xi, yi, ".", color="C%d" % i, ms=3)
        ax.plot(xi, yi, "-", color="C%d" % i, lw=3, alpha=0.5, label=metric)
    plt.setp(
        ax.get_xticklabels(), rotation=30, fontsize=10, fontproperties=lato, alpha=0.75
    )
    plt.setp(
        ax.get_yticklabels(), rotation=30, fontsize=10, fontproperties=lato, alpha=0.75
    )
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontsize(10)
    ax.legend(loc="upper left", fontsize=8)
    ax.set_ylabel("index", fontsize=16)
    ax.set_xlabel("year", fontsize=16)
    ax.set_xlim(year1, datetime.now().year + datetime.now().month / 12)


def plot_stars(ax, year1=2015):
    """Plot stargazers histogram."""
    with open("stars.json") as json_file:
        stars = json.load(json_file)
    times = []
    for star in stars:
        times.append(parser.parse(star["starred_at"]))
    tzinfo = times[0].tzinfo
    years = range(year1, datetime.now().year + 1)
    now = datetime(
        datetime.now().year, datetime.now().month, datetime.now().day, tzinfo=tzinfo
    )
    bins = []
    counts = []
    for year in years:
        for month in range(1, 13):
            for day in range(32):
                try:
                    this_bin = datetime(year, month, day, tzinfo=tzinfo)
                    if this_bin > now:
                        continue
                    this_counts = 0
                    for time in times:
                        if this_bin >= time:
                            this_counts += 1
                    bins.append(matplotlib.dates.date2num(this_bin))
                    counts.append(this_counts)
                except ValueError:
                    pass
    inds = np.array(np.linspace(0, len(bins) - 1, 20), dtype=int)
    ax.plot_date(np.array(bins)[inds], np.array(counts)[inds], ".", color="C2", ms=3)
    ax.plot_date(bins, counts, "-", color="C2", lw=3, alpha=0.5)

    plt.setp(
        ax.get_xticklabels(), rotation=30, fontsize=10, fontproperties=lato, alpha=0.75
    )
    plt.setp(
        ax.get_yticklabels(), rotation=30, fontsize=10, fontproperties=lato, alpha=0.75
    )
    years = list(years) + [datetime.now().year + 1]
    ax.set_xticks(
        matplotlib.dates.date2num(
            [datetime(year, 1, 1, tzinfo=tzinfo) for year in years]
        )
    )
    ax.set_xticklabels(years)
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontsize(10)
    ax.set_ylabel("github stars", fontsize=16)
    ax.set_xlabel("year", fontsize=16)
    ax.margins(0.01, None)


def plot_papers(ax, year1=2015):
    """Plot paper dates histogram."""
    # Get pub dates
    with open("pubs.json", "r") as f:
        pubs = json.load(f)
    with open("pubs_manual.json", "r") as f:
        pubs_manual = json.load(f)
    pubs = sorted(pubs + pubs_manual, key=itemgetter("pubdate"), reverse=True)
    pubs = [p for p in pubs if p["doctype"] in ["article", "eprint"]]
    pubdates = []
    for pub in pubs:
        date = int(pub["pubdate"][:4]) + int(pub["pubdate"][5:7]) / 12.0
        pubdates.append(date)
    hist, bin_edges = np.histogram(pubdates, bins=15)
    cdf = np.cumsum(hist)
    bins = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    ax.plot(bins, cdf, ".", color="C0", ms=3)
    ax.plot(bins, cdf, "-", color="C0", lw=3, alpha=0.5)
    plt.setp(
        ax.get_xticklabels(), rotation=30, fontsize=10, fontproperties=lato, alpha=0.75
    )
    plt.setp(
        ax.get_yticklabels(), rotation=30, fontsize=10, fontproperties=lato, alpha=0.75
    )
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontsize(10)
    ax.set_ylabel("publications", fontsize=16)
    ax.set_xlabel("year", fontsize=16)
    ax.set_xlim(year1, datetime.now().year + datetime.now().month / 12)


def make_plots():
    fig, ax = plt.subplots(1, 5, figsize=(16, 2))
    fig.subplots_adjust(wspace=0.6)
    plot_papers(ax[0])
    plot_cites(ax[1])
    plot_stars(ax[2])
    plot_metrics(ax[3])
    for axis in ax[4:]:
        axis.axis("off")

    fig.savefig("metrics.pdf", bbox_inches="tight")


if __name__ == "__main__":
    make_plots()
