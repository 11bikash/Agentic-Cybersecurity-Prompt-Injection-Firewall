# AegisAgent Architecture Overview

## High-level flow
```text
Incoming content / tool request
        |
        v
Input Normalizer
        |
        v
Threat Detection Ensemble
(patterns + decoded content + canary checks)
        |
        v
Risk Engine
        |
   +----+-----+
   |          |
 ALLOW     SANITIZE / BLOCK
   |          |
   +----+-----+
        |
        v
Safe downstream AI-agent context
        |
        v
Tool Guard
        |
 ALLOW / REVIEW / BLOCK
        |
        v
Agent Flight Recorder / Human Oversight
```

## Components

### 1. Input Normalizer
Normalizes incoming textual content from user messages, web pages, PDF-extracted text, email, Markdown, HTML, API responses, source code, and OCR text.

### 2. Threat Detection Ensemble
`agents/detector.py` checks the content for nine prompt-injection categories. It also attempts Base64 decoding and scans decoded content, and detects canary-secret references.

### 3. Risk Engine
A deterministic scoring layer maps detected attack categories and high-risk behaviors to a 0-100 risk score and an enforcement decision.

### 4. Sanitization / Blocking
The prototype can allow normal content, sanitize suspicious instructions, or quarantine/block high-risk content before downstream agent execution.

### 5. Tool Guard
`guardrails/policies.py` validates high-impact tool calls and checks for sensitive markers or likely exfiltration destinations before an action can execute.

### 6. Red-Team Arena
`agents/red_team.py` provides repeatable defensive tests across the nine attack categories plus a safe control case.

### 7. Agent Flight Recorder
`agents/flight_recorder.py` records major security decisions for explainability, observability, and audit review.

## Feature / depth claim
- **F3:** covers all 9 listed prompt-injection attack categories in the prototype test set (requirement is at least 7).
- **D2:** handles structured/textual inputs with repeatable evaluation and explainable decisions.
- **D3 is not claimed:** OCR/image ingestion is represented as a source type, but multimodal file extraction is not implemented in this prototype.

## Responsible AI / security controls
- Human oversight for high-risk actions
- No production credentials required
- Canary secrets are synthetic test markers
- Explainable evidence and risk scoring
- Defensive red-team test cases only
- Clear separation between detection and tool-action policy enforcement

## Production extension path
- Enterprise identity and policy integration
- Secure persistent audit logging
- Model-based semantic detector in addition to deterministic rules
- File parsers and hardened OCR
- Policy-as-code / approval workflows
- Continuous adversarial evaluation and telemetry
