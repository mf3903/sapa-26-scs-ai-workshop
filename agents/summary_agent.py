"""
Summary Agent — synthesizes findings from all specialist agents into a final report.
Exposed as a LangGraph node function: summary_node(state) -> state update.
"""
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

SYSTEM_PROMPT = """You are a senior medical writer producing structured safety reports.

You will receive:
- The original adverse event report
- A severity assessment from the Severity Agent
- A compliance assessment from the Compliance Agent

Synthesize these into a structured report with three sections:
1. **Severity Summary** — key severity findings and score
2. **Compliance Status** — whether the report is complete, any gaps
3. **Recommended Action** — one clear next step (e.g. "Submit as is", "Obtain missing onset date before submission")

Keep the report under 200 words. Be direct and actionable."""

_llm = ChatAnthropic(model="claude-haiku-4-5-20251001")


def summary_node(state: dict) -> dict:
    """LangGraph node: synthesizes all findings into a final structured report."""
    prompt = f"""Original Report:
{state['report']}

Severity Assessment:
{state['severity_analysis']}

Compliance Assessment:
{state['compliance_analysis']}

Please produce the structured safety report."""

    response = _llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ])
    return {"final_report": response.content}
