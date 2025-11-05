# AppDoc End-to-End Prompt

Use this in GitHub Copilot Chat to run the full Documentron workflow.

Prompt:

"/appdoc
Goal: Run inspect → convert → synthesize → verify → report for the current workspace, with zero manual steps.

Instructions for Copilot:
- If a terminal is not open, open one.
- Run: python Documentron/ux/cli/appdoc.py --repo .
- Stream the terminal output back here.
- If Python is not found, try: py -3 Documentron/ux/cli/appdoc.py --repo .
- On failure of any step, show the error and re-run only the failed step using --steps <step>.
- After completion, show a concise summary by printing 'Generated Documentation/report/summary.md' and, if present, 'Generated Documentation/report/quality.report.json'.
- Do not ask for additional input unless strictly required."
