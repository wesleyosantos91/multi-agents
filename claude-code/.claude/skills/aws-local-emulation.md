---
name: aws-local-emulation
description: "Emulação local de serviços AWS com Floci: 31+ serviços, Docker, SDK config (Java/Python/Go/Node/Terraform/CLI), storage modes, init hooks, Lambda/RDS/ElastiCache emulação. Use quando configurar ambiente local para desenvolvimento com serviços AWS. Consulte https://floci.io/floci/ via WebFetch para verificar novos serviços ou atualizações."
---

# AWS Local Emulation — Floci

Floci e um emulador local de servicos AWS, open source (MIT), sem feature gates, sem telemetria, gratuito para desenvolvimento e CI.

**Referencia oficial**: https://floci.io/floci/
**Quando verificar atualizacoes**: use WebFetch em `https://floci.io/floci/` para checar novos servicos ou mudancas de configuracao.

## Servicos suportados (31+)

| Categoria | Servicos | Protocolo |
|-----------|----------|-----------|
| **Compute** | Lambda, ECS, EC2, EKS | REST JSON, JSON 1.1, EC2 Query |
| **Containers** | ECR | REST JSON |
| **Storage** | S3 | REST XML |
| **Database** | DynamoDB + Streams | JSON 1.1 |
| **Cache** | ElastiCache (Redis/Valkey) | Query + RESP proxy |
| **Relational** | RDS (PostgreSQL/MySQL/MariaDB) | Query + wire proxy |
| **Search** | OpenSearch | REST JSON |
| **Messaging** | SQS, SNS, SES, SES v2 | Query/JSON, REST JSON |
| **Events** | EventBridge, EventBridge Scheduler | JSON 1.1, REST JSON |
| **Streaming** | Kinesis, Data Firehose | JSON 1.1 |
| **Orchestration** | Step Functions, CloudFormation | JSON 1.1, Query |
| **API** | API Gateway v1, API Gateway v2 | REST JSON |
| **Identity** | IAM, STS, Cognito | Query, JSON 1.1 |
| **Security** | KMS, Secrets Manager, ACM | JSON 1.1 |
| **Data** | Glue, Athena | JSON 1.1 |
| **Observability** | CloudWatch (Logs + Metrics) | JSON 1.1, Query |
| **Config** | AppConfig, AppConfigData | REST JSON |
| **AI** | Bedrock Runtime | REST JSON |

## Docker Compose

### Setup basico

```yaml
services:
  floci:
    image: hectorvent/floci:latest    # native image (sub-second startup)
    # image: hectorvent/floci:latest-jvm  # JVM variant (broader compatibility)
    ports:
      - "4566:4566"       # AWS API endpoint (todos os servicos)
      - "6379-6399:6379-6399"   # ElastiCache (Redis/Valkey proxy)
      - "7001-7099:7001-7099"   # RDS (PostgreSQL/MySQL proxy)
    volumes:
      - ./data:/app/data                          # persistencia
      - /var/run/docker.sock:/var/run/docker.sock  # Lambda containers, RDS, ElastiCache
    environment:
      - FLOCI_STORAGE_MODE=hybrid                  # memoria + flush async (dev)
      - FLOCI_DEFAULT_REGION=us-east-1
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4566/_floci/health"]
      interval: 10s
      timeout: 5s
      retries: 3
```

### Setup CI (sem persistencia)

```yaml
services:
  floci:
    image: hectorvent/floci:latest
    ports:
      - "4566:4566"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - FLOCI_STORAGE_MODE=memory    # sem persistencia — rapido
```

### Setup completo (com RDS + ElastiCache + Lambda)

