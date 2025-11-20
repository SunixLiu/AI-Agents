# CV Reviewer
[[Chinese 中文]](Readme_zh.md) 

![Screenshot](./asset/screenshot.png)
## Overview
- Resume review web app built with Streamlit and Agno.
- Bilingual UI and output (Chinese/English), default is Chinese.
- Sidebar model configuration (OpenAI-compatible `Base URL`, `API Key`, `Model ID`).
- Upload JD and CV (PDF/MD/TXT), click Analyze to get a Markdown report with a score and recommendations.

## Requirements
- Python 3.10+
- A running OpenAI-compatible inference service (local or remote)

## Install Dependencies
```bash
pip install -r requirement.txt
```

## Run
```bash
streamlit run app.py
```

## How to Use
- Select language at the top center (default: Chinese).
- In the sidebar, fill `API Base URL`, `API Key`, and `Model ID`, then click Confirm.
- Upload JD and CV in the sidebar (supports `pdf`, `md`, `txt`).
- Click Analyze in the main area to see the Markdown report and score.

## Features
- Language toggle: both UI and output switch between Chinese and English.
- Model configuration: all three fields are required; confirming rebuilds the Agent and shows a success message.
- File support: `pdf` is converted to Markdown; `md`/`txt` read as plain text.
- Output: includes match assessment, strengths, risks, and improvement suggestions, plus a 0–100 score (guided by system prompt).

## Structure
- `app.py`: Main app entry and UI logic
- `requirement.txt`: Dependency list
- `sys_prompt.md`: System instructions

## Troubleshooting
- Cannot connect to model service: verify `API Base URL` and that the service is running.
- Unsupported file type: convert JD/CV to `pdf`, `md`, or `txt`.
- Output language mismatch: check the language toggle and ensure you clicked Confirm in the sidebar.
