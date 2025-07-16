import os
import sys
from logging.config import fileConfig

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy.pool import NullPool

from exerciseAPI.core.config import settings
from exerciseAPI.core.database import Base
from exerciseAPI.models import Course, Exercise, Lesson, Option, Topic

config = context.config

# Establece la URL de la base de datos una sola vez
config.set_main_option("sqlalchemy.url", settings.SYNC_DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Usa la Base que ya tiene los modelos registrados
target_metadata = Base.metadata

async_db_url = settings.DATABASE_URL

sync_db_url = async_db_url.replace("postgresql+asyncpg", "postgresql")

config.set_main_option("sqlalchemy.url", sync_db_url)


def run_migrations_offline() -> None:
    # ... (el resto del archivo no cambia)
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # ... (el resto del archivo no cambia)
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
