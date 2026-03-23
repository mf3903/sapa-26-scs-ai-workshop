# Block B — Multi-Agent AI Systems
**SAPA AI Workshop · Vibe, Build, Pitch: Multi-Agent AI for Pharma**

> **Learning Objectives**
> By the end of this block you will be able to:
> - Explain the difference between an AI assistant and an AI agent
> - Name the 4 core components of an agent
> - Describe the ReAct loop in plain language
> - Read a LangGraph pipeline and understand what each part does

---

## 🎯 What Are We Building Today?

Before diving into concepts, let's look at the destination.

By the end of Block B you will have seen — and run — a **Clinical Trial Safety Analyzer**: a multi-agent system that reads an adverse event report and produces a structured safety assessment.

```mermaid
graph TD
    Input([📄 Adverse Event Report]) --> Orchestrator

    subgraph LangGraph Pipeline
        Orchestrator[🧠 Orchestrator\nReads the report, coordinates agents]
        Orchestrator --> Severity[⚠️ Severity Agent\ncalculate_severity_score tool]
        Orchestrator --> Compliance[📋 Compliance Agent\ncheck_required_fields tool]
        Severity --> Summary
        Compliance --> Summary[📝 Summary Agent\nSynthesizes findings]
    end

    Summary --> Report([✅ Structured Safety Report])
```

Every concept below is a building block toward this system.

---

## 🤖 AI Assistant vs AI Agent

These terms are often used interchangeably — but they describe fundamentally different systems.

An **AI assistant** takes your input, generates a response, and stops. It is reactive. It waits for you to give it the next instruction.

An **AI agent** is different. It receives a goal, reasons about what to do, takes an action, observes the result, and then decides what to do next — repeating this loop until the goal is complete. It is autonomous.

```mermaid
flowchart LR
    subgraph assistant["💬 AI Assistant"]
        direction LR
        Q[Input] --> R[Response] --> Stop([Done])
    end

    subgraph agent["🤖 AI Agent"]
        direction LR
        T[Goal] --> Reason[Reason]
        Reason --> Act[Act]
        Act --> Observe[Observe]
        Observe --> Reason
        Observe -->|goal met| Output([Done])
    end
```

> **Pharma analogy:**
> An assistant answers *"What are the side effects of metformin?"*
> An agent reads an adverse event report, scores its severity, checks for missing fields, and writes a structured summary — without you telling it each step.

---

## 🧩 The 4 Core Components of an AI Agent

Every agent — regardless of framework — is built from the same four parts.

```mermaid
graph TD
    LLM["🧠 LLM\nReasoning & Planning"] <--> Agent((Agent))
    Tools["🔧 Tools\nExternal Actions"] <--> Agent
    Memory["💾 Memory\nContext & History"] <--> Agent
    Persona["🎭 Persona\nRole & Expertise"] --> Agent
```

| Component | What it does | In our system |
|-----------|-------------|---------------|
| **LLM** | Reasons, plans, generates text | Claude — reads the AE report and decides what to do |
| **Tools** | Functions the agent can call | `calculate_severity_score()`, `check_required_fields()` |
| **Memory** | Keeps context across steps | The LangGraph **State** — a shared dict all nodes read/write |
| **Persona** | System prompt that defines the agent's role | *"You are a pharmacovigilance specialist..."* |

> **Key insight:** Tools are what make agents useful beyond text generation.
> Without tools, the agent can only reason. With tools, it can *act*.

---

## 🔄 The ReAct Loop

ReAct stands for **Reason + Act**. It is the fundamental operating cycle of any autonomous agent.

```mermaid
flowchart LR
    Input([Task]) --> Reason
    Reason["💡 Reason\nWhat should I do next?"] --> Act
    Act["⚙️ Act\nCall a tool / generate output"] --> Observe
    Observe["👁️ Observe\nWhat happened? What do I know now?"] --> Reason
    Observe -->|task complete| Output([Result])
```

**Reason** — The LLM analyzes the current situation and plans the next step.

**Act** — The agent executes: calls a tool, makes an API request, or generates content.

**Observe** — The agent sees the result and feeds it back into the next reasoning cycle.

This loop repeats until the task is done — or until the agent decides it cannot proceed.

> **Why this matters for LangGraph:**
> LangGraph doesn't hide this loop — it makes it *explicit and inspectable*.
> Each node in the graph is a step in this cycle. You control exactly when and how agents reason, act, and observe.

---

## 🗺️ Introducing LangGraph

