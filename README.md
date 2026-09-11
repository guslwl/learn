# learn

> This repo is a fork of [amosblomqvist/learn](https://github.com/amosblomqvist/learn), adapted to how i use it.

This is the setup i use to learn with AI. It covers teaching, course planning, research, and visuals.

## What's included

### Skills

- `.agents/skills/teach/`: the teaching philosophy and lesson process
- `.agents/skills/plan-study/`: adaptive course planning, diagnostics, dependency mapping, scheduling, and progress files -- this is new, i've created it so i can map out my university courses and follow along
- `.agents/skills/visualize/`: guidance for adding a correct, minimal visual when an idea is clearer as a picture

### Agents

- `.agents/agents/researcher/` — verifies facts through focused web research
- `.agents/agents/mermaid-maker/` — creates and visually verifies structural or relational diagrams
- `.agents/agents/svg-maker/` — creates and visually verifies spatial or geometric illustrations

## How to use

### The `teach` skill

1. clone it: `git clone (the url of this repo, which i don't have bc it's offline)`
2. `cd` into it: `cd learn/`
3. create a `topics` folder (if it doesn't exist)
4. inside `topics`, create another directory for the AI to place the content related to that topic. example: `topics/data-analysis`
5. create an `initial.md` file and put in it the initial context for whatever you wanna learn
6. start your harness (agy/codex) and prompt the ai with the following:

   ```text
   Use the context provided by the initial file inside `topics/<your-topic>/initial.md` and use the `teach` SKILL to start PROBING me about it.
   ```

### The `plan-study` skill

Use this one when you want to plan a whole course or subject, not just learn a single topic.

1. create a folder for the course inside `topics`. for example:

   ```text
   topics/
   └── computer-networks/
       ├── initial.md
       ├── syllabus.pdf
       ├── lectures/
       └── books/
   ```

2. put the basic context in `initial.md`: what the course is, why you're studying it, what you already know, how much time you have, and any deadlines you know about
3. add whatever material you have. the syllabus is the most important one, but you can also add lecture slides, books, exercises, rubrics, old exams, etc
4. start your harness from the root of the repo and prompt the ai with:

   ```text
   Use the context and materials inside `topics/computer-networks` and use the `plan-study` SKILL to create a study plan for this course.
   ```

The skill will inspect the material and ask about anything important that is missing. Then it will probe what you actually know -- getting everything right just means it needs to ask harder questions. Once it finds the edge of your knowledge, it creates the plan around that instead of blindly following the order of the syllabus.

It will create or update these files:

- `initial.md`: your goal, background, available time, deadlines, and constraints
- `probe.md`: the questions, your answers, and where your knowledge starts to break down
- `plan.md`: the course map, schedule, sources, assessments, milestones, and dependency graph
- `content/00-index.md`: the live progress tracker for every planned lesson

Before teaching anything, it will show you the approach and a small dependency graph. Check them and say whether you approve the plan. After that, the `teach` skill takes over one lesson at a time. Future lesson files are only created when you actually start them, so the folder doesn't get filled with a bunch of empty notes.

## Notes

The whole thing is meant to work **for** you, not against you. Adjust the skills, agents and whatever else you need to match how you learn, the tools available in your harness, and the conventions of your notes workspace.

I've made a few changes compared to the original version of this repo:

1. Removed everything related to `pi.dev`. i use [agy](https://antigravity.google/) for the most part (because of the [student promo](https://one.google.com/ai-student?g1_landing_page=75)) and [they don't allow third-party auth](https://www.reddit.com/r/PiCodingAgent/comments/1sn5vgv/warning_banned_from_gemini_cli_and_antigravity/), so the original setup didn't make sense for me. i adapted it to the `.agents` pattern instead
2. Added the `.agents/skills/plan-study` skill. it is really useful when you have a bunch of context for a specific course you're studying. maybe worth taking a look
