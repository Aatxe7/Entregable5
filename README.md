# Entregable 5 — Flask + PostgreSQL + Docker Compose + Azure CI/CD

## Local
1) Copia `.env.example` a `.env`  
2) Ejecuta:
```bash
docker compose up --build
```
3) Prueba:
- http://localhost:5000/
- http://localhost:5000/health

## Pruebas
Con la app levantada:
```bash
pip install -r requirements-dev.txt
pytest -q
```

## Azure + CI/CD
Workflow: `.github/workflows/azure-ci-cd.yml`.

Secrets requeridos:
- AZURE_CREDENTIALS
- AZURE_RESOURCE_GROUP
- AZURE_CONTAINERAPP_NAME
- AZURE_CONTAINERAPPS_ENV
- AZURE_ACR_NAME
