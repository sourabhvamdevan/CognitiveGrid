# Security Policy

## Supported Versions

Security updates and patches are actively maintained for the latest release of **NexusFlow — Agentic AI Multi-Agent Orchestration Studio** (`main` branch).

| Version | Supported | Runtime Scope |
| :--- | :--- | :--- |
| `1.0.x` (`main`) | Yes | Web Studio UI (`index.html`), FastAPI Backend (`server.py`, `agents.py`), Vercel Serverless API (`api/orchestrate.js`) |
| `< 1.0.0` | No | Legacy prototypes |

## Reporting a Vulnerability

Please **do not** report security vulnerabilities through public GitHub issues, discussions, or pull requests.

Instead, report suspected vulnerabilities using one of the following private channels:

1. **GitHub Private Vulnerability Reporting (Preferred)**: Navigate to the **Security** tab of this repository, click **Advisories**, and select **Report a vulnerability** to open a private security advisory draft.
2. **Direct Maintainer Contact**: Reach out directly to the repository maintainer (@Sourabh) via GitHub profile contact channels with the subject line `[SECURITY] NexusFlow Vulnerability Report`.

### What to Include in Your Report

To help triage and resolve the issue quickly, please include:

- **Affected Component**: Specify whether the issue affects the browser UI (`index.html`), the Python FastAPI orchestration service (`server.py` / `agents.py`), or the Vercel Node serverless handler (`api/orchestrate.js`).
- **Vulnerability Class**: Describe the nature of the issue (for example, API key exposure, Cross-Site Scripting in agent output rendering, Server-Side Request Forgery, or multi-agent prompt injection escalation).
- **Reproduction Steps**: Provide a minimal, reproducible payload, HTTP request, or prompt sequence that demonstrates the issue.
- **Impact Assessment**: Explain what an attacker could achieve under realistic deployment conditions on Vercel or Render.

### Response & Disclosure Timeline

| Stage | Target SLA | Description |
| :--- | :--- | :--- |
| **Acknowledgment** | Within 48 hours | Confirmation that the report was received and assigned for review |
| **Triage & Validation** | Within 5 business days | Reproduction check, severity assessment, and remediation plan |
| **Patch & Release** | Within 14 days | Fix merged to `main` and advisory published with credit to reporter |

## Multi-Agent & API Key Security Best Practices

When deploying or extending this project on **Vercel**, **Render**, or custom cloud infrastructure, follow these security controls:

### 1. Protecting `GEMINI_API_KEY` Credentials

- **Never commit `.env` files**: Keep `.env` listed in `.gitignore` and only commit `.env.example` with dummy values.
- **Use platform secret stores**: Configure `GEMINI_API_KEY` inside **Vercel Environment Variables** (encrypted at rest) or **Render Environment Variables** rather than hardcoding keys in `agents.py`, `server.py`, or `index.html`.
- **Browser-entered keys**: When entering an optional API key in the Studio UI settings modal for client-side testing, the key is stored only in your local browser's `localStorage` (`nexusflow_gemini_key`) and should only be used on trusted personal devices.
- **Rotate compromised keys immediately**: If an API key is ever accidentally pushed to git history, revoke and regenerate it immediately in Google AI Studio.

### 2. Multi-Agent Prompt Injection & Output Handling

- **Untrusted input boundaries**: User objectives passed to the **Planner Agent** are concatenated into downstream context for the **Researcher**, **Builder**, and **Reviewer** agents. Treat all user-supplied prompts and external text as untrusted input.
- **DOM rendering safety**: The Studio UI renders agent outputs inside `#inspectorContent` using `textContent` rather than raw `innerHTML` to prevent Cross-Site Scripting (XSS) when displaying generated code or markdown. Maintain `textContent` or a strict HTML sanitizer if customizing the output viewer.
- **No arbitrary code execution on the server**: The **Builder Agent** synthesizes source code as text artifacts only; neither `server.py` nor `api/orchestrate.js` executes model-generated code via `eval()`, `exec()`, or `subprocess`. Never wire model outputs directly into shell or interpreter execution without an isolated sandbox.

### 3. Production API Hardening (Vercel & Render)

- **Rate limiting**: Add request rate limiting (such as a token-bucket middleware or Vercel Firewall rules) on `POST /api/orchestrate` before exposing a server-funded `GEMINI_API_KEY` to public internet traffic.
- **CORS policy**: Restrict Cross-Origin Resource Sharing (`CORS`) to your production Vercel or Render domain when deploying `server.py` as a standalone API.
- **Dependency hygiene**: Enable GitHub **Dependabot** alerts to monitor `requirements.txt` (`fastapi`, `uvicorn`, `pydantic`, `google-genai`) and `package.json` (`@google/genai`) for upstream security advisories.
