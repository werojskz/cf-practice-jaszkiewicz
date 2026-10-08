# Reading notes and plan

- **Date:** 2026-10-08
- **Author:** Weronika Jaszkiewicz
- **Code:** n/a

## Goal
Review the project workflow, log format, and repository conventions before starting the computational finance exercises.

## Method
I read the repository guidance files and the log template to understand the required entry structure and the Git identity check used by the project tooling.

## Code and runs
n/a

## Results
The repository expects the Git author name to match the member listed in `project.json`. In this project, the member name is "Weronika Jaszkiewicz" and the Git name must be set accordingly before saving a log entry.

## Interpretation
The warning is not a code issue but a Git configuration issue. The project compares the local Git user name with the project member list and blocks the save step unless they match.

## Next steps
Set the global Git identity, then run the log save command to record this entry and continue with the project tasks.

## AI assistance
No AI-generated code was used for this step; I checked the project config and the logtool validation logic directly.
