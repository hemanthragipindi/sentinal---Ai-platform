import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Use backend/.env
from dotenv import load_dotenv
load_dotenv(".env")

# Import all models
from app.database.models.base import Base
from app.modules.auth.models import User, RefreshToken, UserSession, ApiKey
from app.modules.chat.models import Conversation, Message, MessageAttachment
from app.modules.memory.models import Memory, MemoryEmbedding, MemoryVersion, RetrievalLog, RetrievedMemory, MemoryProvenance
from app.modules.experiments.models import PromptTemplate, ModelUsageLog
from app.modules.threat_detection.models import Threat, TrustScore, QuarantinedMemory, SecurityEvent, AnomalyResult
from app.modules.storage.models import File, FileAccessLog
from app.modules.reports.models import Report, UsageStatistic
from app.modules.audit.models import AuditLog, SystemLog
from app.modules.settings.models import UserSettings, SystemSetting
from app.modules.jobs.models import Job, JobLog


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Fetch database URL and replace postgresql:// with postgresql+asyncpg:// if necessary
database_url = os.getenv("DATABASE_URL")
if database_url and database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        # pgvector uses its own types that Alembic may not compare perfectly by default
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
