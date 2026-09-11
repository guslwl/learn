# Study-plan artifact contract

Use this contract when creating a new course plan or making a substantial revision. Existing topic conventions take precedence when they preserve the same information.

## Lifecycle

A topic moves through these states:

1. `discovery` — sources and constraints are being inventoried;
2. `probing` — prerequisite strands are not all bracketed;
3. `draft` — the plan exists but has not been approved;
4. `approved` — the learner approved the approach and dependency DAG;
5. `teaching` — at least one approved node has started;
6. `replanning` — new evidence invalidated part of the approved plan;
7. `complete` — all required outcomes have completion evidence.

Do not skip from `discovery` to `approved`. Store the current state in `content/00-index.md` once that file exists; before then, state it in `plan.md`.

## `initial.md` — learner and course contract

Keep stable inputs here:

- learner's own reason for studying the subject;
- desired capability at the end, stated observably;
- known background and relevant prior experience;
- time per session and sessions per week;
- assessment dates or an explicit `not provided` marker;
- practical environment, tool constraints, and accessibility needs;
- links to the official course documents.

Preserve the learner's wording when it carries intent. Do not turn inferred preferences into facts.

## `probe.md` — diagnostic evidence

Keep both the evidence and the conclusion:

- prerequisite strands and why each matters;
- questions in the order asked;
- learner answers and stated confidence;
- corrections or follow-up questions;
- demonstrated floor and observed ceiling per strand;
- confident misconceptions that the plan must repair;
- planning consequences.

A percentage score is optional and never substitutes for the floor/ceiling analysis.

## `plan.md` — canonical approved design

Use the following sections unless an existing local structure is clearer.

### Status and planning basis

Include lifecycle state, last revision date, current approval status, learner availability, and inputs still missing.

### Goal and completion criteria

State what the learner will be able to explain, distinguish, build, configure, diagnose, or evaluate. Each criterion must have observable evidence.

### Material audit and source policy

List:

- required course documents and whether each was found/read;
- incomplete, suspicious, unreadable, duplicate, or stale material;
- the source hierarchy used for this course;
- discrepancies that can affect teaching or assessment.

### Diagnostic summary

Summarize the relevant frontier and link to `probe.md`. Do not duplicate all answers.

### Coverage and traceability matrix

Every official skill, competency, content unit, and assessed deliverable must map to the learning plan.

| Official requirement | Learning node(s) | Source anchors | Completion evidence | Assessment |
|---|---|---|---|---|

Use a stable requirement identifier when the syllabus provides none, for example `H1`, `C2`, or `U4.3`. A source anchor is a document plus page, section, chapter, or another locator that can be verified. Never fabricate page numbers.

### Dependency DAG and rationale

Include a small Mermaid graph containing roots, major derived nodes, milestones, and the final goal. Follow it with concise prose explaining departures from the institution's presentation order.

### Learning nodes

Give every node a stable number and slug. For each node record:

- outcome;
- motivation;
- prerequisites;
- source anchors;
- estimated sessions;
- conceptual check;
- practical or explanatory artifact;
- completion evidence;
- milestone connection.

The number and slug determine the future lesson filename: `<two-digit-node>-<slug>.md`. Once assigned, keep it stable so Obsidian links do not drift.

Plan the node; do not write its lesson.

### Schedule

Show sessions or weeks, planned nodes, reviews, milestones, assessment preparation, and buffer. Use relative labels until authoritative dates are available. If dates change, preserve node estimates and recompute only the calendar layer.

### Assessment strategy

Map assessment format and weight to preparation evidence. Cover objective, discursive, and practical demands separately. Do not equate assessment weight mechanically with study-time percentage; prerequisites and learner gaps also determine effort.

### Milestones and capstone

Each milestone should integrate multiple established nodes and produce inspectable evidence. State prerequisites, artifact, success criteria, and which official requirements it covers.

### Risks and open inputs

Record material gaps, uncertain claims, unavailable tools, missing dates, and assumptions. State the effect and the next resolution step for each.

### Approval record

Record whether the learner approved the plan and any requested changes. Do not infer approval from silence or from approval of an earlier version.

## `content/00-index.md` — live execution state

Keep this file compact:

- link to `plan.md`;
- lifecycle state;
- legend for node statuses;
- every planned node and milestone in dependency order;
- current node and next ready node;
- blocked nodes with the unmet prerequisite;
- last verified progress.

Write every node and milestone name as a wikilink to its stable future filename. A planned node may remain an unresolved wikilink; do not create an empty file merely to satisfy the link.

Recommended statuses:

- `planned` — approved but not started;
- `ready` — prerequisites verified;
- `in-progress` — lesson file exists and teaching began;
- `needs-repair` — verification exposed a prerequisite gap;
- `verified` — completion evidence accepted;
- `blocked` — an external input or unmet prerequisite prevents progress.

Only `in-progress`, `needs-repair`, or `verified` nodes should normally have numbered lesson files.

## Obsidian graph contract

Every numbered lesson file begins with YAML properties in this shape:

```yaml
---
type: lesson
topic: <topic-slug>
node: N<number>
status: <execution-status>
prerequisites:
  - "[[topics/<topic-slug>/content/<prerequisite-file>|<human title>]]"
related:
  - "[[topics/<topic-slug>/content/<related-file>|<human title>]]"
tags:
  - topic/<topic-slug>
  - type/lesson
---
```

Rules:

- `prerequisites` contains only immediate incoming dependencies from the approved DAG; transitive prerequisites would add redundant graph edges.
- Use `prerequisites: []` for a root node.
- `related` is optional and contains only meaningful non-dependency connections; omit it when empty.
- Use vault-root-relative targets so duplicate filenames in different topics cannot resolve incorrectly.
- `status` matches `content/00-index.md` and is updated when execution state changes.
- The topic index links to every planned node; lessons do not add artificial previous/next links merely to create a denser graph.
- Image embeds already link a lesson to its topic-local attachment. Do not add a second ordinary link to the same image.
- If replanning changes an immediate dependency, update the plan DAG, the index, and the affected lesson properties together.

## Completeness check

Before presenting a draft, confirm that:

- every goal-relevant diagnostic strand has a floor and ceiling;
- every official requirement appears in the traceability matrix;
- every node has prerequisites, evidence, and source anchors;
- the DAG is acyclic and matches the written order;
- session estimates fit the stated availability;
- dated schedules use authoritative dates;
- assessment formats and weights are represented accurately;
- material gaps and source conflicts are visible;
- future lesson bodies were not created;
- every planned index entry is a wikilink to its stable filename;
- every existing lesson has graph properties whose immediate prerequisites match the DAG;
- the plan is still marked `draft` until explicit approval.
