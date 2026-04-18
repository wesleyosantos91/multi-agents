#!/usr/bin/env python3
"""Bloqueia comandos de shell obviamente destrutivos (best effort)."""

import json
import re
import sys

PADROES_BLOQUEIO = [
    r"\brm\s+-rf\s+/",
    r"\brm\s+-rf\s+\*",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+clean\s+-fdx\b",
    r"\bshutdown\b",
    r"\breboot\b",
    r"\bformat\b",
]

ARQUIVOS_SENSIVEIS = [
    "AGENTS.md",
    ".codex/config.toml",
    ".codex/hooks.json",
]


def bloquear(motivo: str) -> int:
    sys.stdout.write(json.dumps({"decision": "block", "reason": motivo}))
    return 0


def main() -> int:
    try:
        evento = json.load(sys.stdin)
    except Exception:
        return 0

    comando = (
        evento.get("tool_input", {}).get("command")
        or evento.get("toolInput", {}).get("command")
        or ""
    )
    lower = comando.lower()

    for padrao in PADROES_BLOQUEIO:
        if re.search(padrao, lower):
            return bloquear("Bloqueado por política: comando potencialmente destrutivo.")

    for arq in ARQUIVOS_SENSIVEIS:
        if arq.lower() in lower and re.search(r"\b(sed|perl|python|echo|cat|tee|truncate)\b", lower):
            return bloquear(
                "Bloqueado por política: edição direta de arquivo sensível via shell. "
                "Use patch explícito com justificativa técnica."
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