```yaml
services:
  floci:
    image: hectorvent/floci:latest
    ports:
      - "4566:4566"
      - "6379-6399:6379-6399"   # ElastiCache proxy
      - "7001-7099:7001-7099"   # RDS proxy
    volumes:
      - floci-data:/app/data
      - /var/run/docker.sock:/var/run/docker.sock
      - ./floci/application.yml:/app/config/application.yml  # config customizada
      - ./floci/init:/app/init  # init hooks
    environment:
      - FLOCI_STORAGE_MODE=hybrid
      - FLOCI_BASE_URL=http://localhost:4566
      - FLOCI_SERVICES_LAMBDA_DEFAULT_MEMORY_MB=256
      - FLOCI_SERVICES_LAMBDA_DEFAULT_TIMEOUT_SECONDS=30
      - FLOCI_SERVICES_RDS_DEFAULT_POSTGRES_IMAGE=postgres:16-alpine
      - FLOCI_SERVICES_ELASTICACHE_DEFAULT_IMAGE=valkey/valkey:8

volumes:
  floci-data:
```

## Portas

| Porta | Servico | Notas |
|-------|---------|-------|
| **4566** | Todos os servicos AWS | Endpoint unico |
| **6379-6399** | ElastiCache proxy | Um proxy por replication group |
| **7001-7099** | RDS proxy | Um proxy por DB instance |
| **9200-9299** | Lambda Runtime API | Interno (Docker network), nao mapear |
| **5100-5199** | ECR Registry | Sidecar container, nao mapear no floci |
| **6500-6599** | EKS API Server | Apenas em modo real |
| **9400-9499** | OpenSearch | Reservado para modo real |

## Storage Modes

| Modo | Persistencia | Performance | Quando usar |
|------|-------------|-------------|-------------|
| **memory** | Nao | Maxima | CI, testes unitarios |
| **hybrid** | Sim (async flush) | Alta | **Dev local (recomendado)** |
| **persistent** | Sim (sync write) | Moderada | Dev que precisa de durabilidade total |
| **wal** | Sim (append + compact) | Alta | Workloads com muita escrita |

```yaml
# Global
floci:
  storage:
    mode: hybrid
    persistent-path: ./data

# Per-service override
    services:
      dynamodb:
        mode: persistent      # DynamoDB duravel
        flush-interval-ms: 5000
      lambda:
        mode: memory           # Lambda code nao precisa persistir
```

```bash
# Via env var
FLOCI_STORAGE_MODE=hybrid
FLOCI_STORAGE_SERVICES_DYNAMODB_MODE=persistent
```

## application.yml (configuracao completa)

```yaml
floci:
  max-request-size: 512MB
  base-url: http://localhost:4566
  default-region: us-east-1
  default-account-id: "000000000000"
  default-availability-zone: us-east-1a

  # Autenticacao (desabilitado por padrao)
  auth:
    validate-signatures: false       # true para forcar SigV4
    presign-secret: "local-emulator-secret"

  # Storage
  storage:
    mode: hybrid
    persistent-path: ./data
    wal:
      compaction-interval-ms: 30000

  # Servicos
  services:
    sqs:
      enabled: true
      default-visibility-timeout: 30
      max-message-size: 262144

    s3:
      enabled: true
      default-presign-expiry-seconds: 3600

    lambda:
      enabled: true
      ephemeral: false
      default-memory-mb: 128
      default-timeout-seconds: 3
      docker-host: unix:///var/run/docker.sock
      runtime-api-base-port: 9200
      code-path: ./data/lambda-code
      container-idle-timeout-seconds: 300
      region-concurrency-limit: 1000
      unreserved-concurrency-min: 100

    elasticache:
      enabled: true
      proxy-base-port: 6379
      default-image: "valkey/valkey:8"

    rds:
      enabled: true
      proxy-base-port: 7001
      default-postgres-image: "postgres:16-alpine"
      default-mysql-image: "mysql:8.0"
      default-mariadb-image: "mariadb:11"

    opensearch:
      enabled: true
      mode: mock           # mock ou real
      default-image: "opensearchproject/opensearch:2"

    cloudwatch-logs:
      enabled: true
      max-events-per-query: 10000

    secrets-manager:
      enabled: true
      default-recovery-window-days: 30

    ssm:
      enabled: true
      max-parameter-history: 5

    acm:
      enabled: true
      validation-wait-seconds: 0

    ecr:
      enabled: true
      registry-image: "registry:2"
      tls-enabled: false

    ecs:
      enabled: true
      mock: false          # true = skip Docker, tasks vao direto RUNNING

    iam:
      enabled: true
      enforcement-enabled: false   # true = enforce IAM policies

    # Desabilitar servico nao usado
    eks:
      enabled: false
```

