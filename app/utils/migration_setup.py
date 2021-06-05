import logging

from alembic import config, script
from alembic.autogenerate import compare_metadata
from alembic.config import main
from alembic.migration import MigrationContext
from alembic.runtime import migration
from app.utils.errors import MigrationError
from core.extensions import db
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


class MigrationSetup:
    def __init__(self, settings, engine: Engine = None) -> None:
        self.settings = settings
        self.engine = engine or self.__setup_engine()
        self.alembic_cfg = config.Config("alembic.ini")

    def __setup_engine(self):
        return create_engine(
            f"postgresql://{self.settings.DB_USER}:{self.settings.DB_PASSWORD}@{self.settings.DB_HOST}:{self.settings.DB_PORT}/{self.settings.DB_NAME}"
        )

    def check_current_head(self):
        logger.info("checking database uptodate")
        directory = script.ScriptDirectory.from_config(self.alembic_cfg)
        with self.engine.begin() as connection:
            context = migration.MigrationContext.configure(connection)
            return set(context.get_current_heads()) == set(directory.get_heads())

    def check_model_changes(self):
        mig_ctx = MigrationContext.configure(self.engine.connect())
        return compare_metadata(mig_ctx, db)

    def upgrade_db(self):
        logger.info("Upgrading database")
        main(["--raiseerr", "upgrade", "head"])

    def generate_migration(self):
        logger.info("Generating new migrations")
        main(["--raiseerr", "revision", "--autogenerate"])

    def process_migration(self):
        logger.info("Start processing migration")
        try:
            if not self.check_current_head():
                self.upgrade_db()
            while self.check_model_changes():
                self.generate_migration()
                self.upgrade_db()
            logger.info("Migration setup SUCCESS")
            return True
        except MigrationError as err:
            logger.error(err, exc_info=True)
