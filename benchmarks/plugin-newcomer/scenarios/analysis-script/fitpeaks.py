#!/usr/bin/env python3
"""Fit Gaussian peaks in two-column spectra (energy, counts); write <name>_peaks.csv next to each."""
import csv
import math
import sys
from pathlib import Path


def peaks(xs, ys, min_height):
    found = []
    for i in range(1, len(ys) - 1):
        if ys[i] > ys[i - 1] and ys[i] >= ys[i + 1] and ys[i] > min_height:
            half = ys[i] / 2
            lo = i
            while lo > 0 and ys[lo] > half:
                lo -= 1
            hi = i
            while hi < len(ys) - 1 and ys[hi] > half:
                hi += 1
            fwhm = xs[hi] - xs[lo]
            found.append((xs[i], fwhm / (2 * math.sqrt(2 * math.log(2))), ys[i]))
    return found


def main(folder):
    for f in sorted(Path(folder).glob("*.csv")):
        if f.stem.endswith("_peaks"):
            continue
        rows = [r for r in csv.reader(f.open()) if r and not r[0].startswith("#")]
        xs = [float(r[0]) for r in rows]
        ys = [float(r[1]) for r in rows]
        out = f.with_name(f.stem + "_peaks.csv")
        with out.open("w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["position", "sigma", "height"])
            w.writerows(peaks(xs, ys, max(ys) * 0.1))
        print(f"{f.name}: {out.name}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data")