## Environment Variables

Todas as config keys usam prefixo `FLOCI_` com dots/dashes convertidos para underscore:

```bash
FLOCI_BASE_URL=http://localhost:4566
FLOCI_DEFAULT_REGION=us-east-1
FLOCI_STORAGE_MODE=hybrid
FLOCI_SERVICES_SQS_DEFAULT_VISIBILITY_TIMEOUT=30
FLOCI_SERVICES_SQS_MAX_MESSAGE_SIZE=262144
FLOCI_SERVICES_LAMBDA_DEFAULT_MEMORY_MB=256
FLOCI_SERVICES_LAMBDA_DEFAULT_TIMEOUT_SECONDS=30
FLOCI_SERVICES_RDS_DEFAULT_POSTGRES_IMAGE=postgres:16-alpine
FLOCI_SERVICES_ELASTICACHE_DEFAULT_IMAGE=valkey/valkey:8
FLOCI_SERVICES_IAM_ENFORCEMENT_ENABLED=false
```

## SDK Configuration

### AWS CLI

```bash
# Configurar alias
alias awslocal='aws --endpoint-url=http://localhost:4566 --region us-east-1'

# Ou via env vars globais
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_DEFAULT_REGION=us-east-1
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test

# Usar
awslocal s3 ls
awslocal sqs list-queues
awslocal dynamodb list-tables
awslocal lambda list-functions
```

### Java (AWS SDK v2)

```java
// application-local.yml (Spring Boot)
// aws:
//   endpoint: http://localhost:4566
//   region: us-east-1

@Configuration
@Profile("local")
public class LocalAwsConfig {

    @Value("${aws.endpoint}")
    private String endpoint;

    private AwsCredentialsProvider localCredentials() {
        return StaticCredentialsProvider.create(AwsBasicCredentials.create("test", "test"));
    }

    @Bean
    public DynamoDbClient dynamoDbClient() {
        return DynamoDbClient.builder()
            .endpointOverride(URI.create(endpoint))
            .region(Region.US_EAST_1)
            .credentialsProvider(localCredentials())
            .build();
    }

    @Bean
    public SqsClient sqsClient() {
        return SqsClient.builder()
            .endpointOverride(URI.create(endpoint))
            .region(Region.US_EAST_1)
            .credentialsProvider(localCredentials())
            .build();
    }

    @Bean
    public S3Client s3Client() {
        return S3Client.builder()
            .endpointOverride(URI.create(endpoint))
            .region(Region.US_EAST_1)
            .credentialsProvider(localCredentials())
            .forcePathStyle(true)   // necessario para S3 local
            .build();
    }

    @Bean
    public LambdaClient lambdaClient() {
        return LambdaClient.builder()
            .endpointOverride(URI.create(endpoint))
            .region(Region.US_EAST_1)
            .credentialsProvider(localCredentials())
            .build();
    }
}
```

### Python (boto3)

```python
import boto3

def get_client(service: str, local: bool = False):
    kwargs = {}
    if local:
        kwargs = {
            "endpoint_url": "http://localhost:4566",
            "region_name": "us-east-1",
            "aws_access_key_id": "test",
            "aws_secret_access_key": "test",
        }
    return boto3.client(service, **kwargs)

# Uso
dynamodb = get_client("dynamodb", local=True)
sqs = get_client("sqs", local=True)
s3 = get_client("s3", local=True)
lambda_client = get_client("lambda", local=True)
```

