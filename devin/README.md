# Multi-Agent Governance for Devin AI

This directory contains the configuration and knowledge base required to turn **Devin AI** into a highly precise, multi-agent engineering team.

## Overview

By using the `.devinrules` file in the root of your project, Devin is instructed to act as a **Staff Engineer Orchestrator**. Instead of jumping straight into code, it follows a structured workflow:
1.  **Analyze** the task.
2.  **Consult** specialized expert personas (found in `docs/ai/roles/`).
3.  **Synthesize** a plan that balances security, architecture, and performance.
4.  **Execute** the implementation.

## How to use in a new project

To bring this intelligence to a new repository:

1.  Copy the `.devinrules` file to your project root.
2.  Copy the `docs/ai/` folder to your project root.
3.  When starting a session with Devin, it will automatically detect these rules and begin consulting the playbooks during its research phase.

## Expert Roles Included

- **Architect**: Structural decisions and resilience.
- **Security**: Hardening and threat modeling.
- **Tech Lead**: Simplicity and technical debt management.
- **DBA**: Database modeling and query optimization.
- **Specialists**: Deep-dives into Java, Python, Go, Frontend, and Mobile.
- **SRE & CI/CD**: Operations, observability, and delivery pipelines.

## Precision Gains

This setup prevents "context window fading" by forcing the AI to focus its attention on specific technical disciplines one at a time, just as a real human engineering team would do.
