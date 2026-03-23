# Entregable 5 — Flask + PostgreSQL + Docker Compose + Azure (ACR + Container Apps) + CI/CD

Repositorio: https://github.com/Aatxe7/Entregable5  
URL producción (Azure Container Apps):  
https://ca-entregable5-backend.bravecliff-1b5dc50e.spaincentral.azurecontainerapps.io  
Health check (producción):  
https://ca-entregable5-backend.bravecliff-1b5dc50e.spaincentral.azurecontainerapps.io/health  

---

## 1) Descripción del proyecto

Backend en **Flask** conectado a **PostgreSQL**, con:

- Ejecución local con **Docker Compose** (backend + postgres).
- Imagen Docker construida con **Dockerfile**.
- Imagen publicada en **Azure Container Registry (ACR)**.
- Despliegue en **Azure Container Apps** con ingress externo.
- **CI** en GitHub Actions: tests + build + push a ACR.
- **Monitorización** con logs mediante Azure CLI.

### Endpoints

- `GET /` → página de confirmación  
- `GET /health` → estado + conexión a BD (db ok/error)  
- `POST /notes` → crea una nota `{ "title": "..." }`  
- `GET /notes` → lista notas (persistencia)  

---

## 2) Estructura del repositorio

- `app.py` → backend Flask  
- `tests/` → pruebas automáticas (pytest)  
- `Dockerfile` → construcción de imagen  
- `docker-compose.yml` → orquestación local (backend + postgres)  
- `requirements.txt` / `requirements-dev.txt`  
- `.env.example` → plantilla de variables (NO subir `.env`)  
- `.github/workflows/ci-acr.yml` → CI (tests + build + push a ACR)  
- `evidencias/` → capturas del proyecto  

---

## 3) Ejecutar en local (Docker Compose)

### 3.1 Preparar variables

1) Copia `.env.example` a `.env` (**NO subir `.env` al repo**).  
   - Windows: duplica el archivo y renómbralo a `.env`

2) Levanta los servicios:

```bash
docker compose up --build
3.2 Probar localmente
http://localhost:5000/
http://localhost:5000/health

Crear y listar notas:

PowerShell

Invoke-RestMethod -Method Post -Uri http://localhost:5000/notes -ContentType "application/json" -Body '{"title":"primera nota"}'
Invoke-RestMethod -Method Get -Uri http://localhost:5000/notes
4) Pruebas (pytest)

Con la app levantada en local:

pip install -r requirements-dev.txt
pytest -q
5) Azure (ACR + PostgreSQL + Container Apps)
Recursos usados
Resource Group: rg-entregable5
ACR: acrentregable5aatxe7.azurecr.io
Container App: ca-entregable5-backend
PostgreSQL Flexible Server: pg-entregable5-aatxe7 (DB: appdb)
Región: spaincentral
5.1 Subida de imagen a ACR (manual, primera vez)
az acr login --name acrentregable5aatxe7

docker build -t mi-backend:v1 .
docker tag mi-backend:v1 acrentregable5aatxe7.azurecr.io/mi-backend:v1
docker push acrentregable5aatxe7.azurecr.io/mi-backend:v1
5.2 Despliegue/actualización de Container App (manual)
az containerapp update --name ca-entregable5-backend --resource-group rg-entregable5 --image acrentregable5aatxe7.azurecr.io/mi-backend:latest
6) CI/CD (GitHub Actions)
Workflow principal (operativo)
.github/workflows/ci-acr.yml
Etapas:
test (pytest + postgres service)
build_push (build + push a ACR con tags latest y SHA)
Secrets necesarios en GitHub

Repo → Settings → Secrets and variables → Actions:

ACR_LOGIN_SERVER = acrentregable5aatxe7.azurecr.io
ACR_USERNAME = acrentregable5aatxe7
ACR_PASSWORD = (password del ACR)

Nota: En tenant académico (UNIR/Azure for Students) puede no haber permisos para crear Service Principal en Azure AD, por lo que el despliegue automático con azure/login puede no ser viable.
En este proyecto se automatiza CI completo (tests + build + push) y el despliegue se actualiza manualmente con az containerapp update (documentado y evidenciado).

7) Monitorización (logs)
az containerapp logs show --name ca-entregable5-backend --resource-group rg-entregable5
8) Evidencias

Carpeta: evidencias/
















9) Entrega
Repositorio: https://github.com/Aatxe7/Entregable5
Evidencias: incluidas en evidencias/



