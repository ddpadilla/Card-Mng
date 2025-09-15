# Card Manager
API para gestionar el registro, consulta y actualización de tarjetas de parqueo asignadas a proveedores de y empleados de una organizacion.

## Características Principales
- **Transactions ACID**: Todas las operaciones de registro y actualización utilizan transacciones atómicas
- **Modelos normalizados**: Modelos de datos normalizados en su tercera forma normal 3FN para la base de datos.
- **Arquitectura RESTful**: API diseñada siguiendo principios REST
- **Gestión de archivos**: Subida y almacenamiento seguro de documentos PDF
- **Interfaz web interactiva**: Frontend funcional para gestión de datos

## Tecnologías

### Backend
- **Python 3.13**: Lenguaje principal
- **Django 5.2.6**: Framework web
- **Django REST Framework 3.15.0**: Framework para APIs RESTful
- **SQLite**: Base de datos 
- **django-cors-headers 4.8.0**: Manejo de CORS
- **python-decouple 3.8**: Gestión de variables de entorno

### Frontend
- **Vanilla JavaScript (ES6+)**: Sin frameworks adicionales
- **HTML5**: Estructura semántica
- **CSS3**: Estilos responsivos
- **Vite**: Bundler y servidor de desarrollo


## ⚙️ Configuración e Instalación

### Requisitos Previos
- Python 3.13+
- pip (gestor de paquetes de Python)

### Instalación Rápida

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd Proyecto\ Card
```

2. **Configurar entorno virtual**
```bash
cd Backend
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install django djangorestframework django-cors-headers python-decouple
```

4. **Configurar variables de entorno**
Crear archivo `.env` en la carpeta Backend:
```
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Ejecutar migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000/`

### Comandos Esenciales

```bash
# Activar entorno virtual
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Ejecutar servidor
python manage.py runserver

# Crear/aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Acceder al shell de Django
python manage.py shell

```

### Frontend

Para el frontend (ubicado en `Frontend/front-card/`):

```bash
# Navegar al directorio del frontend
cd Frontend/front-card

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: `http://localhost:5173/`

### Estructura del Proyecto
```
Proyecto Card/
├── Backend/
│   ├── maincard/             # Configuración principal de Django
│   │   ├── settings.py       # Configuraciones del proyecto
│   │   ├── urls.py          # URLs principales
│   │   ├── wsgi.py          # Configuración WSGI
│   │   └── asgi.py          # Configuración ASGI
│   ├── apiCard/             # Aplicación principal de la API
│   │   ├── models.py        # Modelos de datos
│   │   ├── serializers.py   # Serializers para la API
│   │   ├── views.py         # Vistas de la API
│   │   ├── urls.py          # URLs de la aplicación
│   │   └── admin.py         # Configuración del admin
│   ├── media/               # Archivos subidos (documentos PDF)
│   ├── manage.py            # Script de gestión de Django
│   ├── db.sqlite3           # Base de datos SQLite
│   ├── .env                 # Variables de entorno
│   └── venv/                # Entorno virtual
├── Frontend/
│   └── front-card/          # Aplicación frontend con Vite
│       ├── src/
│       │   ├── main.js      # JavaScript principal
│       │   └── style.css    # Estilos CSS
│       ├── index.html       # Página principal
│       └── package.json     # Dependencias de Node.js
└── README.md                # Este archivo
```


## 📊 Modelos de Datos
Las entidades de la base de datos se encuentran normalizadas en su tercera forma normal 3FN

### 👤 Usuario (User)
```python
- id_user (PK)                # Número de identidad (mínimo 13 dígitos)
- full_name                   # Nombre completo del usuario
- slug                        # Slug generado automáticamente
- created                     # Timestamp de creación
- updated                     # Timestamp de última actualización
```

### 🎫 Tarjeta de Parqueo (ParkingCard)
```python
- card_number (PK)            # Formato: Numérico de 6 a 8 dígitos
- id_user (FK)                # Relación 1:1 con Usuario
- slug                        # Slug generado automáticamente
- state                       # Enum: 'active', 'inactive', 'expired'
- created                     # Timestamp de creación
- updated                     # Timestamp de última actualización
```

**Reglas de Negocio:**
- Cada usuario tiene una sola tarjeta
- Cada tarjeta pertenece a un solo usuario
- Estados permitidos: activa, inactiva, expirada

### 🚗 Vehículo (Vehicle)
```python
- car_plate (PK)              # Placa del vehículo (6-8 caracteres)
- card_number (FK)            # Relación N:1 con ParkingCard
- brand                       # Marca del vehículo
- created                     # Timestamp de creación
- updated                     # Timestamp de última actualización
```

**Reglas de Negocio:**
- Una tarjeta puede tener varios vehículos asociados
- Cada vehículo pertenece a una sola tarjeta

