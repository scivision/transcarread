#!/usr/bin/env python
"""
read excitation rates and plot

    python transcar2excitationrates.py tests/data/beam52
"""
from pathlib import Path
from matplotlib.pyplot import show
from argparse import ArgumentParser
from transcarread import ExcitationRates
from transcarread.plots import plotExcrates
import seaborn as sns

sns.set_context("talk")


def main():
    p = ArgumentParser(description="Read Transcar excitation rates")
    p.add_argument("--emisfn", help="emissions.dat filename", default="dir.output/emissions.dat")
    p.add_argument("path", help="path where dir.output/emissions.dat is")
    p = p.parse_args()

    path = Path(p.path).expanduser().resolve()

    if path.stem.startswith("beam"):  # specific beam
        dlist = [path]
    else:  # overall simulation
        dlist = (d for d in path.iterdir() if d.is_dir())

    for d in dlist:
        rates = ExcitationRates(d / p.emisfn)
        rates.name = d.name[4:]
        plotExcrates(rates)

    show()


if __name__ == "__main__":
    main()