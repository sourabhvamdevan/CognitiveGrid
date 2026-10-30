"""Regenerate the README diagrams for NexusFlow — Agentic AI Multi-Agent Studio.
Requires: pip install graphviz  +  Graphviz `dot` binary.

    python scripts/generate_diagrams.py
"""
from pathlib import Path
from graphviz import Digraph

OUT = Path(__file__).resolve().parents[1] / "images"
OUT.mkdir(exist_ok=True)

FONT = "Helvetica"
C = dict(
    guard="#FDE8E8",
    guard_b="#C0392B",
    agent="#E8F0FE",
    agent_b="#2F5FBF",
    data="#FFF8E1",
    data_b="#B8860B",
    ok="#E6F4EA",
    ok_b="#1E7B3A",
    ink="#1F2937",
)


def base(name: str, rankdir: str = "LR", **kw) -> Digraph:
    g = Digraph(name, format="png")
    g.attr(
        rankdir=rankdir,
        bgcolor="white",
        fontname=FONT,
        pad="0.4",
        dpi="170",
        nodesep="0.45",
        ranksep="0.6",
        **kw,
    )
    g.attr(
        "node",
        fontname=FONT,
        fontsize="12",
        style="filled,rounded",
        shape="box",
        color=C["ink"],
        fontcolor=C["ink"],
        penwidth="1.4",
        margin="0.2,0.12",
    )
    g.attr(
        "edge",
        fontname=FONT,
        fontsize="10",
        color="#4B5563",
        fontcolor="#4B5563",
        penwidth="1.3",
    )
    return g


def guard(g: Digraph, n: str, label: str) -> None:
    g.node(n, label, fillcolor=C["guard"], color=C["guard_b"])


def agent(g: Digraph, n: str, label: str) -> None:
    g.node(n, label, fillcolor=C["agent"], color=C["agent_b"])


def data(g: Digraph, n: str, label: str) -> None:
    g.node(n, label, fillcolor=C["data"], color=C["data_b"])


def good(g: Digraph, n: str, label: str) -> None:
    g.node(n, label, fillcolor=C["ok"], color=C["ok_b"])


# 1 ─ architecture ───────────────────────────────────────────────────────────
def architecture() -> None:
    g = base(
        "architecture",
        "TB",
        label="NexusFlow Multi-Agent Pipeline — Guarded Sequential Handoff Architecture",
        labelloc="t",
        fontsize="18",
        compound="true",
    )
    data(g, "user", "User Mission Objective\n(custom prompt or domain preset)")
    guard(g, "ig", "InputGuard & Mode Router\nvalidate objective · isolate API key · select engine")

    with g.subgraph(name="cluster_agents") as c:
        c.attr(
            label="Autonomous 4-Agent Swarm — context accumulated & audited at every handoff",
            style="rounded,dashed",
            color=C["agent_b"],
            fontname=FONT,
            fontsize="11",
            fontcolor=C["agent_b"],
        )
        c.attr(
            "node",
            style="filled,rounded",
            fontname=FONT,
            fontsize="12",
            color=C["agent_b"],
            fillcolor=C["agent"],
        )
        c.node("pl", "01 · Planner Agent\n(Task Decomposer · plan_schema)")
        c.node("re", "02 · Researcher Agent\n(Domain Synthesizer · kb_retrieval)")
        c.node("bu", "03 · Builder Agent\n(Code Synthesizer · code_synth)")
        c.node("rv", "04 · Reviewer Agent\n(QA Critic & Scorer · qa_audit)")
        c.edge("pl", "re", label=" milestones")
        c.edge("re", "bu", label=" architecture + bounds")
        c.edge("bu", "rv", label=" code artifact")

    data(
        g,
        "engine",
        "Execution Backend\nGemini 3.8 Flash (google-genai)  |  Zero-Config Simulator",
    )
    guard(
        g,
        "og",
        "OutputGuard & DOM Sanitizer\ntextContent XSS guard · no eval/exec · secret check",
    )
    good(
        g,
        "rep",
        "Verified Deliverable + QA Score\n(Interactive Inspector + .MD Report Export)",
    )
    guard(g, "sr", "Safe Fallback / Validation Toast\n(empty input blocked · clean fallback)")

    g.edge("user", "ig")
    g.edge("ig", "pl", lhead="cluster_agents")
    g.edge("engine", "pl", lhead="cluster_agents", style="dashed", label=" model / sim steps ")
    g.edge("rv", "og", ltail="cluster_agents", label="  audited outputs + score")
    g.edge("og", "rep")
    g.edge(
        "ig",
        "sr",
        style="dashed",
        color=C["guard_b"],
        fontcolor=C["guard_b"],
        label=" empty / invalid",
        constraint="false",
    )
    g.edge(
        "og",
        "sr",
        style="dashed",
        color=C["guard_b"],
        fontcolor=C["guard_b"],
        label=" API error -> auto fallback",
        constraint="false",
    )
    g.render(str(OUT / "architecture"), cleanup=True)


