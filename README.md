# Triada Cafetera API

API REST desarrollada con FastAPI para la gestión de usuarios, fincas cafeteras, experiencias y reservas. Este proyecto permite a los usuarios registrarse, gestionar fincas cafeteras, crear experiencias turísticas y realizar reservas.

## 📋 Características

- **Gestión de Usuarios**: Registro, autenticación y gestión de perfiles de usuario
- **Fincas Cafeteras**: CRUD completo para la gestión de fincas cafeteras
- **Experiencias**: Creación y gestión de experiencias turísticas relacionadas con el café
- **Reservas**: Sistema de reservas para fincas y experiencias
- **Autenticación JWT**: Sistema seguro de autenticación con tokens JWT
- **Perfiles de Usuario**: Gestión de perfiles personalizados para cada usuario
- **Documentación Automática**: Documentación interactiva con Swagger/OpenAPI

## 🛠️ Tecnologías Utilizadas

- **FastAPI** 0.116.1 - Framework web moderno y rápido para Python
- **SQLAlchemy** 2.0.43 - ORM para Python
- **Pydantic** 2.10.1 - Validación de datos con tipos de Python
- **PostgreSQL** / **SQLite** - Base de datos (configurable)
- **JWT** - Autenticación basada en tokens
- **Bcrypt** - Encriptación de contraseñas
- **Uvicorn** - Servidor ASGI de alto rendimiento

---

## i. Explicación Detallada de la Estructura de Carpetas y Módulos

El proyecto sigue una arquitectura en capas (Layered Architecture) que separa las responsabilidades en diferentes módulos:

