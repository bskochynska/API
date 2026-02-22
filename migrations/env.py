import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config
import sys
from os.path import abspath, dirname
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

sys.path.insert(0, abspath(dirname(dirname(__file__))))

from app.db.base import Base
from app import models

config = getattr(context, "config")

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def do_run_migrations(connection):
    configure_func = getattr(context, "configure")
    run_migrations_func = getattr(context, "run_migrations")

    configure_func(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with getattr(context, "begin_transaction")():
        run_migrations_func()

async def run_async_migrations():
    """Запуск міграцій в асинхронному режимі."""
    configuration = config.get_section(config.config_ini_section, {})

    # Використовуємо async_engine_from_config замість звичайного
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Alembic потребує синхронного контексту для виконання SQL,
        # тому ми використовуємо run_sync
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Запускаємо асинхронний цикл подій
    asyncio.run(run_async_migrations())

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")

    configure_func = getattr(context, "configure")
    run_migrations_func = getattr(context, "run_migrations")
    begin_transaction_func = getattr(context, "begin_transaction")

    configure_func(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with begin_transaction_func():
        run_migrations_func()

is_offline = getattr(context, "is_offline_mode")()

if is_offline:
    run_migrations_offline()
else:
    run_migrations_online()
