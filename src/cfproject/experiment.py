"""Helper for experiment scripts: configuration, output locations, provenance.

An experiment is a folder experiments/<name>/ with one or more scripts
(usually run.py) and one YAML file per parameter set in configs/. A script
is run with the name of a configuration:

    python experiments/<name>/run.py base           # uses configs/base.yaml
    python experiments/<name>/run.py base --quick   # reduced test run

Where things go (so that different scripts and configurations never
overwrite each other):

    tables        experiments/<name>/output/<tag>/<table>.csv    ex.save_table(rows, "table")
                  experiments/<name>/output/<tag>/<table>.md     (same table in Markdown, for the log)
    other files   experiments/<name>/output/<tag>/<file>         ex.path("file.npz")
    figures       log/figs/<name>-<tag>[-suffix].png              ex.save_figure(fig)

<tag> is the configuration name for run.py, and <script>-<config> for any
other script (e.g. rank_check-base). These are working files: they are not
committed. A figure becomes part of the record when a log entry embeds it
(`logtool save` then copies it into the entry's own folder).

Every figure carries its provenance inside the PNG file (command,
configuration, commit, uncommitted changes, date, machine); see it with
`python tools/logtool.py figinfo <entry or file>`. The same information is
written to output/<tag>/config_used.yaml.

The helper needs only numpy, PyYAML and matplotlib (for figures). It works
without Git and outside the repository, e.g. in a copy of the experiment
folder and src/ on another machine.
"""
import argparse
import csv
import datetime as dt
import platform
import re
import subprocess
import sys
from pathlib import Path

import yaml


