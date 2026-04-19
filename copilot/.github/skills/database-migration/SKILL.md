---
name: database-migration
description: Skill importada do EXEMPLO (database-migration.md).
allowed-tools: "read,search"
user-invocable: true
---

# Skill

---
name: database-migration
description: "Cria ou revisa migrações de banco de dados seguras. Use quando pedirem para criar migration, alterar schema, ou adicionar coluna/tabela."
---

# Database Migration — Safe Practices

Crie ou revise migrações de banco de dados com segurança para produção.

## Regras de ouro

### 1. Toda migração deve ser reversível
- Sempre crie o script de rollback junto com a migração
- Teste o rollback antes de aplicar em produção

### 2. Zero-downtime migrations
Nunca faça operações que lockam tabelas em produção:

| Operação | Segura? | Alternativa |
|----------|---------|-------------|
| ADD COLUMN (nullable) | Sim | — |
| ADD COLUMN (NOT NULL + default) | Depende do DB | Adicionar nullable → backfill → add constraint |
| DROP COLUMN | Sim (cuidado com código) | Deploy código primeiro, depois drop |
| RENAME COLUMN | Não | Add new → backfill → migrate code → drop old |
| ADD INDEX | Depende | `CREATE INDEX CONCURRENTLY` (Postgres) |
| ALTER TYPE | Não | Add new column → migrate → drop old |
| DROP TABLE | Sim (cuidado) | Confirmar que nenhum código referencia |

### 3. Expand-and-contract pattern
Para mudanças incompatíveis:
1. **Expand**: adicione a nova estrutura (nova coluna, novo formato)
2. **Migrate code**: atualize o código para ler/escrever ambos
3. **Backfill**: migre dados antigos para o novo formato
4. **Contract**: remova a estrutura antiga

### 4. Backfill seguro
- Nunca `UPDATE table SET column = value` em tabelas grandes — faça em batches
- Use transações por batch
- Monitore locks e performance durante backfill
- Backfill em horário de baixo tráfego quando possível

## Naming convention
```
V{version}__{description}.sql     # Flyway
{timestamp}_{description}.sql     # Alembic/Django
{number}_{description}.up.sql     # golang-migrate
```

Exemplos:
```
V001__create_orders_table.sql
V002__add_status_column_to_orders.sql
V003__create_index_orders_status.sql
```

## Template de migração

```sql
-- Migration: {descrição}
-- Author: {nome}
-- Date: {data}
-- Reversible: yes/no

-- UP
ALTER TABLE orders ADD COLUMN status VARCHAR(50);
CREATE INDEX CONCURRENTLY idx_orders_status ON orders(status);

-- DOWN (rollback)
DROP INDEX IF EXISTS idx_orders_status;
ALTER TABLE orders DROP COLUMN IF EXISTS status;
```

## Checklist
- [ ] Rollback script existe?
- [ ] Testado em staging com dados similares a produção?
- [ ] Não locka tabelas grandes?
- [ ] Backfill em batches (se aplicável)?
- [ ] Código compatível com antes e depois da migração?
- [ ] Índices criados com CONCURRENTLY (quando suportado)?
- [ ] Monitoramento durante aplicação planejado?
