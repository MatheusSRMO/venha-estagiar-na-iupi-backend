# Dockerfile para a Expense Control API
# Utiliza multi-stage build para otimização da imagem final

# Stage 1: Base image
FROM python:3.12-slim AS base

# Evita criação de arquivos .pyc e buffer de stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Stage 2: Dependencies
FROM base AS dependencies

# Instala dependências do sistema necessárias para compilação
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Production
FROM base AS production

# Cria usuário não-root para segurança
RUN addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 appuser

# Copia dependências instaladas do stage anterior
COPY --from=dependencies /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copia código fonte da aplicação
COPY --chown=appuser:appgroup . .

# Alterna para usuário não-root
USER appuser

# Porta exposta pela aplicação
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
