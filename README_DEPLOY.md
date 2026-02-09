# Guía de Despliegue en Render

Tu proyecto ya está configurado con `render.yaml` y `build.sh`. Sigue estos pasos para desplegar:

## 1. Pasos en el Panel de Render

1.  **Nuevo Servicio**: En tu dashboard de Render, crea un nuevo **Web Service** conectado a tu repositorio de GitHub.
2.  **Configuración Automática**: Render detectará el archivo `render.yaml`. Esto creará automáticamente:
    -   El servicio web (Django/Gunicorn).
    -   Una base de datos **PostgreSQL**.
    -   La conexión entre ambos (`DATABASE_URL`).

## 2. Variables de Entorno (Environment)

Debes configurar las siguientes variables en el panel de Render (Environment Groups o directamente en el servicio):

| Variable | Valor Sugerido |
| :--- | :--- |
| `DEBUG` | `False` |
| `SECRET_KEY` | Una cadena larga y aleatoria |
| `ALLOWED_HOSTS` | `*.onrender.com` (o tu dominio) |
| `EMAIL_HOST_USER` | Tu correo de Gmail |
| `EMAIL_HOST_PASSWORD` | Tu contraseña de aplicación de Gmail |
| `CELERY_BROKER_URL` | La URL de tu instancia de Redis en Render |

## 3. Archivos Estáticos y Tailwind

-   **WhiteNoise**: El proyecto ya usa `whitenoise`. Durante el despliegue (`build.sh`), se ejecuta `collectstatic` automáticamente. Los archivos se servirán de forma eficiente.
-   **Tailwind CDN**: Al usar `<script src="https://cdn.tailwindcss.com"></script>`, NO necesitas configurar nada en Django ni en el servidor. El navegador del usuario descarga la librería y procesa el CSS en tiempo real. **Funcionará perfectamente en el deploy.**

## 4. Base de Datos PostgreSQL

-   El archivo `settings.py` usa `dj_database_url`.
-   En Render, la variable `DATABASE_URL` se inyecta automáticamente.
-   Django detectará que es PostgreSQL y usará el driver `psycopg2-binary` (que ya está en `requirements.txt`).

## 5. Celery y Redis

Asegúrate de tener un servicio de **Redis** creado en Render y que la URL esté en la variable `CELERY_BROKER_URL`.