### Go (AWS SDK v2)

```go
import (
    "context"
    "github.com/aws/aws-sdk-go-v2/aws"
    "github.com/aws/aws-sdk-go-v2/config"
    "github.com/aws/aws-sdk-go-v2/credentials"
    "github.com/aws/aws-sdk-go-v2/service/dynamodb"
)

func localConfig(ctx context.Context) (aws.Config, error) {
    return config.LoadDefaultConfig(ctx,
        config.WithRegion("us-east-1"),
        config.WithCredentialsProvider(
            credentials.NewStaticCredentialsProvider("test", "test", ""),
        ),
        config.WithEndpointResolverWithOptions(
            aws.EndpointResolverWithOptionsFunc(
                func(service, region string, opts ...interface{}) (aws.Endpoint, error) {
                    return aws.Endpoint{URL: "http://localhost:4566"}, nil
                },
            ),
        ),
    )
}

// Uso
cfg, _ := localConfig(ctx)
dynamoClient := dynamodb.NewFromConfig(cfg)
```

### Node.js (AWS SDK v3)

```javascript
import { S3Client } from "@aws-sdk/client-s3";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";

const localConfig = {
  endpoint: "http://localhost:4566",
  region: "us-east-1",
  credentials: { accessKeyId: "test", secretAccessKey: "test" },
  forcePathStyle: true,  // necessario para S3
};

const s3 = new S3Client(localConfig);
const dynamodb = new DynamoDBClient(localConfig);
```

### Terraform

```hcl
provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    dynamodb       = "http://localhost:4566"
    sqs            = "http://localhost:4566"
    sns            = "http://localhost:4566"
    s3             = "http://localhost:4566"
    lambda         = "http://localhost:4566"
    iam            = "http://localhost:4566"
    eventbridge    = "http://localhost:4566"
    secretsmanager = "http://localhost:4566"
    cloudwatch     = "http://localhost:4566"
    sts            = "http://localhost:4566"
    kms            = "http://localhost:4566"
    stepfunctions  = "http://localhost:4566"
    apigateway     = "http://localhost:4566"
    apigatewayv2   = "http://localhost:4566"
    ecr            = "http://localhost:4566"
    ecs            = "http://localhost:4566"
    rds            = "http://localhost:4566"
    kinesis        = "http://localhost:4566"
    cloudformation = "http://localhost:4566"
    ssm            = "http://localhost:4566"
    acm            = "http://localhost:4566"
    ses            = "http://localhost:4566"
    cognito        = "http://localhost:4566"
    glue           = "http://localhost:4566"
    athena         = "http://localhost:4566"
  }
}
```

## Inicializacao de recursos

```bash
#!/bin/bash
# scripts/init-local-aws.sh
ENDPOINT="http://localhost:4566"
AWS="aws --endpoint-url=$ENDPOINT --region=us-east-1"

echo "Waiting for Floci..."
until curl -s $ENDPOINT/_floci/health > /dev/null 2>&1; do sleep 1; done
echo "Floci ready"

# DynamoDB
$AWS dynamodb create-table \
    --table-name orders \
    --attribute-definitions \
        AttributeName=id,AttributeType=S \
        AttributeName=status,AttributeType=S \
        AttributeName=createdAt,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --global-secondary-indexes \
        "IndexName=status-index,KeySchema=[{AttributeName=status,KeyType=HASH},{AttributeName=createdAt,KeyType=RANGE}],Projection={ProjectionType=ALL}" \
    --billing-mode PAY_PER_REQUEST

# SQS
$AWS sqs create-queue --queue-name order-processing
$AWS sqs create-queue --queue-name order-processing-dlq
$AWS sqs set-queue-attributes \
    --queue-url http://localhost:4566/000000000000/order-processing \
    --attributes '{"RedrivePolicy":"{\"deadLetterTargetArn\":\"arn:aws:sqs:us-east-1:000000000000:order-processing-dlq\",\"maxReceiveCount\":\"3\"}"}'

# S3
$AWS s3 mb s3://order-attachments

# Secrets Manager
$AWS secretsmanager create-secret \
    --name order-service/db-password \
    --secret-string '{"password":"local-dev-password"}'

# SNS
$AWS sns create-topic --name order-events

# EventBridge
$AWS events put-rule \
    --name order-created \
    --event-pattern '{"source":["order-service"],"detail-type":["OrderCreated"]}'

echo "Local AWS resources initialized"
```

