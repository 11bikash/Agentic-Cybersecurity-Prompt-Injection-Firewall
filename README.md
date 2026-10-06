# AegisAgent - Adaptive Agentic Prompt Injection Firewall

**ET AI Hackathon: Agentic Edition | Round 2 Working Prototype**

> **Securing the boundary between what an AI agent reads and what it is allowed to do.**

AegisAgent is a zero-trust security prototype for AI agents. It intercepts incoming content before it reaches a downstream agent, detects prompt-injection patterns, assigns an explainable risk score, sanitizes or blocks malicious instructions, validates high-impact tool calls, runs repeatable red-team tests, and records decisions in an Agent Flight Recorder.

## Problem statement
**Agentic Cybersecurity - Prompt Injection Firewall**

The challenge is to detect and neutralize malicious instructions embedded in user input or retrieved content before they influence AI behavior, while allowing legitimate content to pass with minimal disruption.

## What the prototype demonstrates
- Detection coverage for 9 prompt-injection attack categories
- `ALLOW` / `SANITIZE` / `BLOCK` enforcement decisions
- Base64/encoded-instruction inspection
- Canary-secret leakage detection
- Tool Guard for unsafe AI-agent actions
- Red-Team Evaluation Arena
- Agent Flight Recorder for auditability and explainability
- Streamlit user interface for live demonstration

## Attack categories covered
1. Instruction Override
2. Role Change
3. Secret Extraction
4. Tool Abuse
5. Credential Theft
6. Context Poisoning
7. Multi-Step Jailbreaks
8. Encoded Instructions
9. Indirect Prompt Injection

## Claimed hackathon position
- **Feature level: F3** - prototype covers at least 7 attack types; bundled tests cover all 9 listed categories.
- **Depth level: D2** - textual/structured inputs with repeatable evaluation and explainable behavior.
- **D3 is intentionally not claimed** because full multimodal file/OCR ingestion is not implemented in this repository.

## Technology stack
- Python 3.10+
- Streamlit
- Pandas
- Plotly
- BeautifulSoup4
- python-dotenv

The current prototype does **not** require a paid LLM API key to run. Detection and scoring are implemented locally for reproducible judging.

## Quick start
### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

### Windows Command Prompt
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Open the local URL displayed by Streamlit, usually `http://localhost:8501`.

For detailed setup and troubleshooting, see [`docs/INSTALLATION.md`](docs/INSTALLATION.md).

## Live demo flow
1. **Firewall Analyzer - Safe:** verify legitimate content is allowed.
2. **Firewall Analyzer - Malicious HTML:** detect an indirect prompt injection.
3. **Firewall Analyzer - Encoded Attack:** inspect a Base64-encoded malicious instruction.
4. **Tool Guard:** attempt `send_email` with `CANARY_API_KEY_X7` and verify the action is blocked.
5. **Red-Team Arena:** run the full defensive evaluation suite.
6. **Agent Flight Recorder:** review the observable audit trail.

Sample inputs are available in [`data/demo/`](data/demo/).

## Run automated evaluation
```bash
python evaluation/evaluation.py
```
The evaluation suite contains nine malicious categories plus one safe control case.

## Repository structure
```text
.
├── app/
│   └── streamlit_app.py          # Streamlit application
├── agents/
│   ├── detector.py               # Prompt-injection detector and risk engine
│   ├── flight_recorder.py        # Audit / observability trail
│   └── red_team.py               # Defensive red-team test suite
├── guardrails/
│   └── policies.py               # Tool Guard and sensitive-data policies
├── evaluation/
│   └── evaluation.py             # CLI evaluation runner
├── data/demo/
│   ├── malicious_webpage.html
│   ├── encoded_attack.txt
│   └── safe_email.txt
├── docs/
│   ├── architecture.md           # Structural architecture
│   ├── INSTALLATION.md           # Setup and troubleshooting
│   ├── API.md                    # Internal module/API documentation
│   ├── TESTING.md                # Testing guide
│   └── demo_script.md            # Demo narrative
├── .env.example                  # Optional future LLM config
├── .gitignore
├── requirements.txt
└── README.md
```

## Architecture summary
```text
Incoming Content
      |
      v
Input Normalizer
      |
      v
Threat Detection Ensemble
      |
      v
Risk Engine
      |
ALLOW / SANITIZE / BLOCK
      |
      v
Safe Agent Context
      |
      v
Tool Guard
      |
ALLOW / REVIEW / BLOCK
      |
      v
Flight Recorder + Human Oversight
```

See [`docs/architecture.md`](docs/architecture.md) for the detailed architecture and component responsibilities.

## Internal API / module documentation
The prototype is Streamlit-based and does not expose a public REST API. The reusable Python functions are documented in [`docs/API.md`](docs/API.md), including:
- `detect_prompt_injection(...)`
- `evaluate_tool_call(...)`
- `run_red_team()`
- `FlightRecorder`

## Environment setup
`.env.example` is provided for optional future LLM integration. No API key is required for the submitted prototype.

```text
OPENAI_API_KEY=
MODEL_NAME=gpt-4o-mini
```

Never commit real credentials or a populated `.env` file.

## Responsible AI and security controls
- Human oversight for consequential/high-risk actions
- Synthetic canary secrets instead of real credentials
- Explainable evidence for detections
- Risk-based enforcement
- Defensive-only adversarial examples
- Observable audit trail
- No external action is actually executed by this prototype

## Known limitations
- Rule-based prototype; a production deployment should add semantic/model-based detection and broader adversarial evaluation.
- The UI accepts text representing PDF/OCR/source-code input; it does not yet parse uploaded PDF/image files directly.
- Flight-recorder events are stored in the Streamlit session and are not persisted.
- Enterprise authentication, SIEM integration, durable policy stores, and secure production logging are outside this hackathon build.

## Documentation index
- [Installation and environment setup](docs/INSTALLATION.md)
- [Architecture overview](docs/architecture.md)
- [API/module documentation](docs/API.md)
- [Testing guide](docs/TESTING.md)
- [Demo script](docs/demo_script.md)

## Judges: 60-second run path
```bash
python -m venv .venv
# activate the environment
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```
Then run the Safe, Malicious HTML, Tool Guard, and Red-Team Arena examples from the UI.

## Disclaimer
This repository is a defensive hackathon prototype for demonstrating prompt-injection detection and AI-agent security controls. The bundled examples use synthetic data and synthetic secrets only.
