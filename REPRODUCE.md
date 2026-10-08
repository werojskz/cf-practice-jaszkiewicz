# Reproducing the results

With a fresh clone of this repository and the packages in
`requirements.txt`, anyone can regenerate every table and figure of the
report with the commands below.

## Report items

One row per table or figure of the report, in the order they must be run
(rows that use outputs of other rows come later). Put the command in
`backticks`: `python tools/logtool.py reproduce` runs these commands.

| Item | Command | Output | Runtime |
|---|---|---|---|
| Table 1 | `python experiments/<name>/run.py <config>` | `experiments/<name>/output/<config>/...` | ... |
| Figure 1 | `python experiments/<name>/run.py <config>` | `log/figs/<name>-<config>.png` | ... |

(Rows containing `<...>` are ignored by `reproduce`: replace them with your own.)
When the same script produces several items with different parameters, each
item has its own configuration file and its own row.

```bash
python tools/logtool.py reproduce --list        # show the items
python tools/logtool.py reproduce               # run all of them
python tools/logtool.py reproduce "Figure 2"    # run one item
python tools/logtool.py reproduce --quick       # reduced runs, as a quick check
```

## Data

Where external data come from and how to obtain them: source, tickers or
series, date range, access date, and a script or exact steps for
downloading them. If a file cannot be redistributed, say how to get it.

*Or:* No external data: all results use simulated data.

## Environment and cost

- Python version and operating system used: ...
- `requirements.txt` with exact versions (`pip freeze > requirements.txt`).
- Hardware and runtime of the longest runs (e.g. "trained on 8 CPU cores,
  3 hours; `--quick` gives a 10-minute version with the same code path").
