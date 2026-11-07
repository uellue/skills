#!/usr/bin/env python3
"""Make a copy of the kaizen plugin with one rule removed, for a leave-one-out eval run.

    python3 benchmarks/rule-ablation/ablate.py <variant-id> <new-directory>
    python3 benchmarks/rule-ablation/ablate.py --list

The variant (variants.json beside this script) names a file of the plugin and an exact text; the text
must occur exactly once. The copy goes to a directory that must not exist yet (nothing is ever
overwritten or deleted), without the plugin's eval results. Prints the eval command for the copy.
"""

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parents[1] / "plugins" / "kaizen"


def load(path=HERE / "variants.json"):
    return {v["id"]: v for v in json.loads(Path(path).read_text())["variants"]}


def ablate(variant, plugin, out):
    out = Path(out)
    if out.exists():
        raise SystemExit(f"{out} exists; give a new directory")
    target = Path(plugin) / variant["file"]
    text = target.read_text()
    n = text.count(variant["remove"])
    if n != 1:
        raise SystemExit(f"{variant['id']}: the text occurs {n} times in {target}, expected once")
    shutil.copytree(plugin, out, ignore=shutil.ignore_patterns("results", "__pycache__"))
    (out / variant["file"]).write_text(text.replace(variant["remove"], "", 1))
    return out


def main(argv):
    variants = load()
    if argv == ["--list"]:
        for v in variants.values():
            print(f"{v['id']}\t{v['case']}\n  expected: {v['expected_by_agent']}")
        return
    if len(argv) != 2 or argv[0] not in variants:
        raise SystemExit(f"usage: ablate.py <variant-id> <new-directory> | --list; variants: {', '.join(variants)}")
    v = variants[argv[0]]
    out = ablate(v, PLUGIN, argv[1])
    print(f"copy without the rule: {out}\n"
          f"cd {out} && claude plugin eval . --case {v['case']} --scaffold --allow-tools Write Edit "
          f"--ablation none --no-publish --max-cost-usd 2")


if __name__ == "__main__":
    main(sys.argv[1:])
