---
name: terraform-module
description: "Cria ou revisa módulos Terraform seguindo boas práticas. Use quando pedirem para criar infra, módulo Terraform, ou revisar IaC."
argument-hint: "[contexto adicional]"
---

# Terraform Module — Best Practices

Crie ou revise módulos Terraform seguindo boas práticas.

## Estrutura de módulo

```
modules/<nome>/
├── main.tf           # Recursos principais
├── variables.tf      # Variáveis de entrada (todas documentadas)
├── outputs.tf        # Outputs (todos documentados)
├── versions.tf       # Required providers e terraform version
├── locals.tf         # Valores computados (opcional)
├── data.tf           # Data sources (opcional)
└── README.md         # Documentação do módulo
```

## Regras mandatórias

### Variáveis
- Toda variável tem `description` e `type`
- Variáveis sensíveis marcadas com `sensitive = true`
- Defaults razoáveis quando possível
- Validação com `validation` block quando há restrições

```hcl
variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

### Outputs
- Outputs essenciais para composição (ARN, ID, endpoint)
- Todos com `description`

### Naming
- Recursos: `<service>-<component>-<environment>` (ex: `order-api-prod`)
- Tags obrigatórias: `Environment`, `Service`, `ManagedBy=terraform`
- Use `locals` para naming patterns consistentes

```hcl
locals {
  name_prefix = "${var.service}-${var.environment}"
  common_tags = {
    Environment = var.environment
    Service     = var.service
    ManagedBy   = "terraform"
  }
}
```

### State
- Remote state em S3 com encryption
- DynamoDB lock table
- Nunca commitar `.tfstate`
- State separado por ambiente

### Segurança
- Sem segredos hardcoded — use `aws_secretsmanager_secret` ou variáveis
- IAM com menor privilégio — nunca `"*"` em actions
- Security groups: deny by default, allow específico
- Encryption at rest habilitado (S3, RDS, DynamoDB, EBS)

## Checklist
- [ ] `terraform fmt` passou?
- [ ] `terraform validate` passou?
- [ ] Todas variáveis documentadas?
- [ ] Outputs relevantes expostos?
- [ ] Tags obrigatórias presentes?
- [ ] Sem segredos hardcoded?
- [ ] IAM com menor privilégio?
- [ ] Encryption at rest configurado?
- [ ] Remote state configurado?
