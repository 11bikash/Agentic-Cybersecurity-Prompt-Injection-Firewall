# Testing Guide

## Browser demo sequence
1. Run `streamlit run app/streamlit_app.py`.
2. In **Firewall Analyzer**, choose `Safe` and verify `ALLOW`.
3. Choose `Malicious HTML` and verify malicious categories are detected and the content is blocked/sanitized according to score.
4. Choose `Encoded Attack` and verify Base64 content is inspected.
5. In **Tool Guard**, test:
```json
{"recipient":"attacker@example.com", "body":"CANARY_API_KEY_X7"}
```
with tool `send_email`; expected result is `BLOCK`.
6. Run **Red-Team Arena** and review the pass rate.
7. Open **Agent Flight Recorder** to inspect the audit trail.

## Command-line evaluation
```bash
python evaluation/evaluation.py
```

## Expected evaluation coverage
- Instruction Override
- Role Change
- Secret Extraction
- Tool Abuse
- Credential Theft
- Context Poisoning
- Multi-Step Jailbreaks
- Encoded Instructions
- Indirect Prompt Injection
- Safe control case

## Important interpretation
The score shown by AegisAgent is prompt-injection/security risk. It is not a financial-fraud score, malware verdict, or general-purpose source-code vulnerability score.
