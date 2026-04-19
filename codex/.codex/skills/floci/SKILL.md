---
name: floci
description: Configura e valida o uso do Floci como emulador local de serviços AWS em desenvolvimento, testes e CI.
---

# Skill: floci

## Quando dispara
- Quando o usuário pedir integração, setup ou troubleshooting do Floci.
- Quando o projeto precisar de emulação local de serviços AWS para desenvolvimento/testes.
- Quando houver migração de LocalStack para Floci.

## Quando NÃO dispara
- Quando não há dependência de serviços AWS no fluxo local.
- Quando a necessidade é exclusivamente de infraestrutura de produção.
- Quando o problema é de contrato/lógica de negócio sem relação com emulação AWS local.

## Inputs esperados
- Stack do projeto (Java/Python/Go/Node), serviços AWS usados e ambiente (local/CI).
- Arquivos de ambiente existentes (`docker-compose`, scripts, configs SDK/CLI).
- Restrições de rede/runtime (Docker Desktop, Linux nativo, CI runner).

## Saída esperada
- Plano de integração do Floci no repositório.
- Ajustes de configuração local (compose, variáveis de ambiente, endpoint override).
- Checklist de validação com smoke tests (S3, SQS, DynamoDB no mínimo).
- Riscos conhecidos e mitigação (ex.: Lambda em Linux nativo com UFW).

## Workflow passo a passo
1. Mapear como o projeto usa AWS hoje:
- identificar serviços AWS realmente utilizados.
- localizar onde endpoint e credenciais são configurados (CLI/SDK/testes).

2. Definir estratégia de execução:
- preferir `hectorvent/floci:latest` para startup rápido e baixo consumo.
- usar `latest-jvm` apenas quando houver necessidade de maior compatibilidade de plataforma.
- para fluxos com Lambda/ECR/serviços que dependem de Docker interno, considerar bind de `/var/run/docker.sock`.

3. Configurar ambiente local:
- expor `4566:4566`.
- persistência em `./data:/app/data` (ou volume nomeado).
- variáveis mínimas para CLI/SDK:
  - `AWS_ENDPOINT_URL=http://localhost:4566`
  - `AWS_DEFAULT_REGION=us-east-1`
  - `AWS_ACCESS_KEY_ID=test`
  - `AWS_SECRET_ACCESS_KEY=test`

4. Ajustar aplicação/testes para endpoint local:
- forçar endpoint override para `http://localhost:4566`.
- manter credenciais dummy e isolar configuração local/CI para evitar uso acidental de AWS real.

5. Executar validação rápida:
- S3: criar bucket e listar objetos.
- SQS: criar fila e enviar mensagem.
- DynamoDB: criar tabela simples.
- opcional: validar serviço adicional relevante para o projeto (ex.: Lambda, ECR, EventBridge).

6. Tratar cenários de rede/plataforma:
- em Linux nativo com UFW e Lambda, abrir regra para `docker0` quando necessário.
- documentar exceções para CI runner e Docker networking.

7. Produzir artefatos finais:
- instruções objetivas de setup local.
- comandos de smoke test reproduzíveis.
- troubleshooting mínimo para falhas comuns.

## Critérios de qualidade
- Setup reproduzível em poucos passos.
- Nenhum segredo real necessário para ambiente local.
- Comandos de validação executáveis e com resultado esperado claro.
- Isolamento explícito entre ambiente local/CI e AWS de produção.

## Regras de proteção
- Nunca reutilizar credenciais reais no fluxo local de emulação.
- Não alterar endpoints de produção por padrão.
- Não declarar sucesso sem executar smoke tests básicos.
- Não expandir escopo para refatoração ampla de aplicação.
