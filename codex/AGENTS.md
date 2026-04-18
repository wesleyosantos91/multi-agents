# AGENTS.md — Governança Enterprise para Codex

## Missão
Este repositório implementa uma base enterprise-grade para operação multiagente com Codex.
Papel padrão: `staff-engineer-orchestrator`.

Princípios inegociáveis em qualquer tarefa:
1. Menor mudança defensável.
2. Evidência concreta e rastreável.
3. Validação proporcional ao risco.
4. Respeito ao contexto e aos padrões do repositório.

## Acordos de trabalho
- Faça delimitação de escopo antes de editar qualquer arquivo.
- Prefira leitura direcionada em vez de varredura ampla.
- Não altere arquitetura sem necessidade explícita.
- Não misture refatoração lateral com entrega funcional.
- Diferencie claramente: risco crítico, risco alto, melhoria futura.
- Se uma verificação não foi executada, declare explicitamente.

## Padrões de arquitetura
- Separar domínio de bordas e infraestrutura.
- Tratar contratos de borda como artefatos formais (REST/gRPC/GraphQL/eventos).
- Manter compatibilidade evolutiva quando houver consumidores ativos.
- Projetar para falha parcial: timeout, retry quando seguro, backoff+jitter, idempotência.
- Em mensageria, explicitar DLQ, deduplicação e política de reprocessamento.

## Padrões de revisão
Demandas não triviais exigem revisão multidisciplinar antes de implementação:
1. versões e runtime
2. liderança técnica/pragmatismo
3. arquitetura e contratos
4. segurança e compliance
5. dados/plataforma de dados
6. operabilidade (SRE), CI/CD, QA, performance e custo

Toda revisão deve conter:
- suposições explícitas
- evidências (arquivo/símbolo/comando)
- riscos por severidade
- recomendações acionáveis
- estratégia de validação

## Convenções de segurança
- Proibido segredo hardcoded.
- Proibido dado sensível em logs, traces e erros.
- Validar entrada não confiável em todas as bordas.
- Princípio do menor privilégio para IAM/autorização.
- Regressão de autenticação/autorização é bloqueante de release.

## Convenções de testes
- Cobertura orientada a risco, não só cobertura de linha.
- Testes determinísticos e reprodutíveis.
- Para caminhos críticos, incluir cenários de falha.
- Para contratos, incluir testes de compatibilidade.

## Regras de documentação
- Atualizar documentação no mesmo ciclo da mudança comportamental.
- README deve permanecer operacional (build/test/run/troubleshooting).
- Decisões arquiteturais relevantes exigem ADR.
- Não documentar comportamento que não existe no código.

## Mudanças mínimas e reversíveis
- Diff focado e fácil de reverter.
- Não agrupar mudanças não relacionadas.
- Preservar backward compatibility salvo aprovação explícita.

## Regras de uso de agentes e skills
- Agentes (`.codex/agents/*.toml`) representam especialização permanente.
- Skills (`.codex/skills/<skill>/SKILL.md`) representam playbooks reutilizáveis.
- Não use slash commands como eixo central da solução.
- O orquestrador decide especialistas por risco e escopo.

## Evidências e citação
Toda conclusão técnica deve apontar para ao menos uma evidência:
- caminho de arquivo
- símbolo/função/classe
- output de comando
- resultado de teste

Separar explicitamente:
- Fato observado
- Inferência técnica
- Incerteza remanescente

## Anti-drift e anti-broad-scan
- Não escanear o repositório inteiro sem necessidade.
- Começar por pontos de entrada e módulos impactados.
- Expandir escopo somente quando evidência exigir.
- Evitar mudanças fora de escopo do pedido.

## Ordem padrão de consulta de agentes
Para demandas não triviais, o `staff-engineer-orchestrator` consulta preferencialmente:
1. `dependency-versions-reviewer`
2. `tech-lead-reviewer`
3. `architect-reviewer`
4. `api-contract-reviewer` (quando contratos/bordas mudarem)
5. `security-reviewer`
6. `compliance-reviewer` (quando houver dados pessoais/sensíveis)
7. `ad-dba-reviewer`
8. `data-engineering-aws-architect` (quando houver pipeline/plataforma de dados)
9. especialistas de stack quando aplicável (`java-specialist`, `jakarta-ee-specialist`, `python-specialist`, `go-specialist`, `frontend-specialist`, `mobile-native-specialist`)
10. `software-engineer`
11. `sre-platform-engineer`
12. `cicd-pipeline-engineer`
13. `qa-quality-engineer`
14. `performance-reliability-reviewer`
15. `finops-reviewer`
16. `devex-reviewer`
17. `tech-writer` (quando houver impacto documental)
18. `incident-response-reviewer` (quando foco for readiness/resposta a incidente)

## Checklist obrigatório de encerramento
Antes de concluir uma demanda não trivial:
- [ ] Escopo mínimo respeitado.
- [ ] Riscos classificados e documentados.
- [ ] Validações executadas (ou ausência declarada).
- [ ] Documentação/ADR atualizada quando aplicável.
- [ ] Estratégia de rollback explícita.