```
proyeto/
├── app/                          # Módulo principal de la aplicación
│   ├── __pycache__/              # Archivos compilados de Python (generados automáticamente)
│   │
│   ├── config.py                 # Configuración centralizada de la aplicación
│   │                             # - Carga variables de entorno desde .env
│   │                             # - Define configuración de Settings usando Pydantic
│   │
│   ├── database.py               # Configuración y conexión a la base de datos
│   │                             # - Define el engine de SQLAlchemy
│   │                             # - Crea SessionLocal para manejo de sesiones
│   │                             # - Función get_db() para inyección de dependencias
│   │                             # - Función create_tables() para inicializar BD
│   │
│   ├── main.py                   # Punto de entrada de la aplicación FastAPI
│   │                             # - Crea la instancia de FastAPI
│   │                             # - Registra todos los routers
│   │                             # - Define eventos de startup/shutdown
│   │                             # - Endpoints raíz y health check
│   │
│   ├── controllers/              # Capa de lógica de negocio (Business Logic Layer)
│   │   ├── __init__.py           # Inicialización del paquete
│   │   ├── authController.py     # Lógica de autenticación y autorización
│   │   │                         #   - Registro de usuarios
│   │   │                         #   - Login y generación de tokens
│   │   │                         #   - Gestión de contraseñas
│   │   │                         #   - Validación de tokens JWT
│   │   │
│   │   ├── bookingController.py  # Lógica de negocio para reservas
│   │   │                         #   - Crear, leer, actualizar, eliminar reservas
│   │   │                         #   - Validaciones de fechas y disponibilidad
│   │   │
│   │   ├── clientController.py   # Lógica de negocio para clientes
│   │   │
│   │   ├── estateController.py   # Lógica de negocio para fincas cafeteras
│   │   │                         #   - CRUD completo de fincas
│   │   │                         #   - Filtros y búsquedas
│   │   │                         #   - Validaciones de negocio
│   │   │
│   │   ├── experienceController.py # Lógica de negocio para experiencias
│   │   │
│   │   ├── profileController.py  # Lógica de negocio para perfiles de usuario
│   │   │
│   │   └── userController.py     # Lógica de negocio para usuarios
│   │                             #   - CRUD de usuarios
│   │                             #   - Validaciones y reglas de negocio
│   │
│   ├── models/                   # Capa de modelo de datos (Data Access Layer)
│   │   ├── __init__.py           # Exporta todos los modelos
│   │   ├── user.py               # Modelo User - Representa usuarios en la BD
│   │   │                         #   - Relación 1:1 con Profile
│   │   │                         #   - Relaciones 1:N con Bookings, Experiences, Estates
│   │   │
│   │   ├── estate.py             # Modelo Estate - Representa fincas cafeteras
│   │   │                         #   - Relación N:1 con User (owner)
│   │   │                         #   - Relación 1:N con Bookings
│   │   │
│   │   ├── booking.py            # Modelo Booking - Representa reservas
│   │   │                         #   - Relación N:1 con User y Estate
│   │   │
│   │   ├── experiences.py        # Modelo Experiences - Experiencias turísticas
│   │   │                         #   - Relación N:1 con User
│   │   │
│   │   ├── profile.py            # Modelo Profile - Perfiles de usuario
│   │   │                         #   - Relación 1:1 con User
│   │   │
│   │   ├── client.py             # Modelo Client - Hereda de User (herencia)
│   │   ├── owner.py              # Modelo Owner - Hereda de User (herencia)
│   │   ├── review.py             # Modelo Review - Reseñas
│   │   └── service.py            # Modelo Service - Servicios ofrecidos
│   │
│   ├── routes/                   # Capa de presentación (Presentation Layer)
│   │   ├── __init__.py           # Inicialización del paquete
│   │   ├── auth.py               # Endpoints de autenticación
│   │   │                         #   - POST /auth/register
│   │   │                         #   - POST /auth/login
│   │   │                         #   - POST /auth/logout
│   │   │                         #   - GET /auth/me
│   │   │                         #   - POST /auth/change-password
│   │   │
│   │   ├── user.py               # Endpoints de usuarios
│   │   │                         #   - GET /users
│   │   │                         #   - POST /users
│   │   │                         #   - GET /users/{id}
│   │   │                         #   - PUT /users/{id}
│   │   │                         #   - DELETE /users/{id}
│   │   │
│   │   ├── estate.py             # Endpoints de fincas
│   │   │                         #   - GET /estates
│   │   │                         #   - POST /estates
│   │   │                         #   - GET /estates/{id}
│   │   │                         #   - PUT /estates/{id}
│   │   │                         #   - DELETE /estates/{id}
│   │   │
│   │   ├── booking.py            # Endpoints de reservas
│   │   ├── experience.py         # Endpoints de experiencias
│   │   └── profile.py            # Endpoints de perfiles
│   │
│   ├── schemas/                  # Capa de validación y serialización
│   │   ├── __init__.py           # Inicialización del paquete
│   │   ├── auth.py               # Esquemas Pydantic para autenticación
│   │   │                         #   - LoginRequest
│   │   │                         #   - RegisterRequest
│   │   │                         #   - Token
│   │   │                         #   - UserProfile
│   │   │
│   │   ├── user.py               # Esquemas Pydantic para usuarios
│   │   │                         #   - UserCreate
│   │   │                         #   - UserUpdate
│   │   │                         #   - UserResponse
│   │   │
│   │   ├── estate.py             # Esquemas Pydantic para fincas
│   │   │                         #   - EstateCreate
│   │   │                         #   - EstateUpdate
│   │   │                         #   - EstateResponse
│   │   │
│   │   ├── booking.py            # Esquemas Pydantic para reservas
│   │   ├── client.py             # Esquemas Pydantic para clientes
│   │   ├── experience.py         # Esquemas Pydantic para experiencias
│   │   └── profile_schema.py     # Esquemas Pydantic para perfiles
│   │
│   └── utils/                    # Utilidades y funciones auxiliares
│       ├── __init__.py           # Inicialización del paquete
│       ├── auth.py               # Funciones de autenticación
│       │                         #   - get_password_hash()
│       │                         #   - verify_password()
│       │                         #   - create_access_token()
│       │                         #   - verify_token()
│       │
│       └── middleware.py         # Middleware y dependencias de FastAPI
│                                 #   - get_current_user_optional()
│                                 #   - get_current_user_required()
│                                 #   - require_roles()
│                                 #   - require_active_user()
│
├── venv/                         # Entorno virtual de Python (NO incluir en git)
│                                 # Contiene todas las dependencias instaladas
│
├── requirements.txt              # Lista de dependencias del proyecto
│                                 # Usado por pip para instalar paquetes
│
├── .env                          # Variables de entorno (NO incluir en git)
│                                 # Contiene configuración sensible
│
├── test.db                       # Base de datos SQLite (si se usa SQLite)
│
└── README.md                     # Este archivo
```

