#!/bin/bash
# iniciar entrypoint.sh
set -e
cd exerciseAPI

echo "Actualizando base de datos."
alembic upgrade head

echo "Iniciando la aplicación..."
cd ..
exec "$@"