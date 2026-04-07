# 📁 Auto File Organizer

Organizador automático de archivos con Python y Docker. Vigila tu carpeta de Descargas y mueve archivos según su extensión a subcarpetas organizadas.

## 🚀 Características

- Automatización: mueve archivos automáticamente.
- Configuración mediante JSON.
- Seguridad: evita path traversal y verifica permisos.
- Manejo de colisiones (renombra duplicados).
- Logs rotativos.
- Dockerizado: fácil de ejecutar en cualquier sistema.

## 🐳 Ejecutar con Docker

```bash
docker build -t auto-organizer .
docker run --rm -v C:\Users\TU_USUARIO\Downloads:/data/downloads -v C:\Users\TU_USUARIO\Organized:/data/organized auto-organizer python -m src.organizer --once