# How to keep the development log

The log is the main evidence of your work and carries the largest part of
the mark. It should let a reader follow how you got your code to work and
how you chose methods and parameters, including what did not work. The
student manual explains the rules and the marking in full; this is the
short version.

## What makes a good log

- **Regular.** At least one entry per week as a group. Every member writes
  entries about their own work regularly (two or more per month each).
- **Concrete.** Results are numbers, tables or figures produced by code in
  this repository, with Monte Carlo standard errors where relevant.
- **Honest.** Bugs, dead ends and wrong expectations, with an explanation,
  are valuable entries. A log with only successes is not believable.
- **Reasoned.** Say what you expected, what you got and what you conclude.
- **Traceable.** Each entry names the commit of the code and says which
  scripts and parameters produced its results.

## Writing an entry

```bash
git pull
python experiments/lsm_basis/run.py base                  # 1. run what the entry is about
python experiments/lsm_basis/run.py hard
python tools/logtool.py new "Effect of basis degree"      # 2. create the entry
#   3. edit the new file log/2026-10-27_effect-of-basis-degree.md
python tools/logtool.py save                              # 4. freeze figures, check, commit, push
```

- `new` fills in the date, your name and the **Code** field: the current
  commit, plus any files with uncommitted changes. Commit your code first
  (`python tools/logtool.py save -m "..."`) if you want a clean record.
- In the section **Code and runs**, say in your own words which scripts,
  configurations and parameters produced the results. If anything was run
  outside the repository (Colab, a cluster), say where and from which commit,
  and copy the results into `experiments/<name>/imported/<date>_<where>/`.
- **Figures:** embed them from wherever they are in the repository, e.g.
  `![Price against degree](figs/lsm_basis-base.png)`. `save` copies each
  embedded figure into the entry's own folder `log/figs/<entry>/` and points
  the link there, so later runs can never change what the entry shows.
  Figures outside the repository folder are refused: copy them in first.
- `save` checks the format. An entry with errors is **held back** (not
  committed) and the errors are listed; everything else is committed and
  pushed. Fix the entry and save again.
- For entries without computations (reading notes, a derivation, a plan)
  use `new "Title" --no-code`. For a joint entry add
  `--author "Anna Nowak, Maria Wojcik"`.
- `python tools/logtool.py figinfo <entry>` shows how each figure of an entry
  was produced (for figures saved by the experiment helper).

## Structure of an entry

`log/YYYY-MM-DD_short-title.md`, created from the template:

| Part | Content |
|---|---|
| `# Title` | What the entry is about. |
| Fields | `Date`, `Author`, `Code` (filled in by `new`). |
| `## Goal` | The question you are trying to answer. |
| `## Method` | What you implemented or tried, with the parameters needed to repeat it. |
| `## Code and runs` | Which scripts, configurations and parameters produced the results (`n/a` for entries without computations). |
| `## Results` | Tables, figures, program output. |
| `## Interpretation` | What the results mean; whether they were expected. |
| `## Next steps` | What you will try next, and why. |
| `## AI assistance` | Optional: what an AI tool produced, how you checked it, what was wrong with it. |

Use `###` for subsections. Half a page is a typical entry.

## Rules

1. **Do not rewrite history.** Do not change the results or conclusions of
   a committed entry. Correct mistakes in a new entry that links to the old
   one. Fixing typos is fine.
2. **Write the entry when you do the work**, and save (push) it the same day.
3. **Everything in the repository.** Figures in `log/figs/`, derivations in
   `log/derivations/`, code and configs in `src/` and `experiments/`.
4. **Snapshots** of all repositories are taken by the instructor at each
   deadline (P1, P2, final). Whatever is pushed by then is assessed.

## Maths, tables and figures

GitHub shows the log in the browser, including maths.

**Maths.** Inline `$\mathbb{E}[e^{-rT}(K-S_T)^+]$`. Display maths on its
own lines, with an empty line before and after:

```markdown
The continuation value is estimated by least squares:

$$
\hat C_t(x) = \sum_{k=0}^{p} \hat\beta_{t,k}\, \psi_k(x).
$$
```

GitHub quirks: no space right after the opening `$` or before the closing
`$`; inside a table write `\vert` instead of `|`; write sets as
`\lbrace ... \rbrace`; if `_` or `*` upsets a formula use `` $`x_1^*`$ ``;
`\newcommand` does not carry over between formulas.

**Tables.** Copy the Markdown table written by your experiment script: `ex.save_table(rows, "prices")`
writes `output/<config>/prices.md` next to `prices.csv` (and prints the table):

```markdown
| basis | degree | price | se |
|---:|---:|---:|---:|
| laguerre | 3 | 4.4721 | 0.0071 |
```

**Figures.** Experiment scripts save PNGs in `log/figs/`. Embed with

```markdown
![Price against basis degree, ±2 s.e.](figs/lsm_basis-base.png)
```

`save` then copies the figure into `log/figs/<entry>/` and updates the link.

**Longer derivations.** LaTeX in `log/derivations/`; commit the `.tex` and
the compiled `.pdf`; summarise the result in an entry with a link:
`[derivation](derivations/lower_bound.pdf)`.

## Other commands

```bash
python tools/logtool.py check                  # only check the format
python tools/logtool.py export --format pdf    # whole log as one PDF (needs pandoc + LaTeX)
python tools/logtool.py stats                  # the overview the instructor looks at
```