## Testes de integracao (Testcontainers)

### Java

```java
@Testcontainers
@SpringBootTest
class OrderRepositoryIT {

    @Container
    static GenericContainer<?> floci = new GenericContainer<>("hectorvent/floci:latest")
        .withExposedPorts(4566)
        .waitingFor(Wait.forHttp("/_floci/health").forStatusCode(200));

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry registry) {
        String endpoint = "http://" + floci.getHost() + ":" + floci.getMappedPort(4566);
        registry.add("aws.endpoint", () -> endpoint);
    }
}
```

### Python

```python
@pytest.fixture(scope="session")
def aws_endpoint():
    with DockerContainer("hectorvent/floci:latest").with_exposed_ports(4566) as c:
        c.wait_for_logs("Started", timeout=30)
        yield f"http://{c.get_container_host_ip()}:{c.get_exposed_port(4566)}"
```

### Go

```go
func setupFloci(t *testing.T) string {
    ctx := context.Background()
    container, err := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
        ContainerRequest: testcontainers.ContainerRequest{
            Image:        "hectorvent/floci:latest",
            ExposedPorts: []string{"4566/tcp"},
            WaitingFor:   wait.ForHTTP("/_floci/health").WithPort("4566/tcp"),
        },
        Started: true,
    })
    require.NoError(t, err)
    t.Cleanup(func() { container.Terminate(ctx) })
    endpoint, _ := container.Endpoint(ctx, "http")
    return endpoint
}
```

## Linux UFW fix

Em Linux nativo com UFW, Lambda containers podem nao alcançar o Runtime API:

```bash
# Liberar bridge Docker
sudo ufw allow in on docker0 comment 'floci: containers reach host'

# Ou mais restrito
sudo ufw allow in on docker0 to any port 9200:9299 proto tcp comment 'floci lambda runtime api'
sudo ufw allow in on docker0 to any port 5000:5099 proto tcp comment 'floci ecr registry'
```

## Makefile targets

```makefile
.PHONY: local-up local-down local-init local-reset

local-up:
	docker compose up -d floci
	@echo "Waiting for Floci..."
	@until curl -s http://localhost:4566/_floci/health > /dev/null 2>&1; do sleep 1; done
	@echo "Floci ready on http://localhost:4566"

local-init: local-up
	./scripts/init-local-aws.sh

local-down:
	docker compose down

local-reset:
	docker compose down -v
	$(MAKE) local-init
```

## Checklist

- [ ] docker-compose configurado com healthcheck `/_floci/health`?
- [ ] Docker socket montado (necessario para Lambda, RDS, ElastiCache)?
- [ ] Storage mode adequado (memory para CI, hybrid para dev)?
- [ ] SDK clients apontando para `http://localhost:4566`?
- [ ] `forcePathStyle=true` para S3?
- [ ] Script de inicializacao de recursos (tables, queues, buckets)?
- [ ] Testes de integracao usando Testcontainers + Floci?
- [ ] Terraform provider com endpoints configurados?
- [ ] AWS CLI alias `awslocal` configurado?
- [ ] Makefile com targets `local-up`, `local-init`, `local-down`?
- [ ] Portas de ElastiCache (6379+) e RDS (7001+) expostas quando usados?
- [ ] Servicos nao usados desabilitados (`enabled: false`)?
