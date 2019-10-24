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

lato = fm.FontProperties(fname="fonts/Lato-Regular.ttf")


__all__ = ["make_plots"]


def plot_cites(ax):
    """Plot citation dates histogram."""
    citedates = np.loadtxt("citedates.txt")[1:]
    hist, bin_edges = np.histogram(citedates, bins=15)
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
    ax.set_ylabel("citations", fontsize=16)
    ax.set_xlabel("year", fontsize=16)


def plot_metrics(ax):
    with open("metrics.json") as json_file:
        metrics = json.load(json_file)
    for i, metric in enumerate(["h", "g", "i10"]):
        x, y = np.array(sorted(metrics["time series"][metric].items()), dtype=float).T
        inds = x >= 2015
        x = x[inds]
        y = y[inds]
        ax.plot(x, y, ".", color="C%d" % i, ms=3)
        ax.plot(x, y, "-", color="C%d" % i, lw=3, alpha=0.5, label=metric)
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
    ax.plot_date(np.array(bins)[inds], np.array(counts)[inds], ".", color="C0", ms=3)
    ax.plot_date(bins, counts, "-", color="C0", lw=3, alpha=0.5)

    plt.setp(
        ax.get_xticklabels(), rotation=30, fontsize=10, fontproperties=lato, alpha=0.75
    )
    plt.setp(
        ax.get_yticklabels(), rotation=30, fontsize=10, fontproperties=lato, alpha=0.75
    )
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


def plot_papers(ax, year1=2015):
    """Plot paper dates histogram."""
    pubdates = np.loadtxt("pubdates.txt")[1:]
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


def make_plots():
    fig, ax = plt.subplots(1, 5, figsize=(16, 2))
    fig.subplots_adjust(wspace=0.6)
    plot_papers(ax[0])
    plot_cites(ax[1])
    plot_metrics(ax[2])
    plot_stars(ax[3])
    for axis in ax[4:]:
        axis.axis("off")

    fig.savefig("metrics.pdf", bbox_inches="tight")


if __name__ == "__main__":
    make_plots()
