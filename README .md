
# EFI Práctica Profesionalizante "Python"

**Desarrolladores:**
- Octavio Victorio :computer:
- Druetta Cristian :computer:

**Profesor:**
- Lucero Matias
---

## Comenzando 🚀

Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas.

### Clonar el proyecto
```bash
git clone git@github.com:Cdruetta/EFI-python.git
```

### Pre-requisitos 📋

Qué necesitas para instalar el software y cómo instalarlo:

1. **Instalar y correr XAMPP**  
   ```bash
   sudo /opt/lampp/lampp start
   ```

2. **Crear una base de datos (DB) en SQL**  
   Abre el navegador y accede a `http://localhost/phpmyadmin/`

3. **Crear el entorno virtual**
   ```bash
   python3 -m venv entorno
   ```

4. **Activar el entorno virtual**
   ```bash
   source env/bin/activate
   ```

5. **Instalar los requisitos**
   ```bash
   pip install -r requirements.txt
   ```

6. **Correr el proyecto**
   ```bash
   flask run --reload
   ```

---

## Endpoints API 📋
- A continuación se describen los endpoints de la API para interactuar con la aplicación.

# Autenticación y Registro

- **Iniciar sesión**
   - Método: POST
   - Endpoint: /login
- **Descripción:**
   - Permite al usuario iniciar sesión verificando las credenciales proporcionadas. Si las credenciales son correctas, establece la sesión con un token JWT.

**Ejemplo de cuerpo de solicitud:**
{
    "usuario": "admin",
    "contrasenia": "admin"
}

**Ejemplo de respuesta:**
{
    "Token": "Bearer <token>"
}

## Registro de usuario
   - Método: POST
   - Endpoint: /users
- **Descripción:**
   - Registra un nuevo usuario con un nombre de usuario y una contraseña hasheada. Solo un administrador puede crear nuevos usuarios.

**Ejemplo de cuerpo de solicitud:**

{
    "usuario": "octavio",
    "contrasenia": "12345678"
}

**Gestión de Usuarios**

## Mostrar Usuarios
   - Método: GET
   - Endpoint: /users
**Descripción:**
   - Lista todos los usuarios registrados. Solo accesible para administradores.

**Ejemplo de respuesta:**

[
    {
        "id": 1,
        "usuario": "admin",
        "activo": true,
        "is_admin": true
    },
    {
        "id": 2,
        "usuario": "octavio",
        "activo": true,
        "is_admin": false
    }
]
## Actualizar Usuario
   - Método: PUT
   - Endpoint: /user/actualizar
**Descripción:**
   - Permite a un administrador actualizar los detalles de un usuario existente. Solo el administrador puede realizar esta acción.

**Ejemplo de cuerpo de solicitud:**
{
    "id": 1,
    "usuario": "octavio",
    "contrasenia": "newpassword",
    "activo": true
}

##Eliminar Usuario
   - Método: DELETE
   - Endpoint: /user/eliminar
**Descripción:**
   - Permite a un administrador desactivar un usuario.

**Ejemplo de cuerpo de solicitud:**
{
    "id": 2
}

# Gestión de Equipos

## Mostrar Equipos
   - Método: GET
   - Endpoint: /equipos
**Descripción:**
   - Muestra todos los equipos. Los administradores obtienen más detalles, mientras que los usuarios normales reciben información mínima.

**Ejemplo de respuesta:**
[
    {
        "id": 1,
        "nombre": "Equipo A",
        "categoria_id": 2,
        "modelo_id": 1,
        "costo": 100,
        "stock_id": 5,
        "activo": true
    }
]

## Crear Equipo
   - Método: POST
   - Endpoint: /equipos/crear
**Descripción:**
   - Permite a un administrador crear un nuevo equipo.

**Ejemplo de cuerpo de solicitud:**
{
    "nombre": "Equipo X",
    "modelo_id": 1,
    "categoria_id": 2,
    "costo": 200,
    "stock_id": 3,
    "marca_id": 1,
    "activo": 1
}

## Actualizar Equipo
   - Método: PUT
   - Endpoint: /equipos/actualizar
**Descripción:**
   - Permite a un administrador actualizar un equipo existente.

**Ejemplo de cuerpo de solicitud:**
{
    "id": 1,
    "nombre": "Nuevo Equipo",
    "modelo_id": 2,
    "categoria_id": 3,
    "costo": 250,
    "stock_id": 4,
    "marca_id": 2,
    "activo": 0
}

## Eliminar Equipo
   - Método: DELETE
   - Endpoint: /equipos/eliminar
**Descripción:**
   - Permite a un administrador desactivar un equipo.

**Ejemplo de cuerpo de solicitud:**
{
    "id": 2
}

**Autorizar JWT**
   - Para los endpoints que requieren autenticación, asegúrate de enviar el token JWT en el encabezado de la solicitud como sigue:

      - Authorization: Bearer <token>

---