### Flujo de Datos en la Arquitectura

1. **Request** → `routes/` (Recibe la petición HTTP)
2. **Validación** → `schemas/` (Valida los datos con Pydantic)
3. **Lógica de Negocio** → `controllers/` (Procesa la lógica)
4. **Acceso a Datos** → `models/` (Interactúa con la base de datos)
5. **Response** → `routes/` (Retorna la respuesta HTTP)

---

## ii. Instrucciones Completas para Ejecutar el Proyecto en Local

### Paso 1: Verificar Requisitos Previos

Asegúrate de tener instalado:

- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)
- **PostgreSQL** (opcional, también se puede usar SQLite para desarrollo)

Verificar versión de Python:

```bash
python3 --version
```

### Paso 2: Clonar o Navegar al Proyecto

Si el proyecto está en un repositorio Git:

```bash
git clone <url-del-repositorio>
cd proyeto
```

Si ya tienes el proyecto localmente:

```bash
cd /Users/felipelopez/Documents/Universidad/software2/proyeto
```

### Paso 3: Crear y Activar Entorno Virtual

**Crear el entorno virtual:**

```bash
python3 -m venv venv
```

**Activar el entorno virtual:**

En **macOS/Linux**:

```bash
source venv/bin/activate
```

En **Windows**:

```bash
venv\Scripts\activate
```

Verificar que el entorno virtual está activo (deberías ver `(venv)` al inicio de tu prompt):

```bash
which python  # macOS/Linux
where python  # Windows
```

### Paso 4: Instalar Dependencias

Con el entorno virtual activado, instalar todas las dependencias:

```bash
pip install -r requirements.txt
```

Verificar que las dependencias se instalaron correctamente:

```bash
pip list
```

### Paso 5: Configurar Variables de Entorno

Crear el archivo `.env` en la raíz del proyecto (ver sección iv para detalles completos).

### Paso 6: Ejecutar el Servidor

Con el entorno virtual activado:

```bash
uvicorn app.main:app --reload
```

El flag `--reload` permite que el servidor se reinicie automáticamente cuando detecta cambios en el código.

### Paso 7: Verificar que el Servidor Está Corriendo

Abrir en el navegador o usar curl:

```bash
# Verificar endpoint raíz
curl http://localhost:8000/

# Verificar health check
curl http://localhost:8000/health
```

Deberías recibir respuestas JSON indicando que la API está funcionando.

### Paso 8: Acceder a la Documentación

Abrir en el navegador:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## iii. Configuración de Entorno Virtual, Instalación de Dependencias y Uso de requirements.txt

### ¿Qué es un Entorno Virtual?

Un entorno virtual es un entorno Python aislado que permite instalar paquetes específicos para un proyecto sin afectar otros proyectos o el sistema Python global.

### Creación del Entorno Virtual

```bash
# Crear entorno virtual con nombre 'venv'
python3 -m venv venv
```

Esto crea una carpeta `venv/` con:

- Una copia del intérprete de Python
- Un directorio para instalar paquetes (`lib/python3.x/site-packages/`)
- Scripts de activación (`bin/activate` en macOS/Linux)

### Activación del Entorno Virtual

**macOS/Linux:**

```bash
source venv/bin/activate
```

**Windows (PowerShell):**

