# Base Enterprise Multiagente para Codex

Esta base foi desenhada para operação profissional com Codex em repositórios de engenharia de software moderna, com foco em:
- governança forte
- revisão multiagente
- especialização por domínio
- segurança, compliance, dados, performance, QA, SRE, CI/CD, custo e documentação

## Arquitetura da solução
A estrutura separa responsabilidades em camadas:
- Governança global: `AGENTS.md`
- Configuração do projeto: `.codex/config.toml`
- Agentes especializados: `.codex/agents/*.toml`
- Skills/workflows reutilizáveis: `.codex/skills/*/SKILL.md`
- Hooks de lifecycle: `.codex/hooks.json` + `.codex/hooks/*.py`
- Templates e referências: `.codex/templates/*`, `.codex/references/*`

## Fluxo operacional recomendado
1. Entrar por `staff-engineer-orchestrator` em demanda não trivial.
2. Rodar especialistas por risco e escopo.
3. Consolidar recomendações e resolver conflitos.
4. Implementar a menor mudança correta.
5. Validar com evidências e preparar pre-PR.

## Catálogo de agentes
Total: 24 agentes especializados.

- `staff-engineer-orchestrator`
- `dependency-versions-reviewer`
- `tech-lead-reviewer`
- `architect-reviewer`
- `api-contract-reviewer`
- `security-reviewer`
- `compliance-reviewer`
- `ad-dba-reviewer`
- `data-engineering-aws-architect`
- `java-specialist`
- `jakarta-ee-specialist`
- `python-specialist`
- `go-specialist`
- `frontend-specialist`
- `mobile-native-specialist`
- `software-engineer`
- `sre-platform-engineer`
- `cicd-pipeline-engineer`
- `incident-response-reviewer`
- `finops-reviewer`
- `devex-reviewer`
- `qa-quality-engineer`
- `performance-reliability-reviewer`
- `tech-writer`

## Catálogo de skills
Total: 34 workflows canônicos (paridade alta com `EXEMPLO/.claude/commands` + integração Floci).

- `review`
- `full-review`
- `implement`
- `pre-pr`
- `arch-review`
- `security-check`
- `compliance`
- `contract-review`
- `check-deps`
- `data-review`
- `data-platform`
- `qa-review`
- `perf-review`
- `sre-review`
- `cicd-review`
- `finops`
- `floci`
- `incident-readiness`
- `local-setup`
- `docs`
- `adr`
- `changelog`
- `debug`
- `explain`
- `health-check`
- `hotfix`
- `migrate`
- `optimize`
- `quick-fix`
- `refactor`
- `runbook`
- `scaffold`
- `tech-debt`
- `test-gen`

## Decisão de design sobre skills
As skills canônicas deste projeto ficam em `.codex/skills` e são registradas explicitamente em `[[skills.config]]` no `.codex/config.toml`.

## Compatibilidade de hooks no Windows
Hooks do Codex são experimentais e, conforme documentação oficial atual, permanecem desabilitados em runtime Windows.
Mesmo assim, os arquivos de hook são mantidos para Linux/macOS/CI e para facilitar migração futura.

## Estrutura final
```text
.
├─ AGENTS.md
├─ README.md
└─ .codex/
   ├─ config.toml
   ├─ hooks.json
   ├─ hooks/
   ├─ agents/
   ├─ skills/
   ├─ templates/
   └─ references/
```
