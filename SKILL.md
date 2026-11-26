---
name: anylogic-modeling
description: Create, modify, review, and validate native AnyLogic simulation projects on Windows, especially in PLE. Use for ALP or ALPX editing, model experiments, and multilevel pedestrian modeling.
---

# AnyLogic Modeling

Deliver the native model and its required resources. Keep AnyLogic's flowchart, markup, agent lifecycle, and simulation clock. Use external scripts to author files, check references and process results.

## Workflow

1. Identify the installed build, license edition, requested file format, and validation access. Use [local API and edition notes](references/runtime-and-api.md) when these affect the approach.
2. Preserve the input and work on a sibling copy or a separate directory. For new layouts, start with a small editor-generated project or a locally installed official example. Inspect the smallest editable element before duplicating it. For file editing or conversion, read [ALP and ALPX](references/project-files.md).
3. Test a single movement before scaling the model. For multilevel modeling, read [pedestrian and building models](references/pedestrian-models.md). For local examples, use [the generator and verification commands](references/lab-workflow.md).
4. Set the experiment horizon and seed. Define each statistic's event and denominator. Read [experiments and data](references/experiments-and-data.md) for CSV and external integration.
5. Report separately what was structurally checked, compiled by PLE, observed during a run, and visually verified. Trace problems to the first failing phase using [troubleshooting](references/troubleshooting.md). For manually controlled PLE sessions, hand over concise F7/F5 steps and check the resulting files when available.

Prefer local API signatures over online code snippets when the installed version disagrees. Use the experimental labels in the references to distinguish vendor documentation, observed local evidence, and work that still needs a native run.
