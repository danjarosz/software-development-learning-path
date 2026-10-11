# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A learning plan (software-engineering skills, written in Polish) prepared for deployment to Linear, team **LEA**. Not an application: the "code" is one deploy script, the data is one JSON file, and the rest is Markdown for human review. Nothing has been created in Linear yet. It isn't a git repository.

- `linear-plan.json` is the machine-readable plan that `deploy_linear.py` consumes.
- `00-kolejnosc-i-zaleznosci.md` is the overview: how the plan maps to Linear, prerequisites, starting points, project order and the cross-project task relations.
- `01-…md` to `22-…md` hold one Linear project each: project fields and description, milestones, start task, dependency flow, tasks per milestone, relations to other projects.

The JSON and the Markdown files contain the same data, and the generator that produced them is not in this directory. **An edit to a project, milestone, task or relation has to go into `linear-plan.json` and into the matching `NN-*.md` file, and into `00-…md` when it changes order, cross-project relations or counts.** Counts are quoted in several places: 22 projects, 153 milestones, 985 tasks, 1779 "blocks" relations, plus per-project totals in each file's "W skrócie" line and in the `00` table.

## Commands

The script needs only Python 3.9+ and the standard library.

```bash
python3 deploy_linear.py --dry-run          # print plan counts and resume state; makes no API calls
export LINEAR_API_KEY=lin_api_...
python3 deploy_linear.py                    # deploy to Linear (options: --team LEA, --plan, --pause 0.25)
```

There are no tests or linter. To validate the JSON after an edit, run `--dry-run` and check the graph yourself: every `blockedBy` key exists, there are no cycles, and only `S01-START` and `S02-START` have no blockers.

## Data model (`linear-plan.json`)

- `projects[]`: `key` (`S01`…`S22`), `name`, `summary` (truncated to 255 chars as the Linear summary), `description` (Markdown, used as project content), `start`/`target` dates, `label` (`warstwa-0`…`warstwa-8`), `blockedBy` (informational only, the script doesn't deploy it), `milestones[]` (`key`, `name`, `description`).
- `issues[]`: `key`, `project`, `milestone` (null for start tasks), `title`, `description`, `labels`, `status` (`Todo` or `Backlog`), `blockedBy` (list of issue keys).

Key conventions (provisional; Linear assigns `LEA-…` identifiers on deploy):

| Pattern | Meaning |
|---|---|
| `Snn-START` | the project's single entry task, label `start` |
| `Snn-Ek` / `Snn-Uk` | milestone: learning stage k / supplementary path k (sections 12, 17, 20) |
| `Snn-Ek-Mi` | material, label `materiał` (plus `płatny`, `opcjonalne`, `ścieżka uzupełniająca` where they apply) |
| `Snn-Ek-D` | stage proof (`dowód`), which closes the milestone |
| `Snn-Ek-Pi` | ongoing practice (`praktyka`) from the expert stage |

Dependency rules, which edits must preserve:
- The start task blocks every task in the first stage and the supplementary paths.
- A start task is blocked by the proof (`-D`) of the prerequisite projects' stage that gets the skill to working level. Prerequisite projects don't have to be finished first.
- Within a stage, materials run in parallel and all of them block that stage's proof. The proof blocks the next stage's materials.
- Some stages have extra cross-project blockers (for example, Rust-dependent stages wait on `S12-E2-D`). They are listed in section 5 of `00-…md`.
- Optional stages (TinyML and embedded Linux/Zephyr in sections 21 and 22) block nothing.
- Only `S01-START` and `S02-START` are `Todo`; everything else is `Backlog`.

## `deploy_linear.py` behavior

- It deploys in this order: team states, then issue labels (`ISSUE_LABELS` defines their colors), project labels, projects and milestones, issues, `blocks` relations, and finally `mapowanie-kluczy.csv` (key to `LEA-…` identifier).
- It can resume. The IDs of everything it creates are saved to `linear-deploy-state.json` after each object, and keys already in that file are skipped. Deleting the file or changing keys after a partial deploy leads to duplicates in Linear.
- It retries with backoff on rate limits, 5xx responses and network errors.
- It doesn't create project-level dependencies. The script tells the user to add them by hand.
- Linear's Free plan caps a workspace at 250 issues, so this plan needs a paid plan.

## Writing conventions

All content, script output messages and comments are in Polish. Keep that language and the existing style, such as `„…”` quotes and the `·` separator in "`KEY` · Title" references. Inline code uses backticks.
