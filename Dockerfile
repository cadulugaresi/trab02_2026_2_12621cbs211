FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN useradd --create-home inventario && mkdir -p /app/dados && chown inventario /app/dados

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY iniciar_api.py .
COPY inventario/ inventario/

USER inventario

WORKDIR /app/dados

HEALTHCHECK CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/saude')"

EXPOSE 5000
CMD ["python3", "/app/iniciar_api.py"]