LangGraph is a framework for building agents as **state machines** — directed graphs where each node is an agent or function, and edges define how information flows.

> **Mental model:** Think of your agent pipeline as a flowchart where the "clipboard" (shared State) gets passed from desk to desk, and each person adds their findings before handing it on.

```mermaid
graph LR
    A([Start]) --> B[Node A]
    B -->|edge| C[Node B]
    C -->|conditional edge| D[Node C]
    C -->|conditional edge| E[Node D]
    D --> F([End])
    E --> F
```

**Why LangGraph over a simple chain?**

| | Simple Chain | LangGraph |
|---|---|---|
| Control flow | Fixed, linear | Conditional branching, loops |
| Inspectability | Black box | Inspect state at every step |
| Multi-agent | Hard to coordinate | First-class support |
| Error handling | Minimal | Define explicit error edges |

---

## 🔑 LangGraph Vocabulary

Five concepts you need to read any LangGraph pipeline:

```mermaid
graph TD
    State["📋 State\nTypedDict — the shared clipboard\npassed through every node"] --> NodeA
    NodeA["🔵 Node\nA Python function or agent\nreads State, writes to State"] -->|"➡️ Edge\nFixed handoff"| NodeB
    NodeB["🔵 Node"] -->|"🔀 Conditional Edge\nDynamic routing based on State"| NodeC["🔵 Node C"]
    NodeB -->|"🔀 Conditional Edge"| NodeD["🔵 Node D"]
```

| Term | One-line definition |
|------|-------------------|
| **State** | A typed Python dict shared by all nodes — think of it as the running file for the case |
| **Node** | A function that receives State, does work, and returns updated State |
| **Edge** | A fixed transition — "always go from Node A to Node B" |
| **Conditional Edge** | A dynamic transition — "go to Node B *or* Node C depending on what's in State" |
| **Graph** | The compiled pipeline — call it like a function to run the whole thing |

---

## 🏗️ Multi-Agent Orchestration

A single agent trying to do everything leads to overloaded context, hard-to-debug behavior, and brittle outputs.

**The better pattern: one orchestrator + specialized sub-agents.**

```mermaid
graph TD
    subgraph single["❌ Single Agent — Does Everything"]
        SA[One Agent] -->|overloaded| Problems["Errors\nHard to debug\nUnreliable"]
    end

    subgraph multi["✅ Multi-Agent — Specialist Team"]
        Orch[🧠 Orchestrator\nCoordinates & synthesizes]
        Orch --> A1[Specialist A]
        Orch --> A2[Specialist B]
        Orch --> A3[Specialist C]
        A1 & A2 & A3 --> Orch
        Orch --> Out[Reliable output]
    end
```

**In LangGraph**, the orchestrator is just another node — one whose job is to read the full State and route to the right specialist.

Each specialist gets a **focused system prompt** (persona), **specific tools**, and writes its findings back to **State** — where the next node can read them.

---

## 🧪 Our Demo System — Full Picture

Here is how the vocabulary maps to actual code you'll run in the notebooks:

```mermaid
graph TD
    Input([📄 AE Report text]) --> S

    subgraph Graph["LangGraph Pipeline"]
        S["📋 State\n{ report, severity_analysis,\ncompliance_analysis, final_report }"]
        S --> N1

        N1["⚠️ severity_node\nSeverity Agent\n+ calculate_severity_score tool\n+ lookup_drug_class tool"]
        N1 -->|writes severity_analysis to State| N2

        N2["📋 compliance_node\nCompliance Agent\n+ check_required_fields tool"]
        N2 -->|writes compliance_analysis to State| N3

        N3["📝 summary_node\nSummary Agent\nno tools — reads all findings"]
        N3 -->|writes final_report to State| End
    end

    End([✅ Final Report])
```

> **Notice:** adding a new specialist = adding one node + one edge. Everything else stays the same.
> This is the power of the graph pattern.

---

## 💻 Getting Hands-on

Open the notebooks in order:

**1. `notebooks/02a_agent_basics.ipynb`** ← Start here
- Build a single agent with a persona and a tool
- See the ReAct loop in action
- ~5 min to run through

**2. `notebooks/02b_orchestration.ipynb`** ← Then here
- The full Clinical Trial Safety Analyzer
- Agents are imported from `agents/` — notice the abstraction
- Run the full pipeline on a synthetic AE report
- ~10 min to run through

After Block B: Block D gives you 60 minutes to add your own agent to this system.
