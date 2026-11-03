# Install and get started

[简体中文](install.md) · [Home](../README.md)

Lynette Thinking is a set of instructions and reference materials for an AI assistant. Bring your own Codex or an assistant that supports skills. It has no standalone model or project account and requires no project-specific API key. The steps below are for Codex.

## Install in one step

Download and extract the repository, then run from the root containing `README.md` (Python 3.9+):

```sh
python3 scripts/install.py
```

The script only copies local files to `~/.agents/skills/lynette-thinking`. It makes no network calls and does not overwrite an existing directory.

If a skill with this name is already installed, review and back up that version before deciding which copy to replace. Avoid duplicate copies with the same name across discovery locations.

## Install for a project or copy manually

To install for a project, specify the destination from that project:

```sh
python3 /path/to/extracted-repository/scripts/install.py --target .agents/skills/lynette-thinking
```

Replace `/path/to/extracted-repository` with the actual extracted location.

Without Python, manually copy the complete `skills/lynette-thinking/` folder from the repository to the destination. A personal installation should end at `~/.agents/skills/lynette-thinking/SKILL.md`; a project installation should end at `.agents/skills/lynette-thinking/SKILL.md`.

## Your first conversation

After installation, your very first request in Codex can simply describe a concrete dilemma:

> A friend lent me a venue for a book club and now wants to decide the theme. We haven't discussed responsibilities. I want to keep my own direction without falling out on the spot.

Workplace, family, and friendship dilemmas about what to do or say fall within the automatic matching scope; you do not need to mention Lynette. Selection depends on the host and model. To choose it explicitly, or if it is not selected, write:

> Use $lynette-thinking to help me decide my next step: …

You do not need to repeat the name when adding context to the same problem. If a new installation does not appear, restart Codex and check the folder location.

[More ways to ask and add context](../skills/lynette-thinking/README.en.md) · [Usage examples](../skills/lynette-thinking/examples/guided-resolution.en.md)

Discovery locations and behavior follow the [official OpenAI documentation](https://learn.chatgpt.com/docs/build-skills). This package provides direct skill installation. For other assistants, follow their own installation process; compatibility has not been verified across all hosts.

## Your information and removal

The skill has no telemetry, background process, or upload code. Your assistant processes the conversation under its own data policies. When describing a real situation, use roles instead of names and omit employers, contact details, and unrelated chat records.

To remove it, delete only the installed `lynette-thinking` folder, not the surrounding skills directory.
