# FundIt 🌱

Plataforma web de crowdfunding desarrollada con Django y TailwindCSS, donde personas pueden apoyar económicamente campañas organizadas por categorías como tecnología, educación, salud y más.

Proyecto final del **Diplomado Python Full Stack**.

---

## Características principales

- Registro e inicio de sesión de usuarios
- Listado y filtrado de campañas por categoría
- Detalle de campaña con barra de progreso de recaudación
- Sistema de donaciones con comentario opcional
- Historial personal de donaciones
- Panel de administración para gestión de campañas y categorías

---

## Requisitos previos

- Python 3.10 o superior
- PostgreSQL
- Git

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/kevsamuel072-wq/fundit.git
cd fundit
```

### 2. Crear y activar el entorno virtual

```bash
# Crear
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Mac/Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y completa con tus datos:

```bash
cp .env.example .env
```

Edita el archivo `.env`:

```
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=fundit_db
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Crear la base de datos en PostgreSQL

```bash
psql -U postgres -c "CREATE DATABASE fundit_db;"
```

### 6. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Traducir permisos al español

```bash
python manage.py traducir_permisos
```

### 8. Crear superusuario (administrador)

```bash
python manage.py createsuperuser
```

---

## Ejecutar el proyecto

```bash
python manage.py runserver
```

Abre tu navegador en:

```
http://127.0.0.1:8000/
```

Panel de administración:

```
http://127.0.0.1:8000/admin/
```

---

## Estructura del proyecto

```
crowdfunding/
├── campaigns/          # App principal: campañas, categorías y donaciones
├── accounts/           # App de autenticación: registro y login
├── templates/          # Plantillas HTML
├── static/             # Archivos estáticos
├── media/              # Imágenes subidas por usuarios
├── manage.py
├── requirements.txt
└── .env.example
```

---

## Tecnologías utilizadas

- **Backend:** Python 3 + Django 4.2
- **Base de datos:** PostgreSQL
- **Frontend:** TailwindCSS
- **Autenticación:** Django Auth

---

## Autor

Desarrollado por Samuel Bazantes y Verónica Cargua
Proyecto Django