import { GoogleGenAI } from "@google/genai";

const MODEL_ID = "gemini-3.8-flash";

const AGENTS = [
  {
    key: "planner",
    name: "Planner Agent",
    prompt: "You are the Lead Planner Agent. Break the user objective into 3 concrete milestones and clear acceptance criteria."
  },
  {
    key: "researcher",
    name: "Researcher Agent",
    prompt: "You are the Technical Researcher Agent. Specify the optimal architecture pattern, trade-offs, and edge cases."
  },
  {
    key: "builder",
    name: "Builder Agent",
    prompt: "You are the Senior Builder Agent. Produce clean, modular, runnable code implementing the plan."
  },
  {
    key: "reviewer",
    name: "Reviewer Agent",
    prompt: "You are the QA Critic & Security Reviewer Agent. Audit the implementation against the plan and assign a score out of 100."
  }
];

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { objective = "Build a multi-agent workflow", apiKey } = req.body || {};
  const resolvedKey = apiKey || process.env.GEMINI_API_KEY;

  if (!resolvedKey) {
    return res.status(200).json({
      status: "simulated_fallback",
      outputs: null
    });
  }

  try {
    const client = new GoogleGenAI({ apiKey: resolvedKey });
    let context = `USER OBJECTIVE:\n${objective}\n`;
    const outputs = {};

    for (const agent of AGENTS) {
      const interaction = await client.interactions.create({
        model: MODEL_ID,
        system_instruction: agent.prompt,
        input: context
      });
      const text = interaction.output_text || "";
      outputs[agent.key] = text;
      context += `\n\n--- ${agent.name.toUpperCase()} ---\n${text}`;
    }

    return res.status(200).json({ status: "completed", outputs });
  } catch (error) {
    return res.status(500).json({ error: error.message || "Orchestration error" });
  }
}
