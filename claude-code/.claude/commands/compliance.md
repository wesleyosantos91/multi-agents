Acione o `compliance-reviewer` para análise de conformidade regulatória.

## O que verificar
- Dados pessoais mapeados (LGPD/GDPR)
- Base legal para tratamento identificada
- Dados pessoais ausentes de logs, traces e métricas
- Residência de dados alinhada com região AWS (sa-east-1 para Brasil)
- Retenção e descarte de dados pessoais definidos
- Consentimento e direitos do titular
- Anonimização quando aplicável

## Escopo
- Se `$ARGUMENTS` estiver vazio, analise todo o projeto
- Se `$ARGUMENTS` contiver um módulo ou fluxo, foque nele

## Entrada do usuário
$ARGUMENTS
