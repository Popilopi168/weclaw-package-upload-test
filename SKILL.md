---
name: weclaw_installer
description: Automate installing and configuring the WeClaw WeChat bot environment on macOS. Use when the user asks to download/install WeClaw, set up the local Python environment, or troubleshoot setup prerequisites (git/uv, macOS Accessibility permissions, API key).
metadata:
  openclaw:
    os: ["darwin"]
    requires:
      bins: ["git", "uv", "python3"]
---

## When to use

Use this skill when the user wants to:
- Install / download / bootstrap the WeClaw project locally
- Set up Python dependencies with `uv`
- Configure an API key / `.env`
- Fix common macOS setup blockers (especially Accessibility permission)

## Workflow

1. Ensure prerequisites are available: `git`, `uv`, `python3`.
2. On macOS, ensure Accessibility permission is enabled for the terminal/app that will run automation.
3. Ask the user for the required API key if it is not already provided.
4. Run the project’s setup entrypoint to perform the automated steps.

## Entrypoint

Run:

- `python3 setup_package.py`

(If the setup script requires arguments/flags, follow the script’s prompts or update the invocation accordingly.)

## Safety / guardrails

- Do not request or store unrelated secrets.
- Only write `.env` / config values that are explicitly required for WeClaw setup.
- If a step fails, surface the exact command output and suggest the smallest next fix.