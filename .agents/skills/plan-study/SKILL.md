---
name: plan-study
description: Create or revise an adaptive course-level study plan from a syllabus and learning materials, including a diagnostic, dependency map, schedule, assessment alignment, and progress files. Use when starting or replanning a subject or course. Do not use to teach an individual lesson or make a simple task list.
---

# Plan Study

Build a course plan that is complete enough to guide later teaching without pre-writing the lessons. The plan must connect the learner's actual frontier, the course requirements, trustworthy sources, practical evidence, assessment demands, and available study time.

## Required pedagogical dependency

Before taking planning actions, read [`../teach/SKILL.md`](../teach/SKILL.md) completely and obey it as the normative teaching contract. Do not copy its philosophy into this skill.

This skill owns course discovery, diagnosis, planning, persistence, and handoff. `teach` owns the teaching of each approved node.

Non-negotiable consequences of that boundary:

- Never skip the learner-level probe or replace it with self-reported confidence alone.
- A final plan requires both a floor and a ceiling for every goal-relevant prerequisite strand.
- Build a small dependency DAG from truths the learner can safely accept, not from the source material's chapter order.
- Present the approach and DAG, then stop for approval before teaching.
- Do not create lesson bodies for future nodes. Create a numbered lesson file only when that node begins.

## 1. Resolve the course and inspect existing state

Identify the topic root from the user's request. If it is ambiguous and cannot be discovered from the workspace, ask for the path.

Before writing:

1. Inspect existing `initial.md`, `probe.md`, `plan.md`, `content/00-index.md`, and session context that clearly applies to this learner.
2. Preserve user answers, corrections, progress, and unrelated files. Update existing artifacts narrowly; never replace them wholesale merely to match a template.
3. Inventory the syllabus, lectures, books, exercises, rubrics, deadlines, and existing notes.
4. When PDFs are present, run `python3 <this-skill>/scripts/audit_materials.py <topic-root>` if its dependencies are available. Inspect every warning rather than treating the report as proof of completeness.
5. Read the official syllabus in full. Read the portions of other materials needed to map coverage, prerequisites, source quality, and assessment—not entire books without a planning reason.

Record missing, suspicious, duplicate, unreadable, or outdated material. A missing deadline blocks a dated calendar, but not a clearly labeled relative plan.

## 2. Separate scope authority from factual authority

Use the official course documents to determine what the institution expects and assesses. Do not assume they are the strongest factual source.

Default source order:

1. syllabus, rubric, and current AVA calendar for scope, weights, and deadlines;
2. course lectures for instructor emphasis and vocabulary;
3. assigned textbooks for explanations and conceptual verification;
4. current standards, RFCs, specifications, or official documentation for normative and time-sensitive claims;
5. secondary sources only to fill a justified gap.

Record meaningful contradictions or outdated claims in the plan. Preserve what is likely to be assessed while labeling the technically correct model explicitly. Never silently blend conflicting claims.

## 3. Establish the learner contract and probe

Reuse facts already established in current, applicable context. Ask only for missing information that changes the plan, such as:

- desired outcome and required depth;
- assessment dates and fixed deadlines;
- time per session and sessions per week;
- available lab environment and constraints;
- whether an existing plan is being started, resumed, or repaired.

Follow `teach`'s question boundary: use preference questions for genuine choices and graded questions for diagnostic checks. Use the harness's structured question capability when available; otherwise ask in chat while preserving the same semantic distinction.

Probe every prerequisite strand the course plan will rely on. Adapt difficulty until each strand is bracketed by demonstrated knowledge below and a miss or genuine uncertainty above. Investigate confident misconceptions before planning around them. Save raw answers and the resulting diagnosis; do not reduce the probe to a score.

## 4. Research and construct the plan

Before fixing the graph, use the `researcher` agent required by `teach` when available to verify the field, roots, standard framing, and common misconceptions. Give it the course goal and only the source context it needs. If the agent is unavailable, perform the equivalent check against high-trust primary sources and disclose the limitation rather than pretending verification occurred.

Design the learning order from dependencies, even when it differs from lecture order. Preserve traceability back to lecture units and assessments so the learner remains prepared for the institution's sequence.

For every planned node specify:

- why it is needed now;
- prerequisites and outgoing dependency edges;
- observable learning outcome;
- course requirement and source anchors;
- estimated number of study sessions, expressed as a range when uncertain;
- one conceptual check that exposes reasoning;
- one practical or explanatory artifact when the subject supports it;
- completion evidence and the nearest milestone it enables.

Prefer reconstruction, transfer, explanation, and troubleshooting over recall-only work. Use objective-question practice for objective assessments, but do not let exam rehearsal replace understanding.

Create a schedule from session estimates, the learner's availability, prerequisite order, review capacity, and real deadlines. Do not invent dates, page references, tooling, or course requirements.

## 5. Write the planning artifacts

Read [`references/plan-schema.md`](references/plan-schema.md) before creating or substantially revising planning files. It defines the artifact responsibilities, traceability fields, states, and minimum completeness checks.

Use the learner's language. Follow the topic's established Markdown and Obsidian conventions. Keep one canonical copy of each fact; link between artifacts rather than duplicating large sections.

Treat Obsidian links as the persisted form of the dependency graph:

- assign every node a stable lesson filename when planning it, using `<two-digit-node>-<slug>.md`;
- write every planned lesson and milestone in `content/00-index.md` as a wikilink, even before its file exists;
- keep lesson metadata synchronized with the plan's immediate prerequisite edges;
- use vault-root-relative wikilink targets whenever a bare filename would be ambiguous;
- never replace a semantic dependency with a mere previous/next sequence link.

After writing, present in chat:

1. a short prose explanation of the chosen order, tied to the diagnostic and goal;
2. the small Mermaid dependency DAG;
3. unresolved risks or missing inputs that materially affect the plan.

Then wait for explicit approval. Mark the plan approved only after that checkpoint.

## 6. Handoff after approval

Initialize or update `content/00-index.md` with statuses and wikilinks, but leave future lesson files absent. Unresolved wikilinks represent planned nodes without creating empty lesson files. Select the first ready node whose prerequisites are verified and hand teaching back to `teach`.

When revising later, distinguish a local adjustment from a dependency failure. If a prerequisite failure invalidates downstream order, update the DAG, schedule, and affected traceability entries together; preserve completed work and explain the change.
