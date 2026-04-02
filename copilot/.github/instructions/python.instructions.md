---
applyTo: "**/*.py,**/pyproject.toml,**/requirements*.txt,**/uv.lock,**/poetry.lock"
---
# Python Instructions

- Use `pyproject.toml` como unico ponto de configuracao — nao misture com `setup.cfg`, `setup.py` ou `.flake8`.
- Mantenha lockfile reprodutivel versionado no repositorio (`uv.lock`, `poetry.lock` ou `requirements.txt` com hashes).
- Type hints obrigatorios em todo codigo de producao.
- Adote `src/<package>/` layout para evitar importacoes ambiguas.
- Sem `utils.py` generico — nomear por responsabilidade de dominio.
- Handler Lambda fino: recebe evento → delega para `service.py` → retorna. Sem logica de negocio no handler.
- `except` com tipo especifico — nunca `except Exception: pass`.
- Sempre considerar impacto em testes (`pytest`, fixtures, parametrize).

## Referencias

- `docs/ai/roles/python-specialist.md`
- `docs/ai/roles/software-engineer.md`
- `docs/ai/orchestration/staff-engineer-orchestrator.md`
