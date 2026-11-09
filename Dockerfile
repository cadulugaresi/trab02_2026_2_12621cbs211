FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN useradd --create-home inventario && mkdir -p /app/dados && chown inventario /app/dados

WORKDIR /app

COPY main.py .
COPY inventario/ inventario/

USER inventario

WORKDIR /app/dados

HEALTHCHECK CMD python3 -c "import sqlite3; sqlite3.connect('inventario.db').execute('SELECT 1')"

CMD ["python3", "/app/main.py"]
