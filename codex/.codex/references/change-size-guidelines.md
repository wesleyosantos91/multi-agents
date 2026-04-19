# Diretrizes de Tamanho de Mudança

## Preferencial
- Uma mudança comportamental por PR
- Conjunto de arquivos focado
- Menor blast radius possível

## Permitido com justificativa
- Mudança multi-módulo quando exigida por um único comportamento
- Alteração coordenada de contrato + implementação

## Evitar
- Misturar cleanup amplo com feature/fix
- Refatoração sem necessidade objetiva
- Breaking change implícito
