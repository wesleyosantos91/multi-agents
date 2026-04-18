Acione o `tech-writer` para revisar, criar ou atualizar documentação técnica.

## Escopo
- Se `$ARGUMENTS` contiver "review" ou estiver vazio, faça diagnóstico da documentação existente
- Se `$ARGUMENTS` contiver "create", crie a documentação faltante
- Se `$ARGUMENTS` contiver um componente ou fluxo, documente especificamente ele

## O que o tech-writer faz
1. Lê o repositório antes de documentar (nunca inventa comandos)
2. Diagnostica estado atual da documentação
3. Cria ou atualiza: README, getting-started, local-development, testing, troubleshooting, project-structure
4. Cria ADRs quando há decisões arquiteturais não documentadas
5. Reporta lacunas que exigem validação humana

## Entrada do usuário
$ARGUMENTS
