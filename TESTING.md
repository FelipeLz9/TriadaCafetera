# Guía de Pruebas para Endpoints de Clientes

## Opción 1: Documentación Interactiva de FastAPI (Recomendado)

FastAPI genera automáticamente una documentación interactiva. Es la forma más fácil de probar los endpoints.

### Pasos:

1. **Iniciar el servidor:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Abrir en el navegador:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Probar los endpoints:**
   - En Swagger UI puedes hacer clic en cada endpoint
   - Hacer clic en "Try it out"
   - Llenar los datos del request
   - Hacer clic en "Execute"
   - Ver la respuesta

## Opción 2: Script de Prueba Automatizado

### Pasos:

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Asegúrate de tener configurada la base de datos:**
   - Crea un archivo `.env` con:
     ```
     DATABASE_URL=tu_url_de_base_de_datos
     SECRET_KEY=tu_secret_key
     ALGORITHM=HS256
     ```

3. **Iniciar el servidor (en una terminal):**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Ejecutar las pruebas (en otra terminal):**
   ```bash
   python test_client_endpoints.py
   ```

## Opción 3: Usando curl (Línea de comandos)

### Crear un cliente:
```bash
curl -X POST "http://localhost:8000/clients/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "email": "test@example.com",
    "full_name": "Usuario de Prueba",
    "phone": "1234567890",
    "password": "testpass123"
  }'
```

### Obtener todos los clientes:
```bash
curl -X GET "http://localhost:8000/clients/"
```

### Obtener un cliente por ID:
```bash
curl -X GET "http://localhost:8000/clients/1"
```

### Actualizar un cliente:
```bash
curl -X PUT "http://localhost:8000/clients/1" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Nombre Actualizado",
    "phone": "9876543210"
  }'
```

### Eliminar un cliente (soft delete):
```bash
curl -X DELETE "http://localhost:8000/clients/1"
```

## Endpoints Disponibles

- `POST /clients/` - Crear un nuevo cliente
- `GET /clients/` - Obtener todos los clientes
- `GET /clients/{client_id}` - Obtener un cliente por ID
- `PUT /clients/{client_id}` - Actualizar un cliente
- `DELETE /clients/{client_id}` - Eliminar un cliente (soft delete)

## Notas Importantes

- El servidor debe estar ejecutándose antes de probar los endpoints
- Asegúrate de que la base de datos esté configurada correctamente
- Los errores de validación se mostrarán en las respuestas HTTP

