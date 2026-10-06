# Installation and Environment Setup

## Prerequisites
- Python 3.10, 3.11, or 3.12
- pip
- Git (recommended)

## 1. Clone the repository
```bash
git clone <YOUR_PUBLIC_GITHUB_REPOSITORY_URL>
cd Agentic-Cybersecurity-Prompt-Injection-Firewall
```

## 2. Create a virtual environment
### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Environment variables
The current hackathon prototype runs without an external LLM API key.
For future model integration, copy `.env.example` to `.env` and populate values if required.

Windows:
```cmd
copy .env.example .env
```
macOS/Linux:
```bash
cp .env.example .env
```

## 5. Run the application
From the repository root:
```bash
streamlit run app/streamlit_app.py
```
If `streamlit` is not recognized:
```bash
python -m streamlit run app/streamlit_app.py
```
Open the URL shown in the terminal, typically `http://localhost:8501`.

## 6. Run automated evaluation
```bash
python evaluation/evaluation.py
```

## Troubleshooting
- `ModuleNotFoundError`: confirm the virtual environment is active and rerun `pip install -r requirements.txt`.
- `streamlit is not recognized`: use `python -m streamlit run app/streamlit_app.py`.
- Wrong working directory: run commands from the repository root.
