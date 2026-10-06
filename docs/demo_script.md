# 3-Minute Demo Script

0:00 - 0:20: Introduce the problem: AI agents read external content and use tools, so prompt injection can hijack behavior.

0:20 - 0:45: Show AegisAgent dashboard and explain zero-trust content handling.

0:45 - 1:15: Analyze a safe message. Decision: ALLOW.

1:15 - 1:55: Analyze malicious HTML with hidden indirect prompt injection. Decision: BLOCK/SANITIZE with evidence.

1:55 - 2:25: Validate a risky send_email tool call containing a canary secret. Tool Guard blocks exfiltration.

2:25 - 2:50: Run Red-Team Arena and show detection pass rate.

2:50 - 3:10: Show Agent Flight Recorder for auditability.

3:10 - 3:30: Close with the value: not a chatbot, but a defensive runtime layer for safe agentic AI.
