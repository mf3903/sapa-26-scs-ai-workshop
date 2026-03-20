# SAPA AI Workshop
**Vibe, Build, Pitch: Multi-Agent AI for Pharma**

A hands-on 3.5-hour workshop covering multi-agent design patterns and vibe coding.

## Quick Start (GitHub Codespaces)

Click the button below to launch a pre-configured cloud environment — no local setup needed.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/YOUR_ORG/sapa-26-scs-ai-workshop)

The Codespace will automatically:
- Install Python 3.11 + Node.js 20
- Install all Python dependencies
- Install the Claude Code CLI (`claude`)
- Pre-install Jupyter, Pylance, and GitHub Copilot extensions

## Prerequisites (self-attested at registration)

Participants should be comfortable with:
- Running code in VS Code or a cloud IDE
- Basic Git usage (clone, commit, push)
- Python scripting

## API Key Setup

1. Create a `.env` file in the repo root:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```
2. Or set it as a [Codespaces secret](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-secrets-for-your-codespaces) named `ANTHROPIC_API_KEY`.

## Claude Code (optional)

Claude Code is pre-installed in the Codespace. Authenticate with your own Anthropic account:
```bash
claude
```
Each attendee uses their own credentials. No shared keys needed.

## GitHub Copilot (optional)

Copilot is pre-configured. It activates automatically if your GitHub account has Copilot access.

## Workshop Agenda

| Block | Duration | Topic |
|-------|----------|-------|
| A | 20 min | Logistics & Setup — example showcase |
| B | 30 min | Core Hands-On: Multi-Agent System in Jupyter |
| C | 30 min | Vibe Coding & Agentic Development Patterns |
| D | 60 min | Group Build Challenge |
| E | 30 min | Shark Tank Presentations |

## Notebooks

- `notebooks/01_hello_agent.ipynb` — environment check + minimal LangGraph agent
- *(more coming)*

## Local Setup (alternative)

```bash
git clone https://github.com/YOUR_ORG/sapa-26-scs-ai-workshop
cd sapa-26-scs-ai-workshop
uv sync
uv run jupyter lab
```
