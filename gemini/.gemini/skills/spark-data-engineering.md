# Apache Spark — Data Engineering Patterns

Padroes e idiomas para Spark em pipelines de dados de producao.

## Quando usar Spark

| Cenario | Spark? | Alternativa |
|---------|--------|-------------|
| Batch > 1GB | Sim | — |
| Batch < 100MB | Nao | Lambda + Pandas / DuckDB |
| Streaming com janelas | Sim (Structured Streaming) | Kinesis Analytics / Flink |
| ETL simples S3→S3 | Depende do volume | AWS Glue (Spark managed) |
| ML feature engineering | Sim | — |
| Ad-hoc query em data lake | Nao | Athena / Redshift Spectrum |

## PySpark — Estrutura de projeto

```
data-pipeline/
├── src/
│   ├── jobs/
│   │   ├── __init__.py
│   │   ├── ingest_orders.py       # Job de ingestao
│   │   ├── transform_orders.py    # Job de transformacao
│   │   └── publish_metrics.py     # Job de publicacao
│   ├── transforms/
│   │   ├── __init__.py
│   │   ├── orders.py              # Transformacoes de orders
│   │   └── common.py              # Transformacoes reutilizaveis
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── orders.py              # StructType schemas
│   ├── quality/
│   │   ├── __init__.py
│   │   └── checks.py              # Data quality checks
│   └── utils/
│       ├── __init__.py
│       ├── spark_session.py        # SparkSession factory
│       └── io.py                   # Read/write helpers
├── tests/
│   ├── conftest.py                 # SparkSession fixture
│   ├── test_transforms.py
│   └── test_quality.py
├── config/
│   ├── dev.yaml
│   ├── staging.yaml
│   └── prod.yaml
├── pyproject.toml
└── Dockerfile
```

## SparkSession factory

```python
from pyspark.sql import SparkSession

def create_spark_session(app_name: str, env: str = "local") -> SparkSession:
    builder = SparkSession.builder.appName(app_name)

    if env == "local":
        builder = (builder
            .master("local[*]")
            .config("spark.sql.shuffle.partitions", "4")
            .config("spark.driver.memory", "2g"))
    else:
        builder = (builder
            .config("spark.sql.adaptive.enabled", "true")
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer"))

    return builder.getOrCreate()
```

## Schemas explícitos (nunca inferir em producao)

```python
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

ORDER_SCHEMA = StructType([
    StructField("id", StringType(), nullable=False),
    StructField("customer_id", StringType(), nullable=False),
    StructField("title", StringType(), nullable=False),
    StructField("amount", DoubleType(), nullable=False),
    StructField("status", StringType(), nullable=False),
    StructField("created_at", TimestampType(), nullable=False),
])

# Leitura com schema explicito
df = spark.read.schema(ORDER_SCHEMA).parquet("s3://bucket/raw/orders/")
```

## Transformacoes (funcoes puras)

```python
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def add_order_category(df: DataFrame) -> DataFrame:
    """Adiciona categoria baseada no valor do pedido."""
    return df.withColumn(
        "category",
        F.when(F.col("amount") >= 1000, "premium")
         .when(F.col("amount") >= 100, "standard")
         .otherwise("basic"),
    )

def filter_valid_orders(df: DataFrame) -> DataFrame:
    """Remove pedidos invalidos."""
    return df.filter(
        (F.col("id").isNotNull())
        & (F.col("amount") > 0)
        & (F.col("status").isin("pending", "confirmed", "shipped", "delivered"))
    )

def enrich_with_date_parts(df: DataFrame, col_name: str = "created_at") -> DataFrame:
    """Adiciona colunas de particionamento por data."""
    return (df
        .withColumn("year", F.year(F.col(col_name)))
        .withColumn("month", F.month(F.col(col_name)))
        .withColumn("day", F.dayofmonth(F.col(col_name))))

# Composicao de transformacoes
result = (raw_orders
    .transform(filter_valid_orders)
    .transform(add_order_category)
    .transform(enrich_with_date_parts))
```

## Particionamento e escrita

```python
# Escrita particionada (Parquet)
(df
    .repartition("year", "month")
    .write
    .mode("overwrite")
    .partitionBy("year", "month")
    .parquet("s3://bucket/curated/orders/"))

# Delta Lake (quando disponivel)
(df
    .write
    .format("delta")
    .mode("merge")
    .option("mergeSchema", "true")
    .save("s3://bucket/curated/orders/"))

# Controle de tamanho de arquivos
(df
    .coalesce(target_files)  # Reducao sem shuffle
    .write
    .option("maxRecordsPerFile", 1_000_000)
    .parquet(output_path))
```

## Data Quality checks

