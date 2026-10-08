"""<One line: what this experiment computes.>

Run it from the repository folder, naming a configuration in configs/:

    python experiments/<name>/run.py base
    python experiments/<name>/run.py base --quick              # reduced test run
    python experiments/<name>/run.py base --set n_samples=[100,1000]   # override values

Where the results go (chosen by the helper):
    tables       experiments/<name>/output/base/*.csv    ex.save_table(...)
                 and the same table in Markdown (*.md), ready to copy into a log entry
    other files  experiments/<name>/output/base/...      ex.path("file.npz")
    figures      log/figs/<name>-base.png                 ex.save_figure(...)
These are working files, not committed. A figure becomes part of the record
when a log entry embeds it; `logtool save` then keeps a copy with the entry.

Create a new experiment from this template with
    python tools/logtool.py experiment <name>
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import matplotlib  # noqa: E402

matplotlib.use("Agg")                   # draw figures to files, without opening windows
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from cfproject.experiment import Experiment  # noqa: E402
# Your own code lives in src/cfproject/, e.g.
# from cfproject.lsm import lsm_put  # noqa: E402


def main():
    ex = Experiment(__file__)           # reads configs/<config>.yaml named on the command line
    cfg = ex.config                     # a dictionary: cfg["sigma"], cfg["n_samples"], ...

    # ------------------------------------------------------------ computation (replace)
    # Example: estimate the mean of a normal distribution with n samples.
    rows = []
    for i, n in enumerate(cfg["n_samples"]):
        rng = ex.rng(offset=i)          # seeded from cfg["seed"]; an independent stream for each i
        x = rng.normal(cfg["mu"], cfg["sigma"], size=n)
        rows.append({"n": n, "mean": x.mean(), "se": x.std(ddof=1) / np.sqrt(n)})

    # ------------------------------------------------------------ results
    # A table: written to output/<config>/estimates.csv, and as a Markdown table ready
    # for the log to output/<config>/estimates.md (also printed on screen).
    ex.save_table(rows, "estimates", fmt={"mean": "{:.4f}", "se": "{:.4f}"})

    # A figure: written to log/figs/<name>-<config>.png, ready to embed in a log entry.
    fig, ax = plt.subplots(figsize=(6, 3.6))
    n = np.array([r["n"] for r in rows])
    ax.errorbar(n, [r["mean"] for r in rows], yerr=[2 * r["se"] for r in rows], fmt="o-",
                capsize=3, label="estimate ± 2 s.e.")
    ax.axhline(cfg["mu"], color="gray", ls="--", label="true mean")
    ax.set_xscale("log")
    ax.set_xlabel("number of samples")
    ax.set_ylabel("estimate")
    ax.legend(frameon=False)
    ex.save_figure(fig)
    # Any other output file goes to the same folder, e.g. np.savez(ex.path("samples.npz"), x=x)


# Keep this guard: with parallel code (multiprocessing, joblib) on Windows and macOS,
# worker processes import this file, and must not run main() themselves.
if __name__ == "__main__":
    main()
