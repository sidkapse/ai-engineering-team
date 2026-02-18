# AI Engineering Team

A multi-agent system that turns natural-language requirements into a complete Python solution: a backend module, a design document, a Gradio UI, and unit tests. The crew behaves like a small engineering team—design, backend, frontend, and QA—working in sequence.

## What This Project Does

You provide **high-level requirements** (and optionally a module/class name). The crew:

1. **Designs** — An engineering lead produces a detailed design (classes, methods, behavior) in Markdown.
2. **Implements** — A backend engineer writes a single, self-contained Python module that matches the design.
3. **Builds UI** — A frontend engineer writes a Gradio app that demonstrates the backend.
4. **Adds tests** — A test engineer writes a `test_<module_name>.py` with unit tests for the backend.

Outputs are written under an `output/` directory, so you get a runnable module, a launchable Gradio app, and tests you can run with `python -m test_accounts` or `python -m unittest test_accounts`.

### Example: Trading Account System

Out of the box, the crew is configured to build a **trading account management system**:

- Create an account with an initial deposit
- Deposit/withdraw funds
- Buy/sell shares (with mock prices for AAPL, TSLA, GOOGL)
- Portfolio value, profit/loss, holdings, and transaction history
- Guards against negative balance, overselling, and overbuying

The pre-generated example lives in `output_gpt_4o/`: `accounts.py`, `accounts.py_design.md`, `app.py`, and `test_accounts.py`. You can run that example without re-running the crew (see [Running the Generated App](#running-the-generated-app)).

---

## Project Structure

```
ai-engineering-team/
├── README.md                 # This file
├── pyproject.toml            # Project metadata and dependencies (CrewAI, Gradio, LiteLLM)
├── src/
│   └── ai_engineering_team/
│       ├── main.py           # Entry point: defines requirements, module_name, class_name; runs crew
│       ├── crew.py           # Crew definition: agents, tasks, sequential process
│       ├── config/
│       │   ├── agents.yaml   # Roles, goals, and LLM settings for each agent
│       │   └── tasks.yaml   # Task descriptions, expected outputs, and output file paths
│       └── tools/
│           └── custom_tool.py  # Optional custom tool (template)
├── output_gpt_4o/           # Example output from a previous run (trading account)
│   ├── accounts.py          # Backend module
│   ├── accounts.py_design.md
│   ├── app.py               # Gradio UI
│   └── test_accounts.py     # Unit tests
└── output/                  # Default output directory when you run the crew (created on first run)
```

---

## Prerequisites

- **Python** 3.10, 3.11, or 3.12 (see `requires-python` in `pyproject.toml`; 3.13 may work but is not guaranteed).
- **OpenAI API key** — agents use `openai/gpt-4o` by default (via LiteLLM).
- **Package manager** — [uv](https://docs.astral.sh/uv/) (recommended) or `pip`.

---

## Installation

### Option 1: Using uv (recommended)

From the **project root** (`ai_engineering_team/`):

```bash
# Install uv if you don't have it
pip install uv

# Create a virtual environment and install the project and dependencies
uv venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
uv pip install -e .

# Or use CrewAI’s installer (if you use crewai CLI)
crewai install
```

### Option 2: Using pip

```bash
cd /path/to/ai_engineering_team
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -e .
```

---

## Configuration

### API key

Create a `.env` file in the project root (`ai_engineering_team/`) and add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-your-key-here
```

CrewAI/LiteLLM will read this when the agents run. **Do not commit `.env`**; add it to `.gitignore` if it isn’t already.

---

## Running the Crew

From the **project root** (`ai_engineering_team/`), with the virtual environment activated:

```bash
# Using the crewai CLI (if you ran crewai install)
crewai run

# Or using the project’s entry point
run_crew
# or
ai_engineering_team
```

This will:

1. Load the requirements and settings from `main.py` (see [Customizing the Run](#customizing-the-run)).
2. Run the four agents in sequence: design → code → frontend → tests.
3. Write outputs into the paths defined in `config/tasks.yaml` (by default under `output/`, with filenames derived from `module_name`).

Run times are on the order of several minutes depending on API latency. The agents are verbose by default, so you’ll see their steps in the terminal.

---

## Running the Generated App and Tests

After a run, you’ll have (for the default “accounts” example) something like:

- `output/accounts.py`
- `output/accounts.py_design.md`
- `output/app.py`
- `output/test_accounts.py`

(Or the same structure under a custom output directory if you changed paths in `tasks.yaml`.)

### Run the Gradio app

```bash
cd output   # or output_gpt_4o to use the included example
uv add gradio #optional
uv run app.py
```

Then open the URL shown in the terminal (e.g. `http://127.0.0.1:7860`) in your browser.

### Run the unit tests

```bash
cd output   # or output_gpt_4o
python -m pytest test_accounts.py -v
# or
python -m unittest test_accounts
```

---

## Customizing the Run

All run-time inputs are set in **`src/ai_engineering_team/main.py`**:

- **`requirements`** — Multi-line string describing what the system should do. This is passed to the engineering lead and all other agents.
- **`module_name`** — Name of the Python module file (e.g. `"accounts.py"`). Used in task prompts and output filenames.
- **`class_name`** — Name of the main class in that module (e.g. `"Account"`).

Edit these and run the crew again to generate a different module and UI (e.g. a different domain, still one module and one main class).

You can also:

- **Agents:** Edit `src/ai_engineering_team/config/agents.yaml` to change roles, goals, or LLM (e.g. switch model).
- **Tasks:** Edit `src/ai_engineering_team/config/tasks.yaml` to change task descriptions, expected outputs, or output file paths.
- **Crew logic:** Edit `src/ai_engineering_team/crew.py` to add tools, change process (e.g. hierarchical), or adjust agent options (e.g. `allow_code_execution`).

---

## The Agents (Summary)

| Agent               | Role summary                         | Config in `agents.yaml` |
|---------------------|--------------------------------------|--------------------------|
| **Engineering lead**| Turns requirements into a design doc | `engineering_lead`       |
| **Backend engineer**| Implements the design in one module  | `backend_engineer`       |
| **Frontend engineer** | Builds Gradio app for the backend  | `frontend_engineer`      |
| **Test engineer**   | Writes unit tests for the module     | `test_engineer`          |

All use `openai/gpt-4o` by default. Backend and test engineers have code execution enabled (safe mode) so they can validate behavior.

---

## Dependencies

- **crewai[tools]** — Multi-agent framework and tools.
- **gradio** — For the generated demo UIs.
- **litellm** — For model routing (e.g. `openai/gpt-4o`).

See `pyproject.toml` for exact versions.

---

## Troubleshooting

- **“No OPENAI_API_KEY”** — Add `OPENAI_API_KEY` to a `.env` file in the project root.
- **Output not where you expect** — Check `output_file` in `config/tasks.yaml`; paths are relative to the project root unless you change them.
- **Import errors when running `app.py` or tests** — Run them from the directory that contains the generated module (e.g. `output/` or `output_gpt_4o/`) so that `from accounts import Account` (or your module name) resolves.
- **Syntax or runtime errors in generated code** — You can fix the generated files by hand or adjust the task descriptions in `tasks.yaml` and re-run the crew.

---

## References

- [CrewAI documentation](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [Gradio documentation](https://www.gradio.app/docs)
