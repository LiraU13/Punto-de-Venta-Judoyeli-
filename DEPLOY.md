# Guía de Despliegue Paso a Paso

Sigue estos pasos exactos para subir tu proyecto a GitHub y desplegarlo en Render.

## 1. Preparar el Repositorio (En tu computadora)

Abre la terminal en la carpeta principal de tu proyecto:
`c:\Users\lirau\Documentos\Proyectos2\Proyectos Universidad\SPV-DYB-py v3.4 - 14-08-2023\SPV-DYB-py`

Ejecuta los siguientes comandos uno por uno:

1.  **Inicializar Git:**

    ```bash
    git init
    ```

2.  **Crear archivo .gitignore** (Para no subir archivos innecesarios):

    ```bash
    echo "venv/" > .gitignore
    echo "__pycache__/" >> .gitignore
    echo "*.pyc" >> .gitignore
    echo "spv_dybj.db" >> .gitignore
    ```

    _(Nota: Ignoramos la base de datos local para que Render cree una nueva limpia al iniciar)_

3.  **Agregar tus archivos:**

    ```bash
    git add .
    ```

4.  **Guardar los cambios (Commit):**

    ```bash
    git commit -m "Preparando portfolio demo con SQLite"
    ```

5.  **Renombrar la rama principal a 'main':**
    ```bash
    git branch -M main
    ```

## 2. Subir a GitHub

1.  Ve a [GitHub.com](https://github.com) y crea un **Nuevo Repositorio** (New Repository).

    - Ponle un nombre, ej: `portfolio-judoyeli`.
    - Déjalo en **Público**.
    - **NO** marques ninguna casilla de "Initialize this repository".
    - Dale a **Create repository**.

2.  Copia el comando que aparece que dice `git remote add origin ...` (será algo como `https://github.com/TU_USUARIO/portfolio-judoyeli.git`).

3.  **En tu terminal**, pega ese comando y dale Enter:

    ```bash
    git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
    ```

4.  **Subir el código:**
    ```bash
    git push -u origin main
    ```

## 3. Desplegar en Render

1.  Ve a [Render.com](https://render.com) e inicia sesión con GitHub.
2.  Haz clic en el botón **"New +"** y selecciona **"Web Service"**.
3.  Selecciona **"Build and deploy from a Git repository"**.
4.  Busca tu repositorio `portfolio-judoyeli` y dale a **"Connect"**.
5.  En la configuración:
    - **Name**: `portfolio-judoyeli-demo` (o lo que quieras).
    - **Region**: Frankfurt (o la más cercana).
    - **Branch**: `main`.
    - **Runtime**: **Python 3**.
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `gunicorn --chdir app app:app`
6.  Baja y selecciona el plan **"Free"**.
7.  Dale a **"Create Web Service"**.

## 4. ¡Listo!

Render tardará unos minutos en construir tu sitio. Cuando termine, verás un enlace arriba a la izquierda (ej: `https://portfolio-judoyeli-demo.onrender.com`).

**Credenciales de Acceso (Datos Falsos):**

- **Usuario**: `admin`
- **Contraseña**: `admin`
