#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function
import matplotlib.font_manager as fm
import matplotlib.pyplot as pl
from matplotlib.ticker import MaxNLocator
import numpy as np
lato = fm.FontProperties(fname='fonts/Lato-Regular.ttf')

__all__ = ["plot_cites"]


def plot_cites():
    """Plot citation dates histogram."""
    citedates = np.loadtxt('citedates.txt')
    hist, bin_edges = np.histogram(citedates, bins=15)
    cdf = np.cumsum(hist)
    bins = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    fig, ax = pl.subplots(1, figsize=(2.5, 2))
    ax.plot(bins, cdf, '.', color='C0', ms=3)
    ax.plot(bins, cdf, '-', color='C0', lw=3, alpha=0.5)
    pl.setp(ax.get_xticklabels(), rotation=30,
            fontsize=10, fontproperties=lato, alpha=0.75)
    pl.setp(ax.get_yticklabels(), rotation=30,
            fontsize=10, fontproperties=lato, alpha=0.75)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontsize(12)
    fig.savefig('citations.pdf', bbox_inches='tight')


if __name__ == "__main__":
    plot_cites()