```bash
venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```bash
venv\Scripts\activate.bat
```

**Desactivar el entorno virtual:**

```bash
deactivate
```

### Archivo requirements.txt

El archivo `requirements.txt` contiene todas las dependencias del proyecto con sus versiones específicas:

```
fastapi==0.116.1
uvicorn==0.35.0
sqlalchemy==2.0.43
pydantic-settings==2.10.1
pydantic[email]==2.10.1
passlib[bcrypt]==1.7.4
python-multipart==0.0.12
python-jose[cryptography]==3.3.0
email-validator==2.1.0
jwt==1.4.0
dotenv==0.9.9
pathlib==1.0.1
psycopg2-binary==2.9.11
bcrypt==5.0.0
```

### Instalación de Dependencias desde requirements.txt

```bash
# Asegúrate de tener el entorno virtual activado
pip install -r requirements.txt
```

Esto instalará todas las dependencias listadas con las versiones exactas especificadas.

### Comandos Útiles Relacionados con Dependencias

**Ver dependencias instaladas:**

```bash
pip list
```

**Verificar dependencias del proyecto:**

```bash
pip freeze
```

**Actualizar requirements.txt con dependencias actuales:**

```bash
pip freeze > requirements.txt
```

**Instalar una nueva dependencia y actualizar requirements.txt:**

```bash
pip install nombre-paquete
pip freeze > requirements.txt
```

**Desinstalar una dependencia:**

```bash
pip uninstall nombre-paquete
```

---

## iv. Configuración de la Base de Datos y Variables de Entorno (.env)

### Variables de Entorno

Las variables de entorno permiten configurar la aplicación sin modificar el código, especialmente útil para información sensible como contraseñas y claves secretas.

### Crear el Archivo .env

Crear un archivo llamado `.env` en la raíz del proyecto (mismo nivel que `requirements.txt`):

```bash
touch .env  # macOS/Linux
# O crear manualmente en el editor
```

### Contenido del Archivo .env

```env
# URL de conexión a la base de datos
# Para PostgreSQL:
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/triada_cafetera

# Para SQLite (desarrollo):
# DATABASE_URL=sqlite:///./test.db

# Clave secreta para firmar tokens JWT
# IMPORTANTE: Genera una clave segura y única
# Puedes generar una con: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=tu_clave_secreta_muy_segura_aqui_minimo_32_caracteres

# Algoritmo de encriptación para JWT
ALGORITHM=HS256
```

### Configuración de PostgreSQL

**1. Instalar PostgreSQL:**

```bash
# macOS (con Homebrew)
brew install postgresql
brew services start postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**2. Crear la base de datos:**

```bash
# Acceder a PostgreSQL
psql postgres

# Crear base de datos
CREATE DATABASE triada_cafetera;

# Crear usuario (opcional)
CREATE USER mi_usuario WITH PASSWORD 'mi_contraseña';
GRANT ALL PRIVILEGES ON DATABASE triada_cafetera TO mi_usuario;

# Salir
\q
```

**3. Configurar DATABASE_URL:**

```env
DATABASE_URL=postgresql://mi_usuario:mi_contraseña@localhost:5432/triada_cafetera
```

### Configuración de SQLite (Desarrollo)

Para desarrollo rápido, puedes usar SQLite:

```env
DATABASE_URL=sqlite:///./test.db
```

SQLite no requiere instalación adicional y crea un archivo `test.db` en la raíz del proyecto.

### Carga de Variables de Entorno

El proyecto carga las variables de entorno automáticamente usando `python-dotenv` y `pydantic-settings`:

**En `app/config.py`:**

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
```

**En `app/database.py`:**

```python
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
```

### Inicialización de la Base de Datos

Las tablas se crean automáticamente al iniciar la aplicación mediante:

```python
# En app/main.py
@app.on_event("startup")
def startup_event():
    create_tables()  # Crea todas las tablas definidas en models/
```

### Verificación de la Configuración

**Verificar que las variables se cargan correctamente:**

```python
from app.config import settings
print(settings.DATABASE_URL)  # No debería mostrar None
print(settings.SECRET_KEY)    # No debería mostrar None
```

**Verificar conexión a la base de datos:**

```bash
# Para PostgreSQL
psql -U mi_usuario -d triada_cafetera

