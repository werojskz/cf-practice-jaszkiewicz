# Experiments

The student manual (section "Writing experiment programs") explains this in
detail. In short:

```
experiments/lsm_basis/
  run.py                 the code, shared by all parameter sets
  configs/base.yaml      one parameter set, including the random seed
  configs/hard.yaml      another one
  output/base/           working results of "run.py base" (not committed):
                         tables as .csv, and as .md ready to copy into the log
  imported/              results obtained elsewhere, copied in (committed)
```

```bash
python tools/logtool.py experiment lsm_basis           # create a new experiment from _template/
python experiments/lsm_basis/run.py base               # figures go to log/figs/lsm_basis-base.png
python experiments/lsm_basis/run.py hard --quick       # reduced test run
python experiments/lsm_basis/run.py hard --set n_eval=1e6   # override a value for this run
```

Good practice (the manual explains why):

- Parameters and seeds in configuration files; `--set` for quick variations.
- Write results through the helper (`ex.save_table`, `ex.save_figure`,
  `ex.path(...)`): they land in predictable places and figures carry their
  provenance (see `python tools/logtool.py figinfo`).
- Outputs in `output/` and `log/figs/` are working files, overwritten by the
  next run. What matters is kept by the log: figures embedded in an entry are
  frozen with it; tables are pasted into the entry.
- Results obtained outside the repository go into
  `experiments/<name>/imported/<date>_<where>/`, and the entry says how they
  were produced.
