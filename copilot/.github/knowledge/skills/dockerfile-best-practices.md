---
name: dockerfile-best-practices
description: "Cria ou revisa Dockerfile seguindo boas práticas de segurança e performance. Use quando pedirem para criar Dockerfile, otimizar imagem Docker ou revisar container."
---

# Dockerfile — Best Practices

Crie ou revise Dockerfiles seguindo boas práticas de segurança, performance e manutenibilidade.

## Regras mandatórias

### Segurança
- **Nunca rodar como root**: adicionar `USER nonroot` ou `USER 1001`
- **Imagem base minimal**: preferir `distroless`, `alpine` ou `-slim`
- **Tag específica**: nunca `FROM node:latest` → `FROM node:22-alpine`
- **Sem segredos no build**: nunca `COPY .env` ou `ARG PASSWORD=...`
- **Scan de vulnerabilidades**: `trivy image <image>` antes de push

### Performance
- **Multi-stage build**: separar build de runtime
- **Cache de dependências**: copiar lockfile antes do código
- **Ordenar layers**: do menos ao mais mutável
- **`.dockerignore`**: excluir `.git`, `node_modules`, `target/`, `__pycache__/`, etc.

## Templates por linguagem

### Java (Maven + distroless)
```dockerfile
FROM eclipse-temurin:25-jdk-alpine AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src
RUN mvn package -DskipTests -B

FROM gcr.io/distroless/java25-debian12:nonroot
COPY --from=build /app/target/*.jar /app/app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

### Python (uv + distroless)
```dockerfile
FROM python:3.13-slim AS build
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev
COPY src ./src

FROM gcr.io/distroless/python3-debian12:nonroot
WORKDIR /app
COPY --from=build /app/.venv /app/.venv
COPY --from=build /app/src ./src
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8080
ENTRYPOINT ["python", "-m", "src.main"]
```

### Go (scratch)
```dockerfile
FROM golang:1.24-alpine AS build
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/server ./cmd/server

FROM scratch
COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=build /app/server /server
USER 1001
EXPOSE 8080
ENTRYPOINT ["/server"]
```

### Node.js
```dockerfile
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --production=false
COPY . .
RUN npm run build

FROM node:22-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package.json .
USER 1001
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## Checklist
- [ ] Multi-stage build?
- [ ] Imagem base com tag específica (não latest)?
- [ ] USER não-root definido?
- [ ] Cache de dependências otimizado?
- [ ] .dockerignore configurado?
- [ ] Sem segredos na imagem?
- [ ] HEALTHCHECK definido (quando aplicável)?