# Ver tablas creadas
\dt
```

### Seguridad del Archivo .env

**IMPORTANTE:**

- **NUNCA** subas el archivo `.env` a Git
- Agrega `.env` al archivo `.gitignore`
- Usa diferentes valores de `SECRET_KEY` en desarrollo y producción
- No compartas el archivo `.env` públicamente

**Ejemplo de .gitignore:**

```
.env
venv/
__pycache__/
*.pyc
*.db
test.db
```

---

## v. Enlace o Ruta para Acceder a la Documentación de la API

FastAPI genera automáticamente documentación interactiva de la API usando OpenAPI (Swagger) y ReDoc.

### Documentación Interactiva (Swagger UI)

**URL:** http://localhost:8000/docs

**Características:**

- Interfaz interactiva para probar endpoints
- Documentación completa de todos los endpoints
- Esquemas de request/response
- Posibilidad de autenticarse y hacer peticiones reales
- Validación de datos en tiempo real

**Uso:**

1. Abrir http://localhost:8000/docs en el navegador
2. Explorar los endpoints organizados por tags
3. Expandir un endpoint para ver detalles
4. Hacer clic en "Try it out" para probar el endpoint
5. Ingresar datos y hacer clic en "Execute"
6. Ver la respuesta y el código de estado

### Documentación Alternativa (ReDoc)

**URL:** http://localhost:8000/redoc

**Características:**

- Interfaz más limpia y legible
- Mejor para lectura de documentación
- No permite probar endpoints directamente
- Ideal para compartir con desarrolladores

### Esquema OpenAPI JSON

**URL:** http://localhost:8000/openapi.json

Este endpoint retorna el esquema OpenAPI completo en formato JSON, útil para:

- Integración con herramientas externas
- Generación de clientes SDK
- Importación en Postman o Insomnia

### Endpoints de Información

**Endpoint raíz:**

- **URL:** http://localhost:8000/
- **Método:** GET
- **Descripción:** Información básica de la API y enlaces a documentación

**Health Check:**

- **URL:** http://localhost:8000/health
- **Método:** GET
- **Descripción:** Verifica el estado de la API

**Estado de Autenticación:**

- **URL:** http://localhost:8000/auth/status
- **Método:** GET
- **Descripción:** Información sobre el servicio de autenticación

### Notas sobre la Documentación

- La documentación se genera automáticamente desde los docstrings de las funciones
- Los esquemas Pydantic se convierten automáticamente en esquemas OpenAPI
- Los tags organizan los endpoints en grupos lógicos
- Los ejemplos de request/response se generan automáticamente

---

## vi. Descripción de Cómo se Aplicaron los Principios SOLID dentro del Proyecto

Los principios SOLID son cinco principios de diseño orientado a objetos que hacen que el software sea más mantenible, escalable y fácil de entender. A continuación se describe cómo se aplicaron en este proyecto:

### 1. Single Responsibility Principle (SRP) - Principio de Responsabilidad Única

**Definición:** Cada clase debe tener una sola razón para cambiar, es decir, una sola responsabilidad.

**Aplicación en el Proyecto:**

- **Controladores (`controllers/`)**: Cada controlador tiene una responsabilidad específica:

  - `AuthController`: Solo maneja autenticación y autorización
  - `EstateController`: Solo maneja la lógica de negocio de fincas
  - `BookingController`: Solo maneja la lógica de reservas
  - `UserController`: Solo maneja la lógica de usuarios

- **Modelos (`models/`)**: Solo representan la estructura de datos:

  - `User`: Solo define la estructura de la tabla de usuarios
  - `Estate`: Solo define la estructura de la tabla de fincas
  - No contienen lógica de negocio

- **Rutas (`routes/`)**: Solo definen los endpoints HTTP:

  - `auth.py`: Solo define rutas de autenticación
  - `estate.py`: Solo define rutas de fincas
  - Delegan la lógica a los controladores

- **Esquemas (`schemas/`)**: Solo validan y serializan datos:

  - `UserCreate`: Solo valida datos de creación de usuario
  - `EstateResponse`: Solo serializa datos de respuesta

- **Utilidades (`utils/`)**: Funciones con responsabilidades específicas:
  - `auth.py`: Solo funciones de autenticación (hash, verificación, tokens)
  - `middleware.py`: Solo middleware de autenticación

**Ejemplo:**

```python
# ❌ Violación de SRP (NO se hace así)
class UserManager:
    def create_user(self): ...
    def send_email(self): ...  # Responsabilidad diferente
    def generate_report(self): ...  # Otra responsabilidad diferente

# ✅ Aplicación correcta de SRP
class UserController:  # Solo lógica de usuarios
    def create_user(self): ...

class EmailService:  # Solo envío de emails
    def send_email(self): ...

class ReportGenerator:  # Solo generación de reportes
    def generate_report(self): ...
