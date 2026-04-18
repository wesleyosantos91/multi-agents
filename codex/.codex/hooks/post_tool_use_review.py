#!/usr/bin/env python3
"""Emite alertas contextuais após comandos sensíveis."""

import json
import sys


def main() -> int:
    try:
        evento = json.load(sys.stdin)
    except Exception:
        return 0

    comando = (
        evento.get("tool_input", {}).get("command")
        or evento.get("toolInput", {}).get("command")
        or ""
    ).lower()

    if "git commit" in comando and "--amend" in comando:
        sys.stdout.write(
            json.dumps(
                {
                    "systemMessage": "Evite commit --amend sem solicitação explícita do usuário."
                }
            )
        )

    if "terraform apply" in comando:
        sys.stdout.write(
            json.dumps(
                {
                    "systemMessage": "Confirme evidências de validação e plano de rollback antes de terraform apply."
                }
            )
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
