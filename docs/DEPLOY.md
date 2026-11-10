# Manual de Despliegue — SIGR v1.1.0

> Sistema Integral de Gestión de Restaurante
> Guía completa para instalar, configurar y desplegar el sistema.

---

## Índice
1. [Requisitos previos](#1-requisitos-previos)
2. [Instalación local](#2-instalación-local)
3. [Configuración](#3-configuración)
4. [Ejecución](#4-ejecución)
5. [Verificación](#5-verificación)
6. [Despliegue en producción](#6-despliegue-en-producción)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Requisitos previos

| Software | Versión mínima | Verificar |
|---|---|---|
| **Python** | **3.11 o 3.12** ⚠️ | `python3.11 --version` |
| **pip** | 22+ | `pip --version` |
| **Git** | 2.30+ | `git --version` |

> ⚠️ **CRÍTICO:** NO usar Python 3.13+ ni 3.14. SQLAlchemy 2.0 no compila en esas versiones.

### Sistemas operativos soportados
- Linux: Ubuntu 20.04+, Debian 11+, Fedora 36+, Arch
- macOS: 12 Monterey+
- Windows: 10/11 (usar WSL2)

---

## 2. Instalación local

### 2.1 Clonar el repositorio

```bash
git clone https://github.com/fadelga1/trabajo_gestion_software.git
cd trabajo_gestion_software
2.2 Instalar Python 3.11 (Ubuntu/Debian)
bash

sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y

2.3 Crear entorno virtual
bash

python3.11 -m venv venv
source venv/bin/activate     # Linux/macOS
# venv\Scripts\activate      # Windows

Verificar:
bash

which python
# Debe mostrar: .../venv/bin/python

python --version
# Python 3.11.x

2.4 Instalar dependencias
bash

pip install --upgrade pip
pip install -r requirements.txt

Verificar:
bash

pip list | grep -iE 'flask|werkzeug|sqlalchemy'

Salida esperada:
text

Flask               3.0.0
Flask-Login         0.6.3
Flask-SQLAlchemy    3.1.1
SQLAlchemy          2.0.x
Werkzeug            3.0.1

3. Configuración
3.1 Archivo .env
bash

cp .env.example .env

Editar .env con nano o VS Code:
env

SECRET_KEY=<clave-segura-generada>
FLASK_ENV=development
DATABASE_URL=sqlite:///sigr.db

Generar SECRET_KEY segura:
bash

python -c "import secrets; print(secrets.token_urlsafe(32))"

    ⚠️ NUNCA comitear .env a Git. Ya está en .gitignore.

3.2 Base de datos

La BD se crea automáticamente al primer arranque con datos demo (init_db()).

Ubicación: instance/sigr.db
4. Ejecución
4.1 Modo desarrollo
bash

python app.py

Salida esperada:
text

✅ BD inicializada con usuarios y menú demo.
 * Running on http://0.0.0.0:5000
 * Debug mode: on

4.2 Acceder

Abrir navegador en:
text

http://localhost:5000

4.3 Detener

Ctrl + C en la terminal.
4.4 Cambiar puerto

Editar app.py:
python

app.run(debug=True, host='0.0.0.0', port=5001)

5. Verificación
Credenciales demo
Rol	Email	Password
Admin	admin@sigr.com	admin123
Mesero	mesero@sigr.com	mesero123
Cliente	cliente@sigr.com	cliente123
Pruebas rápidas
#	Prueba	Resultado esperado
1	Abrir http://localhost:5000	Pantalla de login
2	Login admin	Nav con Caja, Reportes, Gestionar Menú
3	Login mesero	Nav sin Caja/Reportes
4	Login cliente	Nav solo Menú, Pedidos, Reservas
5	Cliente intenta /caja	403 Forbidden
6	Versión en nav (esquina)	v1.1.0
Comandos de verificación
bash

python -m py_compile app.py && echo "✅ Sintaxis OK"

python -c "import flask, flask_login, flask_sqlalchemy; print('✅ Deps OK')"

sqlite3 instance/sigr.db ".tables"

6. Despliegue en producción
Consideraciones previas

    Cambiar SECRET_KEY por una segura

    Poner debug=False en app.py

    Añadir gunicorn a requirements.txt

    Configurar HTTPS

    Backup de BD

Añadir gunicorn:
bash

echo "gunicorn==21.2.0" >> requirements.txt
pip install gunicorn

Opción A — Render (gratuita)

    Crear cuenta en https://render.com

    New → Web Service → conectar GitHub repo

    Configurar:

        Build Command: pip install -r requirements.txt

        Start Command: gunicorn app:app

    Variables de entorno:

        SECRET_KEY=<clave-segura>

        PYTHON_VERSION=3.11.9

    Deploy

⚠️ SQLite en Render es efímero. Para persistencia usar PostgreSQL.
Opción B — Railway

    Crear cuenta en https://railway.app

    New Project → Deploy from GitHub repo

    Añadir Procfile:
    text

    web: gunicorn app:app

    Variables: SECRET_KEY=<clave>

    Generate Domain

Opción C — Docker

Crear Dockerfile:
dockerfile

FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p instance
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

Crear .dockerignore:
text

venv/
__pycache__/
.git/
instance/
.env
*.db
*.bak

Build y run:
bash

docker build -t sigr:v1.1.0 .
docker run -d -p 8000:8000 --name sigr-app sigr:v1.1.0

Opción D — VPS Ubuntu + Nginx + Gunicorn

    Instalar dependencias:
    bash

    sudo apt install python3.11 python3.11-venv nginx -y

    Clonar en /var/www:
    bash

    cd /var/www
    sudo git clone https://github.com/fadelga1/trabajo_gestion_software.git
    sudo chown -R $USER:$USER trabajo_gestion_software
    cd trabajo_gestion_software
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt gunicorn

    Servicio systemd /etc/systemd/system/sigr.service:
    ini

    [Unit]
    Description=SIGR Gunicorn
    After=network.target

    [Service]
    User=www-data
    WorkingDirectory=/var/www/trabajo_gestion_software
    Environment="PATH=/var/www/trabajo_gestion_software/venv/bin"
    Environment="SECRET_KEY=cambiar-en-produccion"
    ExecStart=/var/www/trabajo_gestion_software/venv/bin/gunicorn --workers 2 --bind unix:/var/www/trabajo_gestion_software/sigr.sock app:app

    [Install]
    WantedBy=multi-user.target

    Activar:
    bash

    sudo systemctl daemon-reload
    sudo systemctl enable sigr
    sudo systemctl start sigr

    Nginx /etc/nginx/sites-available/sigr:
    nginx

    server {
        listen 80;
        server_name tudominio.com;
        location / {
            include proxy_params;
            proxy_pass http://unix:/var/www/trabajo_gestion_software/sigr.sock;
        }
    }

    Activar y HTTPS:
    bash

    sudo ln -s /etc/nginx/sites-available/sigr /etc/nginx/sites-enabled/
    sudo nginx -t && sudo systemctl restart nginx
    sudo apt install certbot python3-certbot-nginx -y
    sudo certbot --nginx -d tudominio.com

7. Troubleshooting
Error	Causa	Solución
ModuleNotFoundError: flask	venv no activado	source venv/bin/activate
error: command 'gcc' failed	Python incompatible	usar 3.11/3.12
Address already in use	Puerto 5000 ocupado	sudo lsof -i :5000 → matar proceso
unable to open database file	Falta instance/	mkdir instance
SECRET_KEY must be set	Falta .env	cp .env.example .env
TemplateNotFound	Falta archivo HTML	verificar templates/
Authentication failed en Git	Token inválido	regenerar PAT en GitHub
SyntaxError: 'return' outside function	Indentación rota	python -m py_compile app.py
Comandos de diagnóstico
bash

sudo lsof -i :5000
curl -I http://localhost:5000/login
ls -la instance/sigr.db
sqlite3 instance/sigr.db "SELECT COUNT(*) FROM usuarios;"

Mantenimiento
Backup manual
bash

cp instance/sigr.db backups/sigr-$(date +%Y%m%d-%H%M).db

Backup automático (cron)
bash

crontab -e
# Añadir:
0 3 * * * cp /ruta/al/proyecto/instance/sigr.db /ruta/al/proyecto/backups/sigr-$(date +\%Y\%m\%d).db

Actualizar
bash

git pull origin main
source venv/bin/activate
pip install -r requirements.txt
# Reiniciar servicio

Última actualización: 10/11/2026
Versión del documento: 1.1
Autor: Equipo SIGR
