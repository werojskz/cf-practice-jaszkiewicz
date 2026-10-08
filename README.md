# Project {{PROJECT}}: {{TITLE}}

Computational Finance projects 2026/27, group **{{GROUP}}**.

| Member | GitHub |
|---|---|
{{MEMBERS_TABLE}}

**Main reference:** {{REFERENCE}}

> If you see `{{...}}` placeholders above, the repository has not been
> initialised yet: run `python tools/logtool.py init` (see the student manual).

## Everyday commands

```bash
git pull                                              # get the others' work
python experiments/<name>/run.py <config>             # run an experiment
python tools/logtool.py save -m "What I changed"      # commit + push code (any time)
python tools/logtool.py new "Title of the entry"      # new log entry (date, author, commit filled in)
#   ... edit the new file in log/, embed figures with ![caption](figs/<figure>.png) ...
python tools/logtool.py save                          # freeze figures, check, commit, push
```

New experiment: `python tools/logtool.py experiment <name>`.

## Where things are

| Path | Content |
|---|---|
| [`log/`](log/README.md) | **Development log**, one Markdown file per entry. Rules: [LOG_GUIDE.md](LOG_GUIDE.md). |
| `log/figs/` | Working figures written by the experiment scripts (not committed); `log/figs/<entry>/` holds each entry's frozen figures (committed). |
| `log/derivations/` | Longer derivations (`.tex` and compiled `.pdf`). |
| `src/cfproject/` | Your implementation: models, pricers, estimators. |
| `experiments/<name>/` | One folder per experiment: `run.py`, one config per parameter set in `configs/`; working results in `output/` (not committed). |
| `experiments/<name>/imported/` | Results obtained outside this repository (Colab, a cluster), copied in and committed. |
| `experiments/_template/` | Starting point for new experiments (`logtool experiment <name>` copies it). |
| `report/` | Final report (`report.tex`, at most 5 pages). |
| [`REPRODUCE.md`](REPRODUCE.md) | One command for every table and figure of the report. |
| `tools/logtool.py` | Log helper: `init`, `new`, `save`, `check`, `experiment`, `figinfo`, `reproduce`. |

## Setup on your computer

```bash
git clone <this repository's URL>
cd <folder>
pip install -r requirements.txt
```
