# Getting Started — Environment Setup
**SAPA AI Workshop · Block A**

> No local installation needed. Everything runs in GitHub Codespaces — a full VS Code environment in your browser.

---

## What is GitHub Codespaces?

A Codespace is a **cloud-hosted development environment** that runs entirely in your browser. It looks and works exactly like VS Code on your laptop — but Anthropic, Python, and all dependencies are pre-installed for you.

You do not need to install Python, Jupyter, or any packages locally.

---

## Step 1 — Set Your API Key (do this BEFORE launching)

> **Do this first.** Secrets set before launching are automatically available inside the Codespace. If you set it after, you will need to rebuild — which is an extra step.

The workshop uses Claude (Anthropic's AI model). You need an API key to run the notebooks.

1. Go to [github.com/settings/codespaces](https://github.com/settings/codespaces)
2. Under **Secrets**, click **New secret**
3. Fill in:
   - **Name:** `ANTHROPIC_API_KEY`
   - **Value:** your API key (starts with `sk-ant-...`)
4. Under **Repository access**, select the workshop repo
5. Click **Save**

Your key will be injected automatically when the Codespace starts. You will never need to type it again.

> **Don't have an API key yet?** Go to [console.anthropic.com](https://console.anthropic.com) → API Keys → Create Key.

---

## Step 2 — Launch Your Codespace

1. Go to the workshop repository on GitHub (link provided by instructor)
2. Click the green **`< > Code`** button
3. Click the **`Codespaces`** tab
4. Click **`Create codespace on main`**

```
GitHub Repo
    └── < > Code ▼
            └── Codespaces tab
                    └── + Create codespace on main   ← click this
```

> **First launch takes ~2 minutes.** The environment is being built with all dependencies.
> Subsequent launches are much faster.

Once it loads, you will see a VS Code interface in your browser with a file explorer on the left and a terminal at the bottom.

---

## Step 3 — Install Dependencies (in Codespace terminal)

Once your Codespace is running, open the **Terminal** (it's at the bottom of the screen — if you don't see it, press `` Ctrl+` ``).

Type the following command and press Enter:

```bash
uv sync
```

This reads the `pyproject.toml` file and installs all required Python packages into a virtual environment (`.venv/`).

You should see output ending with something like:

```
✓ Installed 42 packages in 8.3s
```

> **What is `uv`?** It is a fast Python package manager. Think of it as a faster, more reliable version of `pip install -r requirements.txt`. You only need to run it once (or after the repo is updated).

---

## Step 4 — Select the Right Python Kernel

This step is critical. Without it, the notebooks will use the wrong Python environment and imports will fail.

1. Open any notebook (e.g. `notebooks/01_hello_agent.ipynb`) by clicking it in the file explorer
2. In the top-right corner of the notebook, you will see a kernel selector — it may say **"Python 3"** or **"Select Kernel"**
3. Click on it
4. A dropdown appears — select **`.venv (Python 3.11.x)`**

```
Top-right of notebook:
    [ .venv (Python 3.11.x) ▼ ]   ← make sure this is selected
```

> **Why does this matter?** The `uv sync` command installed packages into `.venv/`. If you select a different Python, none of the imports will work. Always verify the kernel shows `.venv`.

---

## Step 5 — Verify Everything Works

Open `notebooks/01_hello_agent.ipynb` and run the first cell (`Shift+Enter` to run a cell).

You should see output like:

```
Python: 3.11.x
anthropic: 0.49.0
langgraph: 0.2.x
langchain: 0.3.x

All dependencies loaded successfully!
```

If you see `ModuleNotFoundError` — double check Step 4 (wrong kernel selected).

If you see `ANTHROPIC_API_KEY not set` — double check Step 2.

---

## Quick Reference

| Action | How |
|--------|-----|
| Open terminal | `` Ctrl+` `` |
| Run a notebook cell | `Shift+Enter` |
| Run all cells | `Shift+F10` or Menu → Run → Run All Cells |
| Install/update packages | `uv sync` in terminal |
| Rebuild the Codespace | `Ctrl+Shift+P` → `Codespaces: Rebuild Container` |
| Check your API key is set | `echo $ANTHROPIC_API_KEY` in terminal |

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'anthropic'"**
→ You selected the wrong kernel. Go to Step 4 and select `.venv`.

**"ANTHROPIC_API_KEY not set"**
→ The Codespaces secret wasn't set before launch. In the terminal, run:
`echo "ANTHROPIC_API_KEY=sk-ant-YOUR_KEY" > .env` — then re-run the notebook cell.

**"The Codespace is taking very long to load"**
→ First-time setup can take up to 3 minutes. If it exceeds 5 minutes, try refreshing the page.

**"I closed the terminal by accident"**
→ Press `` Ctrl+` `` to open a new one. Your work is not lost.

**"I'm lost — I don't know where I am"**
→ Click the file icon in the top-left sidebar to open the file explorer.
Find `notebooks/` and click any `.ipynb` file to open it.
