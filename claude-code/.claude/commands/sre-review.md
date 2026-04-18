Acione o `sre-platform-engineer` para análise de operabilidade e plataforma.

## Escopo
- Se `$ARGUMENTS` estiver vazio, analise o projeto/branch atual
- Se `$ARGUMENTS` contiver um módulo ou aspecto operacional, foque nele

## O que avaliar
- Deployability e rollback
- Readiness/liveness probes
- Logs estruturados (JSON)
- Métricas e tracing distribuído
- Terraform: organização, state, naming
- Docker e ambiente local
- Lambda versions/aliases, deploy strategy
- CloudWatch Alarms configurados
- Ministack cobrindo serviços AWS

## Entrada do usuário
$ARGUMENTS
