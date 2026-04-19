Crie a estrutura de um novo módulo/componente seguindo os padrões do projeto.

## Processo obrigatório

### 1. Detecção de padrões
- Leia a estrutura de módulos existentes no projeto (Glob + Read)
- Identifique convenções: nomes de pacotes, organização de pastas, configuração, testes
- Identifique o padrão de build (pom.xml, build.gradle, pyproject.toml, go.mod)

### 2. Scaffolding
- Crie a estrutura seguindo **exatamente** os padrões detectados
- Inclua: código principal, testes, configuração, build file
- Siga a arquitetura definida no CLAUDE.md (web/, message/, core/, domain/, infrastructure/)
- Use as versões de dependências já existentes no projeto — não invente versões

### 3. Validação
- Confirme que o build compila/importa sem erros
- Confirme que os testes do scaffold passam
- Confirme que a estrutura é consistente com os módulos existentes

### 4. Output
Entregue:
- **Arquivos criados**: lista completa
- **Padrões seguidos**: quais módulos existentes serviram de referência
- **Próximos passos**: o que o desenvolvedor precisa fazer para completar a implementação

## Agentes disponíveis (quando necessário)
- Se envolver dependências novas: acione `dependency-versions-reviewer` antes de criar
- Para a criação: use `software-engineer`
- Para validar aderência: acione `tech-lead-reviewer`

## O que criar
$ARGUMENTS