```

### 2. Open/Closed Principle (OCP) - Principio Abierto/Cerrado

**Definición:** Las entidades de software deben estar abiertas para extensión pero cerradas para modificación.

**Aplicación en el Proyecto:**

- **Extensión de Controladores**: Se pueden crear nuevos controladores sin modificar los existentes:

  - Agregar `ReviewController` no requiere modificar `EstateController`
  - Agregar `PaymentController` no afecta otros controladores

- **Extensión de Modelos mediante Herencia**:

  ```python
  # Modelo base
  class User(Base):
      # Atributos comunes

  # Extensiones sin modificar User
  class Owner(User):  # Hereda de User
      __mapper_args__ = {'polymorphic_identity': 'owner'}

  class Client(User):  # Hereda de User
      __mapper_args__ = {'polymorphic_identity': 'client'}
  ```

- **Extensión de Rutas**: Se pueden agregar nuevas rutas sin modificar las existentes:

  ```python
  # En main.py, agregar nuevos routers sin modificar los existentes
  app.include_router(new_router)  # Extensión sin modificación
  ```

- **Configuración Extensible**: El sistema de configuración permite agregar nuevas variables sin modificar código:
  ```python
  class Settings(BaseSettings):
      # Se pueden agregar nuevas variables sin modificar código existente
      NEW_FEATURE_ENABLED: bool = False
  ```

**Ejemplo:**

```python
# ✅ Extensión sin modificación
# Agregar nuevo tipo de usuario sin modificar User
class Admin(User):
    __mapper_args__ = {'polymorphic_identity': 'admin'}
```

### 3. Liskov Substitution Principle (LSP) - Principio de Sustitución de Liskov

**Definición:** Los objetos de una superclase deben poder ser reemplazados por objetos de sus subclases sin romper la aplicación.

**Aplicación en el Proyecto:**

- **Herencia de Modelos**: `Owner` y `Client` heredan de `User` y pueden usarse donde se espera un `User`:

  ```python
  class Owner(User):
      __mapper_args__ = {'polymorphic_identity': 'owner'}

  class Client(User):
      __mapper_args__ = {'polymorphic_identity': 'client'}

  # Cualquier función que acepte User también acepta Owner o Client
  def process_user(user: User):
      # Funciona con User, Owner o Client
      pass
  ```

- **Esquemas Pydantic**: Los esquemas de respuesta pueden ser extendidos sin romper la compatibilidad:

  ```python
  class UserResponse(BaseModel):
      id: int
      username: str

  class OwnerResponse(UserResponse):  # Extiende UserResponse
      estates: List[EstateResponse]
      # Puede usarse donde se espera UserResponse
  ```

**Ejemplo:**

```python
# ✅ Aplicación correcta de LSP
def get_user_profile(user: User) -> UserProfile:
    # Funciona con User, Owner, Client
    return UserProfile.from_orm(user)

owner = Owner(...)
client = Client(...)
get_user_profile(owner)  # ✅ Funciona
get_user_profile(client)  # ✅ Funciona
```

### 4. Interface Segregation Principle (ISP) - Principio de Segregación de Interfaces

**Definición:** Los clientes no deben depender de interfaces que no usan. Es mejor tener muchas interfaces específicas que una general.

**Aplicación en el Proyecto:**

- **Esquemas Pydantic Específicos**: Cada operación tiene su esquema específico:

  ```python
  # Esquemas específicos para cada operación
  class UserCreate(BaseModel):      # Solo para crear
      username: str
      email: str
      password: str

  class UserUpdate(BaseModel):      # Solo para actualizar (campos opcionales)
      email: Optional[str] = None
      full_name: Optional[str] = None

  class UserResponse(BaseModel):    # Solo para respuestas
      id: int
      username: str
      email: str
  ```

- **Dependencias Específicas**: Middleware con responsabilidades específicas:

  ```python
  # Dependencia opcional (no requiere autenticación)
  async def get_current_user_optional(...) -> Optional[UserProfile]:
      # Para endpoints que pueden funcionar con o sin usuario
      pass

  # Dependencia requerida (requiere autenticación)
  async def get_current_user_required(...) -> UserProfile:
      # Para endpoints que requieren usuario autenticado
      pass
  ```

- **Controladores Específicos**: Cada controlador expone solo los métodos necesarios:
  ```python
  class EstateController:
      # Solo métodos relacionados con fincas
      def create_estate(self): ...
      def get_estate_by_id(self): ...
      # No tiene métodos de usuarios o reservas
  ```

**Ejemplo:**

```python
# ❌ Violación de ISP
class UserSchema:
    # Mezcla creación, actualización y respuesta
    username: str
    password: str  # No debería estar en respuesta
    id: int        # No debería estar en creación

