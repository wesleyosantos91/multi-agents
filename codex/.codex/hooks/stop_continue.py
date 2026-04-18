#!/usr/bin/env python3
"""Injeta lembretes de governança no ciclo de sessão/prompt."""

import argparse
import json
import sys

MENSAGEM_SESSAO = (
    "Modo enterprise ativo: priorize menor mudança defensável, evidências concretas e validação proporcional."
)

MENSAGEM_PROMPT = (
    "Antes de editar, confirme escopo, arquivos impactados e plano de validação. Evite varreduras amplas sem necessidade."
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session-start", action="store_true")
    parser.add_argument("--user-prompt", action="store_true")
    args = parser.parse_args()

    if args.session_start:
        payload = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": MENSAGEM_SESSAO,
            }
        }
        sys.stdout.write(json.dumps(payload))
        return 0

    if args.user_prompt:
        payload = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": MENSAGEM_PROMPT,
            }
        }
        sys.stdout.write(json.dumps(payload))
        return 0

    sys.stdout.write(json.dumps({"continue": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