### 📄 Documento (Document)
```python
- id_document (PK)            # UUID generado automáticamente
- card_number (FK)            # Relación N:1 con ParkingCard
- authorization_document      # Archivo PDF
- created                     # Timestamp de creación
- updated                     # Timestamp de última actualización
```

**Reglas de Negocio:**
- Una tarjeta puede tener varios documentos asociados
- Cada documento pertenece a una sola tarjeta
- Solo se permiten archivos PDF
- Validación de extensión de archivo implementada



## 🚀 API Endpoints

### Base URL
`http://localhost:8000/api/`

### Características de la API
- **Transacciones ACID**: Todas las operaciones de registro y actualización utilizan `@transaction.atomic`
- **Validaciones robustas**: Validación de unicidad y integridad de datos
- **Respuesta unificada**: Estructura de respuesta consistente y plana
- **Gestión de archivos**: Subida segura de documentos PDF

### Endpoints Disponibles

#### 📝 Registro

**Registrar nueva tarjeta completa**
- `POST /api/register/`

**Datos requeridos (FormData para soporte de archivos):**
```json
{
  "id_user": "1234567890123",
  "full_name": "Juan Pérez López",
  "card_number": "123456",
  "state": "active",
  "car_plate": "ABC123",
  "brand": "Toyota",
  "authorization_document": "[archivo PDF]"
}
```

#### 📋 Consultas (Solo Lectura)

**Consulta por ID de Usuario**
- `GET /api/user/{id_user}/`

**Consulta por Número de Tarjeta**
- `GET /api/card/{card_number}/`

**Respuesta unificada (estructura plana):**
```json
{
  "id_user": "1234567890123",
  "full_name": "Juan Pérez López",
  "card_number": "123456",
  "state": "active",
  "car_plate": "ABC123",
  "brand": "Toyota",
  "authorization_document": "/media/documentos/archivo.pdf",
  "created": "2024-01-15T10:30:00Z",
  "updated": "2024-01-15T10:30:00Z"
}
```

#### ✏️ Actualización de Registros

**Actualizar por ID de Usuario**
- `PUT /api/update/user/{id_user}/`
- `PATCH /api/update/user/{id_user}/`

**Actualizar por Número de Tarjeta**
- `PUT /api/update/card/{card_number}/`
- `PATCH /api/update/card/{card_number}/`

**Datos que se pueden actualizar:**
```json
{
  "full_name": "Nuevo nombre",
  "state": "inactive",
  "car_plate": "XYZ789",
  "brand": "Honda"
}
```

### Ejemplos de URLs

```bash
# Registro
POST http://localhost:8000/api/register/

# Consultas
GET http://localhost:8000/api/user/1234567890123/
GET http://localhost:8000/api/card/123456/

# Actualizaciones
PUT http://localhost:8000/api/update/user/1234567890123/
PUT http://localhost:8000/api/update/card/123456/
```

### Códigos de Respuesta

- `200 OK`: Consulta exitosa
- `201 Created`: Registro creado exitosamente
- `404 Not Found`: Usuario o tarjeta no encontrada
- `400 Bad Request`: Datos inválidos o faltantes
- `500 Internal Server Error`: Error del servidor

## 🔒 Transacciones ACID

### Implementación en Serializers

El proyecto implementa transacciones ACID utilizando el decorador `@transaction.atomic` de Django en los serializers:

#### RegistrationSerializer
```python
@transaction.atomic
def create(self, validated_data):
    """
    Método para crear todos los objetos relacionados en una sola transacción ACID.
    """
    # Creación atómica de User, ParkingCard, Vehicle y Document
```

#### UnifiedUpdateSerializer
```python
@transaction.atomic
def update(self, instance, validated_data):
    """
    Actualización atómica de múltiples modelos relacionados.
    """
    # Actualización atómica de campos en User, ParkingCard y Vehicle
```

### Beneficios de las Transacciones ACID
- **Atomicidad**: Todas las operaciones se completan o ninguna se ejecuta
- **Consistencia**: Los datos mantienen su integridad referencial
- **Aislamiento**: Las transacciones concurrentes no se interfieren
- **Durabilidad**: Los cambios confirmados persisten en la base de datos

## ✅ Validaciones Implementadas

### Usuarios
- ID de usuario debe tener al menos 13 dígitos
- Nombre completo es obligatorio
- Validación de unicidad para evitar duplicados

### Tarjetas
- Número debe tener entre 6 y 8 dígitos
- Estados válidos: 'active', 'inactive', 'expired'
- Validación de unicidad del número de tarjeta

### Vehículos
- Placa debe tener entre 6 y 8 caracteres
- Marca es obligatoria
- Validación de unicidad de placa (excluyendo actualización del mismo vehículo)

### Documentos
- Solo archivos PDF permitidos
- Validación de extensión de archivo
- Almacenamiento seguro en directorio `media/documentos/`

