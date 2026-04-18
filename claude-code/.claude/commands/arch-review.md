Acione o `architect-reviewer` para uma análise arquitetural focada.

## Escopo
- Se `$ARGUMENTS` estiver vazio, analise a arquitetura do projeto ou branch atual
- Se `$ARGUMENTS` contiver um módulo ou decisão, foque nele

## O que avaliar
- Boundaries entre camadas
- Acoplamento e coesão
- Trade-offs técnicos
- Resiliência e tolerância a falhas
- Decisão de modelo de execução (Lambda vs container vs batch vs Step Functions)
- Compatibilidade evolutiva de contratos
- Separação correta: web/ (borda síncrona), message/ (borda assíncrona), domain/, infrastructure/, core/

## Entrada do usuário
$ARGUMENTS
