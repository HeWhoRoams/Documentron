# AppDoc End-to-End Prompt

Use this in GitHub Copilot Chat to run the full Documentron workflow.

Prompt: 

"/appdoc Run inspect → convert → synthesize → verify → report for the current workspace. Use the VS Code task 'AppDoc: Run All' and stream output. Place artifacts in `Documentron/artifacts` and docs in `Documentron/docs`. Summarize results from `Documentron/artifacts/report/summary.md`."