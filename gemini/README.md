# Multi-Agent Orchestration para Google Gemini CLI

## O que é isso?

Uma estrutura de **orquestração por papéis virtuais** nativa para o [Gemini CLI](https://github.com/google/gemini-cli) que transforma o seu terminal em um **time de engenharia completo**.

O repositório utiliza o conceito de **Contexto Persistente** e **Comandos Customizados** para que o Gemini atue como um **Staff Engineer Orchestrator**, capaz de invocar especialistas para revisões de segurança, arquitetura, dados e implementação.

---

## Estrutura de Orquestração Nativa

A estrutura atual segue o padrão oficial do Gemini CLI:

| Componente | Arquivo / Pasta | Função |
| :--- | :--- | :--- |
| **Constituição** | `GEMINI.md` | Define o comportamento global e a persona do Orquestrador. |
| **Configuração** | `.gemini/settings.json` | Configurações do projeto e metadados. |
| **Comandos (Agentes)** | `.gemini/commands/` | Atalhos TOML que invocam papéis especializados. |
| **Base de Conhecimento** | `docs/ai/` | Documentação técnica que serve de contexto para os agentes. |

---

## Como Usar no Gemini CLI

Com o Gemini CLI instalado e configurado no repositório, você tem acesso imediato à orquestração.

### 1. Orquestração Principal (Default)
Ao iniciar uma conversa normal, o Gemini já lê o `GEMINI.md` e assume o papel de **Staff Engineer Orchestrator**. Ele coordena a visão geral e planeja as mudanças.

### 2. Comandos Multiagente (Especialistas)
Você pode invocar especialistas diretamente para tarefas específicas usando a sintaxe `/comando`:

| Comando | Papel | Quando usar |
| :--- | :--- | :--- |
| `/upgrade-plan` | **Orchestrator** | Criar planos complexos de refatoração ou migração. |
| `/review-architecture` | **Architect** | Revisar limites de sistema, resiliência e trade-offs. |
| `/software-engineer` | **Developer** | Gerar implementação mínima, pragmática e correta. |
| `/security-reviewer` | **Security** | Validar vulnerabilidades, auth e hardening. |
| `/ad-dba-reviewer` | **DBA** | Revisar modelagem de dados, queries e índices. |
| `/sre-platform-engineer`| **SRE** | Ajustar CI/CD, Terraform, Observabilidade e IaC. |
| `/tech-lead-reviewer` | **Tech Lead** | Validar simplicidade e evitar débitos técnicos. |

#### Exemplos de Uso no Terminal:

```bash
# Pedir uma revisão de segurança focada
/security-reviewer "Revise a lógica de JWT no Controller de autenticação"

# Solicitar um plano de arquitetura para um novo microsserviço
/review-architecture "Desenhe a integração assíncrona entre o Checkout e o Estoque"

# Pedir código seguindo os padrões do projeto
/software-engineer "Crie o repositório JPA para a entidade Order com suporte a paginação"
```

---

## Ordem de Consulta (Workflow)

O Orquestrador segue esta ordem lógica de raciocínio (definida em `docs/ai/orchestration/`):
1. **Diagnóstico Inicial** da demanda.
2. **Consulta aos Especialistas** pertinentes (Tech Lead -> Architect -> Security -> ...).
3. **Resolução de Conflitos** entre recomendações técnicas.
4. **Plano Final Priorizado** e entrega do código/documentação.

---

## Estrutura do Repositório

```text
gemini/
├── GEMINI.md                                              # Regras e Persona Principal
├── .gemini/
│   ├── settings.json                                      # Configuração do CLI
│   └── commands/                                          # Definição dos Comandos (Agentes)
│       ├── orchestrate/                                   # Comandos de Fluxo
│       └── roles/                                         # Comandos de Especialistas
└── docs/ai/
    ├── orchestration/                                     # Lógica do Staff Engineer
    └── roles/                                             # Detalhamento de cada Papel (MD)
```

---

## Como Adicionar um Novo Especialista

1. **Crie a documentação:** Adicione um arquivo `.md` em `docs/ai/roles/` com o escopo e regras do papel.
2. **Crie o comando:** Adicione um arquivo `.toml` em `.gemini/commands/roles/` referenciando o arquivo `.md` no campo `context`.
3. **Registre:** Adicione o novo comando na lista de comandos do `GEMINI.md`.

---

## Portabilidade para outros Projetos

Para levar essa inteligência para outro repositório:
1. Copie as pastas `.gemini/` e `docs/ai/`.
2. Copie o arquivo `GEMINI.md`.
3. Ajuste as referências de stack tecnológica no `GEMINI.md` e nos arquivos de `docs/ai/`.