# ✅ Aplicación correcta de ISP
class UserCreate(BaseModel):    # Solo campos para crear
    username: str
    password: str

class UserResponse(BaseModel):  # Solo campos para respuesta
    id: int
    username: str
```

### 5. Dependency Inversion Principle (DIP) - Principio de Inversión de Dependencias

**Definición:** Los módulos de alto nivel no deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones.

**Aplicación en el Proyecto:**

- **Inyección de Dependencias con FastAPI**: Las rutas dependen de abstracciones (interfaces) en lugar de implementaciones concretas:

  ```python
  # En routes/estate.py
  @router.post("/estates")
  def create_estate(
      estate_data: EstateCreate,           # Abstracción (schema)
      db: Session = Depends(get_db)       # Abstracción (sesión)
  ):
      controller = EstateController(db)   # Dependencia inyectada
      return controller.create_estate(estate_data)
  ```

- **Controladores Dependen de Abstracciones**: Los controladores dependen de `Session` (abstracción de SQLAlchemy) no de implementaciones concretas:

  ```python
  class EstateController:
      def __init__(self, db: Session):  # Depende de abstracción Session
          self.db = db  # No depende de implementación concreta
  ```

- **Configuración mediante Abstracciones**: El sistema usa `BaseSettings` de Pydantic (abstracción) en lugar de leer archivos directamente:

  ```python
  class Settings(BaseSettings):  # Abstracción de configuración
      DATABASE_URL: str
      # No depende de cómo se carga (archivo, variables de entorno, etc.)
  ```

- **Utilidades como Abstracciones**: Las funciones de utilidad (`utils/auth.py`) proporcionan abstracciones:
  ```python
  # Las rutas dependen de la abstracción (función)
  # No de la implementación concreta (bcrypt, jwt, etc.)
  from app.utils.auth import get_password_hash, verify_password
  # Si cambiamos la implementación, las rutas no se afectan
  ```

**Ejemplo:**

```python
# ✅ Aplicación correcta de DIP
# Alto nivel (routes) depende de abstracción (Session)
@router.get("/estates")
def get_estates(db: Session = Depends(get_db)):  # Abstracción
    controller = EstateController(db)
    return controller.get_all_estates()

# Bajo nivel (database) implementa la abstracción
def get_db():  # Implementación concreta
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Resumen de Aplicación de SOLID

| Principio | Aplicación en el Proyecto                                                  | Beneficio                              |
| --------- | -------------------------------------------------------------------------- | -------------------------------------- |
| **SRP**   | Separación clara: controllers, models, routes, schemas, utils              | Código más fácil de mantener y testear |
| **OCP**   | Extensión mediante herencia y nuevos módulos sin modificar existentes      | Fácil agregar nuevas funcionalidades   |
| **LSP**   | Owner y Client pueden sustituir a User                                     | Polimorfismo correcto                  |
| **ISP**   | Esquemas específicos (Create, Update, Response) y dependencias específicas | Interfaces claras y específicas        |
| **DIP**   | Inyección de dependencias con FastAPI, abstracciones en controladores      | Bajo acoplamiento, alta cohesión       |

### Beneficios de Aplicar SOLID

1. **Mantenibilidad**: Código más fácil de entender y modificar
2. **Testabilidad**: Cada componente puede testearse independientemente
3. **Escalabilidad**: Fácil agregar nuevas funcionalidades
4. **Reutilización**: Componentes pueden reutilizarse en diferentes contextos
5. **Bajo Acoplamiento**: Cambios en un módulo no afectan otros
6. **Alta Cohesión**: Cada módulo tiene responsabilidades claras y relacionadas

---

## 📝 Notas Adicionales

- La aplicación crea automáticamente las tablas en la base de datos al iniciar
- Se recomienda usar PostgreSQL en producción
- Para desarrollo, puedes usar SQLite configurando `DATABASE_URL=sqlite:///./test.db`
- El entorno virtual debe estar activado antes de ejecutar comandos
- Nunca subas el archivo `.env` a control de versiones

## 📄 Licencia

Este proyecto es parte de un trabajo académico de la Universidad.

---

**Desarrollado con ❤️ usando FastAPI y principios SOLID**