class Experiment:
    """Set up an experiment run. Create it once, in main():

        ex = Experiment(__file__)
    """

    def __init__(self, script_file, argv=None):
        self.script = Path(script_file).resolve()
        self.folder = self.script.parent
        self.name = self.folder.name
        self.root = self.folder.parents[1]
        configs = sorted((self.folder / "configs").glob("*.yaml"))
        names = [c.stem for c in configs]
        ap = argparse.ArgumentParser(description=f"Experiment {self.name}")
        ap.add_argument("config", nargs="?",
                        help=f"configuration in configs/ (available: {', '.join(names) or 'none'})")
        ap.add_argument("--quick", action="store_true",
                        help="reduced test run using the 'quick:' section of the configuration")
        ap.add_argument("--set", nargs="+", default=[], metavar="KEY=VALUE",
                        help="override configuration values for this run, e.g. --set n_paths=1e6")
        args = ap.parse_args(argv)
        variant = args.config
        if variant is None:
            if len(configs) != 1:
                ap.error(f"name a configuration: {', '.join(names)}")
            variant = names[0]
        if variant.endswith(".yaml"):
            variant = Path(variant).stem
        path = self.folder / "configs" / f"{variant}.yaml"
        if not path.exists():
            ap.error(f"no configs/{variant}.yaml (available: {', '.join(names)})")
        self.variant = variant
        self.quick = args.quick
        self.config_path = path
        cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        quick = cfg.pop("quick", {}) or {}
        if self.quick:
            cfg.update(quick)
        for item in args.set:
            key, sep, value = item.partition("=")
            if not sep:
                ap.error(f"--set expects KEY=VALUE, got '{item}'")
            cfg[key] = yaml.safe_load(value)
        self.config = _numbers(cfg)
        self.tag = variant if self.script.stem == "run" else f"{self.script.stem}-{variant}"
        self.out = self.folder / ("output_quick" if self.quick else "output") / self.tag
        self.figdir = self.root / "log" / "figs" / ("quick" if self.quick else "")
        self.command = " ".join(["python", self.rel(self.script), variant] +
                                (["--quick"] if self.quick else []) +
                                (["--set", *args.set] if args.set else []))
        self.provenance = self._provenance()
        self.out.mkdir(parents=True, exist_ok=True)
        (self.out / "config_used.yaml").write_text(
            "".join(f"# {k}: {v}\n" for k, v in self.provenance.items()) +
            yaml.safe_dump(self.config, sort_keys=False), encoding="utf-8")
        print(f"== {self.command}   (outputs: {self.rel(self.out)}/)")
        if self.provenance.get("uncommitted changes"):
            print("   note: the code has uncommitted changes ("
                  f"{self.provenance['uncommitted changes']})")

    # ------------------------------------------------------------------ provenance
    def _provenance(self):
        info = {"command": self.command, "config": self.rel(self.config_path),
                "date": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                "machine": platform.node() or "?", "python": sys.version.split()[0]}
        try:
            def g(*a):
                return subprocess.run(["git", *a], cwd=self.folder, capture_output=True,
                                      text=True, timeout=10).stdout.rstrip()
            commit = g("rev-parse", "--short", "HEAD").strip()
            info["commit"] = commit or "unknown (not in a Git repository)"
            if commit:
                dirty = [ln[3:].strip() for ln in g("status", "--porcelain", "--untracked-files=all", "--", ".", "../../src")
                         .splitlines() if ln[3:].strip().endswith((".py", ".yaml", ".yml", ".ipynb"))]
                if dirty:
                    info["uncommitted changes"] = ", ".join(dirty[:8])
        except (OSError, subprocess.SubprocessError):
            info["commit"] = "unknown (Git not available)"
        return info

    def rel(self, p):
        p = Path(p).resolve()
        try:
            return p.relative_to(self.root).as_posix()
        except ValueError:
            return p.as_posix()

    # ------------------------------------------------------------------ paths
    def path(self, filename):
        """Path for any other output file, e.g. np.savez(ex.path("paths.npz"), ...)."""
        return self.out / filename

    def output_of(self, experiment, config, filename, script="run"):
        """Path of a file written by another experiment, e.g.
        ex.output_of("binomial_ref", "ls_grid", "reference_grid.csv")."""
        tag = config if script == "run" else f"{script}-{config}"
        p = self.root / "experiments" / experiment / "output" / tag / filename
        if not p.exists():
            raise FileNotFoundError(f"{self.rel(p)} does not exist: run\n"
                                    f"    python experiments/{experiment}/{script}.py {config}\nfirst.")
        return p

    # ------------------------------------------------------------------ random numbers
    def rng(self, key="seed", offset=0):
        """numpy Generator seeded from the configuration value cfg[key].

        offset=0 gives the stream of cfg[key] itself; offsets 1, 2, ... give further
        streams that are statistically independent of it and of each other, and
        do not collide with other seeds (e.g. seed 101 is not seed 100 with offset 1).
        """
        import numpy as np
        seed = self.config[key]
        return np.random.default_rng(seed if offset == 0 else [seed, offset])

    # ------------------------------------------------------------------ tables
    def save_table(self, rows, name, fmt=None, show=True):
        """Write rows (a list of dicts) to two files in output/<tag>/:
        <name>.csv  the numbers at full precision, for further processing;
        <name>.md   the same table in Markdown, formatted with fmt, ready to copy
                    into a log entry.
        With show=True the Markdown table is also printed."""
        if not rows:
            return None
        f = self.out / f"{name}.csv"
        with open(f, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        table = md_table(rows, fmt=fmt)
        md = self.out / f"{name}.md"
        md.write_text(table + "\n", encoding="utf-8")
        if show:
            print()
            print(table)
            print()
        print(f"saved {self.rel(f)}")
        print(f"saved {self.rel(md)}  (Markdown table, ready to copy into the log)")
        return f

    # ------------------------------------------------------------------ figures
    def figure_path(self, suffix=""):
        return self.figdir / f"{self.name}-{self.tag}{'-' + suffix if suffix else ''}.png"

    def save_figure(self, fig, suffix=""):
        """Save a matplotlib figure as log/figs/<name>-<tag>[-suffix].png, with its
        provenance stored inside the file."""
        path = self.figure_path(suffix)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.tight_layout()
        comment = "\n".join(f"{k}: {v}" for k, v in self.provenance.items())
        fig.savefig(path, dpi=140, bbox_inches="tight", metadata={"Comment": comment})
        print(f"saved {self.rel(path)}")
        return path


_FLOAT_TEXT = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)[eE][+-]?\d+$")


def _numbers(obj):
    """Configuration values: YAML reads 1e5 as text, so turn such values into numbers;
    whole numbers of at least 1000 written as decimals (2.0e+5) become integers."""
    if isinstance(obj, dict):
        return {k: _numbers(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_numbers(v) for v in obj]
    if isinstance(obj, str) and _FLOAT_TEXT.match(obj.strip()):
        obj = float(obj)
    if isinstance(obj, float) and obj.is_integer() and 1000 <= abs(obj) < 2**53:
        return int(obj)
    return obj


def md_table(rows, cols=None, fmt=None):
    """Markdown table from a list of dicts. fmt maps column -> format, e.g. {'price': '{:.4f}'}."""
    cols = cols or list(rows[0])
    fmt = fmt or {}

    def cell(r, c):
        v = r[c]
        if c in fmt:
            return fmt[c].format(v)
        if isinstance(v, float):
            return f"{v:.6g}"
        return str(v)

    lines = ["| " + " | ".join(cols) + " |", "|" + "---:|" * len(cols)]
    lines += ["| " + " | ".join(cell(r, c) for c in cols) + " |" for r in rows]
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(__doc__)
