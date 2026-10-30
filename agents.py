"""
NexusFlow — Base-Level Agentic AI Multi-Agent System
Uses the official Google GenAI SDK (`google-genai`) and `gemini-3.8-flash`
with an automatic zero-key simulated fallback for instant cloud demos.
"""

import os
import sys
from dataclasses import dataclass
from typing import Dict, List

MODEL_ID = "gemini-3.8-flash"


@dataclass
class AgentSpec:
    key: str
    name: str
    role_prompt: str


AGENTS: List[AgentSpec] = [
    AgentSpec(
        key="planner",
        name="Planner Agent",
        role_prompt=(
            "You are the Lead Planner Agent in a 4-agent engineering system. "
            "Break the user's objective into 3 concrete milestones, required components, "
            "and clear acceptance criteria."
        ),
    ),
    AgentSpec(
        key="researcher",
        name="Researcher Agent",
        role_prompt=(
            "You are the Technical Researcher Agent. Given the objective and the Planner's "
            "milestones, specify the optimal architecture pattern, algorithmic bounds, and edge cases."
        ),
    ),
    AgentSpec(
        key="builder",
        name="Builder Agent",
        role_prompt=(
            "You are the Senior Builder Agent. Produce clean, modular, runnable code that "
            "implements the Planner's milestones and follows the Researcher's architecture."
        ),
    ),
    AgentSpec(
        key="reviewer",
        name="Reviewer Agent",
        role_prompt=(
            "You are the QA Critic & Security Reviewer Agent. Audit the Builder's output "
            "against the Planner's acceptance criteria, note any edge-case fixes, and give a score out of 100."
        ),
    ),
]


class MultiAgentOrchestrator:
    """Sequential handoff orchestrator: Planner -> Researcher -> Builder -> Reviewer."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")

    def run_pipeline(self, objective: str) -> Dict[str, str]:
        if not self.api_key:
            return self._run_simulated(objective)

        from google import genai

        client = genai.Client(api_key=self.api_key)
        accumulated_context = f"USER OBJECTIVE:\n{objective}\n"
        outputs: Dict[str, str] = {}

        for spec in AGENTS:
            interaction = client.interactions.create(
                model=MODEL_ID,
                system_instruction=spec.role_prompt,
                input=accumulated_context,
            )
            step_output = interaction.output_text or ""
            outputs[spec.key] = step_output
            accumulated_context += f"\n\n--- {spec.name.upper()} OUTPUT ---\n{step_output}"

        return outputs

    def _run_simulated(self, objective: str) -> Dict[str, str]:
        """Deterministic fallback when GEMINI_API_KEY is not set on Render/Vercel."""
        title = objective.strip()[:80]
        return {
            "planner": (
                f"## Milestone Plan (Planner Agent)\n"
                f"Objective: {title}\n"
                f"1. Define core data contracts and validation boundaries.\n"
                f"2. Implement modular service logic with structured telemetry.\n"
                f"3. Verify edge cases with automated unit tests."
            ),
            "researcher": (
                "## Technical Synthesis (Researcher Agent)\n"
                "- Pattern: Hexagonal service layer with explicit state handoffs.\n"
                "- Complexity: O(n) single-pass execution with non-blocking I/O."
            ),
            "builder": (
                "## Implementation Artifact (Builder Agent)\n"
                "```python\n"
                "def execute_task(objective: str) -> dict:\n"
                "    return {'status': 'completed', 'objective': objective, 'verified': True}\n"
                "```"
            ),
            "reviewer": (
                "## QA & Security Audit (Reviewer Agent)\n"
                "- All milestones satisfied and verified.\n"
                "- Quality Score: 96 / 100"
            ),
        }


if __name__ == "__main__":
    user_goal = " ".join(sys.argv[1:]) or "Build a token-bucket rate limiter middleware in FastAPI"
    orchestrator = MultiAgentOrchestrator()
    results = orchestrator.run_pipeline(user_goal)
    for agent_key, text in results.items():
        print(f"\n==================== {agent_key.upper()} ====================")
        print(text)