# 2 ─ defense & orchestration layers ─────────────────────────────────────────
def layers() -> None:
    g = base(
        "layers",
        "TB",
        label="NexusFlow Defence-in-Depth & Orchestration: Six Independent Layers",
        labelloc="t",
        fontsize="18",
    )
    g.attr("node", shape="box", width="7.4", fontsize="13")
    rows = [
        (
            "L1",
            "Objective & Input Validation",
            "non-empty objective guard · prompt boundary wrapping · Pydantic request schema",
            C["guard"],
            C["guard_b"],
        ),
        (
            "L2",
            "Credential & Secret Isolation",
            ".env excluded via .gitignore · platform secret store (Vercel / Render) · local-only key storage",
            C["guard"],
            C["guard_b"],
        ),
        (
            "L3",
            "Role-Scoped Agent Instructions",
            "per-agent system_instruction isolation (Planner, Researcher, Builder, Reviewer)",
            C["agent"],
            C["agent_b"],
        ),
        (
            "L4",
            "Sequential Context Bus & Telemetry",
            "structured inter-agent handoffs · per-step token tracking · live event trace bus",
            C["agent"],
            C["agent_b"],
        ),
        (
            "L5",
            "Resilient Dual-Mode Execution",
            "official Gemini Interactions API (gemini-3.8-flash) · automatic zero-key simulated fallback",
            C["data"],
            C["data_b"],
        ),
        (
            "L6",
            "DOM XSS Guard & Static Code Delivery",
            "strict textContent rendering (never raw innerHTML) · zero server eval/exec · safe .MD export",
            C["ok"],
            C["ok_b"],
        ),
    ]
    prev = None
    for k, title, desc, fill, line in rows:
        g.node(k, f"{k}  {title}\n{desc}", fillcolor=fill, color=line)
        if prev:
            g.edge(prev, k, arrowhead="vee")
        prev = k
    g.render(str(OUT / "defense_layers"), cleanup=True)


# 3 ─ request flow ───────────────────────────────────────────────────────────
def flow() -> None:
    g = base(
        "flow",
        "TB",
        label="Request Flow: Live Gemini API vs. Zero-Config Simulated Fallback",
        labelloc="t",
        fontsize="18",
    )
    data(g, "req", "Incoming Task Request\n(Studio UI / POST /api/orchestrate / CLI)")
    g.node(
        "d1",
        "Objective passes\ninput validation?",
        shape="diamond",
        fillcolor=C["guard"],
        color=C["guard_b"],
        margin="0.05,0.05",
    )
    g.node(
        "d2",
        "Live Gemini Mode enabled\n& API key available?",
        shape="diamond",
        fillcolor=C["data"],
        color=C["data_b"],
        margin="0.05,0.05",
    )
    agent(
        g,
        "live",
        "Live Gemini 3.8 Flash Chain\n(/api/orchestrate or client.interactions.create)",
    )
    agent(
        g,
        "sim",
        "Simulated Multi-Agent Engine\n(deterministic 4-agent synthesis · zero key needed)",
    )
    agent(
        g,
        "pipe",
        "Sequential 4-Agent Execution\nPlanner -> Researcher -> Builder -> Reviewer",
    )
    guard(
        g,
        "og",
        "Output Sanitizer & QA Scorer\n(textContent DOM render · compute score / 100)",
    )
    good(
        g,
        "ok",
        "Combined Deliverable + QA Audit\n(View per-agent tabs · Copy · Export .MD)",
    )
    guard(
        g,
        "no",
        "Safe Refusal Toast / HTTP 422\n(no pipeline execution)",
    )
    data(g, "log", "Telemetry Bus: timestamp · agent · tool · token count · elapsed time")

    g.edge("req", "d1")
    g.edge("d1", "d2", label=" yes", color=C["ok_b"], fontcolor=C["ok_b"])
    g.edge("d1", "no", label=" no", color=C["guard_b"], fontcolor=C["guard_b"])
    g.edge("d2", "live", label=" yes", color=C["ok_b"], fontcolor=C["ok_b"])
    g.edge("d2", "sim", label=" no (zero-config)", color=C["data_b"], fontcolor=C["data_b"])
    g.edge("live", "pipe")
    g.edge(
        "live",
        "sim",
        style="dashed",
        color=C["guard_b"],
        fontcolor=C["guard_b"],
        label=" network / key error fallback",
    )
    g.edge("sim", "pipe")
    g.edge("pipe", "og")
    g.edge("og", "ok")
    for n in ("d1", "pipe", "og"):
        g.edge(n, "log", style="dotted", arrowhead="none", constraint="false")
    g.render(str(OUT / "request_flow"), cleanup=True)


if __name__ == "__main__":
    architecture()
    layers()
    flow()
    print("Diagrams written to", OUT)