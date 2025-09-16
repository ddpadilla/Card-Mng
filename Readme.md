# Card Manager
API para gestionar el registro, consulta y actualización de tarjetas de parqueo asignadas a proveedores de y empleados de una organizacion.

## (El Problema)
Este proyecto nace de una experiencia real en uno de mis trabajos anteriores en una de mis responsabilidades era la gestion de tarjetas de parqueo, cada tarjeta conllevaba una firma autorizadora en fisico y se archivaba, lo que generaba demoras significativas cuando se buscaba el documento fisico adicional riesgo de pérdida de información. Card Manager es la solución que diseñé y construí para digitalizar este flujo, centralizando la información al alcance de un click de los documentos, asegurando la integridad de los datos con transacciones ACID y proveyendo acceso instantáneo a los registros de aprobación.

## Características Principales
- **Integridad de Datos Garantizada**: Operaciones atómicas con transacciones ACID que previenen datos corruptos o inconsistentes (o todo se guarda, o no se guarda nada).
- **Base de Datos Eficiente**: Diseño normalizado (3FN) que evita la redundancia y asegura la consistencia de los datos.
- **API Estándar y Escalable**: Una API RESTful que sigue las mejores prácticas de la industria para una fácil integración.
- **Gestión Segura de Archivos**: Subida y almacenamiento seguro de documentos PDF para un registro de auditoría completo.
- **Interfaz Web Interactiva**: Un cliente ligero y funcional construido con Vanilla JS para la gestión de datos.
- **Arquitectura de Producción Real**: Despliegue profesional del backend en un servidor Linux (DigitalOcean) y frontend en Vercel.


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

1. **Uso dependencias**
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

### Frontend

Para el frontend (ubicado en `Frontend/front-card/`):

```bash
# Navegar al directorio del frontend
cd Frontend/front-card

```

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
- **🌐 Producción**: `https://servertest1.me/api/`
- **💻 Desarrollo**: `http://localhost:8000/api/`

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
POST https://servertest1.me/api/register/

# Consultas
GET https://servertest1.me/api/user/1234567890123/
GET https://servertest1.me/api/card/123456/

# Actualizaciones
PUT https://servertest1.me/api/update/user/1234567890123/
PUT https://servertest1.me/api/update/card/123456/
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

