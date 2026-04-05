# E-Clerk

E-Clerk es un sistema escrito en Python usando el framework FastAPI. Está diseñado para APIs rápidas y asíncronas y utiliza PostgreSQL (v16) como base de datos, ejecutada en un contenedor Docker con datos persistidos fuera del contenedor.

## Características principales

- API REST construida con FastAPI
- Conexión a PostgreSQL 16
- Persistencia de datos fuera del contenedor Docker

## Requisitos

- Python 3.11+ (recomendado)
- pip
- Docker y Docker Compose (opcional, para la base de datos)

## Instalación (entorno de desarrollo)

1. Clonar el repositorio y moverse al directorio del proyecto:

   cd /ruta/al/proyecto/eclerk

2. Crear y activar un entorno virtual:

   python -m venv .venv
   source .venv/bin/activate

3. Instalar dependencias (ejemplo de `requirements.txt`):

   pip install --upgrade pip
   pip install fastapi uvicorn[standard] sqlalchemy asyncpg python-dotenv alembic

   (Si prefieres usar sincronía: reemplaza `asyncpg` por `psycopg[binary]` y ajusta el código.)

4. Crear un archivo `.env` en la raíz del proyecto con la configuración de la base de datos. Ejemplo:

   # .env
   DATABASE_URL=postgresql+asyncpg://eclerk_user:strongpassword@localhost:5432/eclerk_db
   SECRET_KEY=changeme

5. Ejecutar la aplicación en desarrollo:

   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   - Asegúrate de que `app.main:app` apunte al módulo correcto de tu proyecto.

## PostgreSQL v16 en Docker (persistencia fuera del contenedor)

Puedes ejecutar PostgreSQL 16 en Docker de manera simple o con Docker Compose. Se muestran ambas opciones y cómo persistir los datos en el host.

### Opción A — docker run (bind mount para persistencia)

1. Crear carpeta para persistencia en el proyecto (ruta relativa):

   mkdir -p ./pg_data
   chmod 700 ./pg_data

2. Levantar el contenedor PostgreSQL 16 vinculando la carpeta local a `/var/lib/postgresql/data`:

   docker run -d \
     --name eclerk-postgres \
     -e POSTGRES_USER=eclerk_user \
     -e POSTGRES_PASSWORD=strongpassword \
     -e POSTGRES_DB=eclerk_db \
     -p 5432:5432 \
     -v $(pwd)/pg_data:/var/lib/postgresql/data \
     postgres:16

Notas:
- La carpeta `./pg_data` en el host contendrá los datos (persistencia fuera del contenedor).
- Asegúrate de usar una ruta absoluta o `$(pwd)/pg_data` según tu shell (zsh/bash).

### Opción B — docker-compose (recomendado para desarrollo)

Crear un archivo `docker-compose.yml` en la raíz del proyecto con el siguiente contenido:

```yaml
version: '3.8'
services:
  db:
    image: postgres:16
    container_name: eclerk-postgres
    environment:
      POSTGRES_USER: eclerk_user
      POSTGRES_PASSWORD: strongpassword
      POSTGRES_DB: eclerk_db
    ports:
      - "5432:5432"
    volumes:
      - ./pg_data:/var/lib/postgresql/data
    restart: unless-stopped
```

Levantar con:

   docker compose up -d

Esto crea (o reutiliza) la carpeta `./pg_data` para la persistencia de la base de datos fuera del contenedor.

### Volúmenes Docker (alternativa)

Si prefieres usar un volumen gestionado por Docker en lugar de un bind mount:

   docker volume create eclerk_pgdata
   docker run -d \
     --name eclerk-postgres \
     -e POSTGRES_USER=eclerk_user \
     -e POSTGRES_PASSWORD=strongpassword \
     -e POSTGRES_DB=eclerk_db \
     -p 5432:5432 \
     -v eclerk_pgdata:/var/lib/postgresql/data \
     postgres:16

Esta opción persiste datos fuera del contenedor (en el host Docker), pero el directorio exacto es manejado por Docker.

## Conexión desde la aplicación

Usa la variable `DATABASE_URL` (ej. en `.env`) para que tu app se conecte a PostgreSQL. Ejemplo de cadena de conexión para asyncpg (SQLAlchemy async):

   postgresql+asyncpg://eclerk_user:strongpassword@localhost:5432/eclerk_db

Si usas `psycopg[binary]` con conexión síncrona:

   postgresql://eclerk_user:strongpassword@localhost:5432/eclerk_db

## Copia de seguridad y restauración

- Hacer dump de la base de datos (host con cliente `pg_dump`):

  pg_dump -h localhost -p 5432 -U eclerk_user -d eclerk_db -F c -f eclerk_db.dump

- Restaurar (con `pg_restore`):

  pg_restore -h localhost -p 5432 -U eclerk_user -d eclerk_db -c eclerk_db.dump

Si prefieres ejecutar los comandos dentro del contenedor:

  docker exec -it eclerk-postgres pg_dump -U eclerk_user -d eclerk_db -F c > eclerk_db.dump

## Buenas prácticas

- Nunca almacenes credenciales en el repositorio: usa variables de entorno o un gestor de secretos.
- Asegura permisos correctos en la carpeta de persistencia (por ejemplo `chmod 700 pg_data`).
- Usa migrations (Alembic) para gestionar esquemas en producción.

## Ejemplo rápido de checklist para levantar el proyecto

1. Crear `.venv` e instalar dependencias.
2. Crear `./pg_data` y levantar PostgreSQL (docker compose up -d).
3. Configurar `.env` con `DATABASE_URL` apuntando a la base de datos.
4. Ejecutar la app: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.

---

Para cualquier ajuste adicional (migraciones, despliegue en producción, Dockerización completa de la app, CI/CD), puedo agregar ejemplos concretos según el stack que uses.