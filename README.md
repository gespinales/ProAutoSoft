# ProAutoSoft — Sistema de Gestión de Repuestos Vehiculares

Sistema web para administrar ventas, productos, clientes, vendedores, cuentas por cobrar y envíos de **PROAUTO J&D / EIKO S.A.**, reemplazando el sistema basado en hojas de Excel.

## Requisitos

- Python 3.13+
- pip

## Instalación

```bash
# Clonar el repositorio
git clone <repo-url>
cd ProAutoSoft

# Crear y activar entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Cargar datos iniciales (opcional)
python manage.py loaddata datos_iniciales.json

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor de desarrollo
python manage.py runserver 8080
```

## Desarrollo

```bash
# Activar entorno virtual
venv\Scripts\activate
.\venv\Scripts\python manage.py runserver 8080

# Iniciar servidor
python manage.py runserver 8080

# Abrir en el navegador
# http://localhost:8080/admin/
```

### Credenciales por defecto

- **Usuario:** `admin` (superusuario)
- **Contraseña:** `admin123`

> ⚠️ Cambiar en producción.

### Crear usuarios staff (acceso al admin)

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
u = User.objects.create_user(username='nombre', password='clave')
u.is_staff = True  # necesario para acceder al admin
u.save()
```

O desde el admin: **http://localhost:8080/admin/auth/user/add/**

## Estructura del proyecto

```
ProAutoSoft/
├── config/                  # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── formats/es/          # Formatos de número localizados
├── clientes/                # Gestión de clientes
├── productos/               # Catálogo de productos
├── vendedores/              # Gestión de vendedores
├── ventas/                  # Ventas y detalle de ventas
├── cuentas_cobrar/          # Cuentas por cobrar y abonos
├── envios/                  # Envíos e items de envío
├── static/                  # Archivos estáticos (CSS, JS)
│   └── admin/
│       ├── css/detalle_venta.css
│       └── js/detalle_venta.js
├── templates/               # Templates personalizados
├── manage.py
└── requirements.txt
```

## Apps

| App | Modelos principales |
|-----|-------------------|
| `clientes` | Cliente |
| `productos` | Producto |
| `vendedores` | Vendedor |
| `ventas` | Venta, DetalleVenta |
| `cuentas_cobrar` | CuentaCobrar, Abono |
| `envios` | Envio, ItemEnvio |

## Funcionalidades

- **Admin de Django** personalizado con autocomplete, inlines y readonly fields
- **Detalle de venta en línea** con auto-poblado de precios desde el catálogo
- **Cálculo de totales** en tiempo real (venta, costo, ganancia, %)
- **Formato de números** con separadores de miles `,` y decimales `.` (Q1,234.56)
- **API REST** para consultar precios de productos
- **Dashboard** con resumen de clientes, ventas del mes, saldo pendiente y productos

## Tecnologías

- Django 6.0
- Python 3.13
- SQLite (desarrollo) / PostgreSQL (producción)
- Django REST Framework

## Migración a PostgreSQL

```python
# En config/settings.py, cambiar:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'proautosoft',
        'USER': 'postgres',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Luego ejecutar `python manage.py migrate`.

## Commit inicial

Antes del primer commit, asegurarse de:

1. Crear archivo `.gitignore` con:
   ```
   venv/
   *.pyc
   __pycache__/
   db.sqlite3
   .DS_Store
   *.xlsx
   ```

2. Generar `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```

3. Commit:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: ProAutoSoft Django project"
   ```