```python
from dataclasses import dataclass

@dataclass
class QualityResult:
    check: str
    passed: bool
    details: str

def check_not_null(df: DataFrame, columns: list[str]) -> list[QualityResult]:
    results = []
    for col in columns:
        null_count = df.filter(F.col(col).isNull()).count()
        results.append(QualityResult(
            check=f"not_null:{col}",
            passed=null_count == 0,
            details=f"{null_count} nulls found",
        ))
    return results

def check_uniqueness(df: DataFrame, columns: list[str]) -> QualityResult:
    total = df.count()
    distinct = df.select(*columns).distinct().count()
    return QualityResult(
        check=f"unique:{','.join(columns)}",
        passed=total == distinct,
        details=f"{total - distinct} duplicates found",
    )

def check_freshness(df: DataFrame, col: str, max_hours: int) -> QualityResult:
    max_ts = df.agg(F.max(col)).collect()[0][0]
    age_hours = (datetime.now() - max_ts).total_seconds() / 3600
    return QualityResult(
        check=f"freshness:{col}",
        passed=age_hours <= max_hours,
        details=f"Latest record: {age_hours:.1f}h ago (max: {max_hours}h)",
    )
```

## Structured Streaming

```python
# Leitura de Kafka
orders_stream = (spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "broker:9092")
    .option("subscribe", "orders")
    .option("startingOffsets", "latest")
    .option("maxOffsetsPerTrigger", 10000)
    .load()
    .select(F.from_json(F.col("value").cast("string"), ORDER_SCHEMA).alias("data"))
    .select("data.*"))

# Transformacao + escrita
query = (orders_stream
    .transform(filter_valid_orders)
    .transform(add_order_category)
    .writeStream
    .format("parquet")
    .option("checkpointLocation", "s3://bucket/checkpoints/orders/")
    .option("path", "s3://bucket/streaming/orders/")
    .trigger(processingTime="5 minutes")
    .partitionBy("year", "month", "day")
    .start())
```

## AWS Glue

```python
# Job Glue com GlueContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ["JOB_NAME", "SOURCE_PATH", "TARGET_PATH"])
glueContext = GlueContext(SparkContext())
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Dynamic Frame → DataFrame
dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database="raw_db",
    table_name="orders",
)
df = dynamic_frame.toDF()

# Transformacoes Spark normais
result = df.transform(filter_valid_orders).transform(add_order_category)

# Escrita
(result.write
    .mode("overwrite")
    .format("parquet")
    .save(args["TARGET_PATH"]))

job.commit()
```

## Performance tuning

| Problema | Solucao |
|----------|---------|
| Shuffle excessivo | `spark.sql.adaptive.enabled=true` |
| Partitions demais apos join | `coalescePartitions.enabled=true` |
| Skew em joins | `spark.sql.adaptive.skewJoin.enabled=true` |
| OOM no driver | `spark.driver.memory`, evitar `.collect()` |
| OOM nos executors | `spark.executor.memory`, reduzir `shuffle.partitions` |
| Arquivos pequenos | `coalesce()` antes de escrever |
| Scan completo | Particionar por colunas de filtro frequente |

```python
# Broadcast join para tabelas pequenas (< 10MB)
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_df), "key")

# Cache para DataFrames reutilizados
df.cache()  # ou .persist(StorageLevel.MEMORY_AND_DISK)
df.count()  # materializa o cache
# ... multiplas operacoes no df ...
df.unpersist()
```

## Testing

```python
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    return (SparkSession.builder
        .master("local[2]")
        .appName("test")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate())

def test_add_order_category(spark):
    data = [("1", 1500.0), ("2", 500.0), ("3", 50.0)]
    df = spark.createDataFrame(data, ["id", "amount"])
    result = add_order_category(df).collect()
    categories = {row["id"]: row["category"] for row in result}
    assert categories == {"1": "premium", "2": "standard", "3": "basic"}

def test_filter_valid_orders(spark):
    data = [("1", 100.0, "pending"), ("2", -1.0, "pending"), ("3", 50.0, "invalid")]
    df = spark.createDataFrame(data, ["id", "amount", "status"])
    result = filter_valid_orders(df)
    assert result.count() == 1
```

## Checklist

- [ ] Schema explicito (nunca inferSchema em producao)?
- [ ] Transformacoes como funcoes puras (DataFrame → DataFrame)?
- [ ] Particionamento por colunas de filtro frequente?
- [ ] Adaptive Query Execution habilitado?
- [ ] Data quality checks antes de publicar?
- [ ] Checkpoint para streaming jobs?
- [ ] Broadcast join para tabelas pequenas?
- [ ] Sem .collect() em datasets grandes?
- [ ] Controle de tamanho de arquivos de saida?
- [ ] Testes unitarios com SparkSession local?
