import logging
from datetime import datetime
from uuid import uuid4

from alembic import config, script
from alembic.autogenerate import compare_metadata
from alembic.config import main
from alembic.migration import MigrationContext
from alembic.runtime import migration
from app.utils.errors import MigrationError
from core.extensions import db
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)


class MigrationSetup:
    def __init__(self, settings, engine: Engine = None) -> None:
        self.settings = settings
        self.engine = engine or self.__setup_engine()
        self.alembic_cfg = config.Config("alembic.ini")
        self.meta_ = MetaData()

    def __setup_engine(self):
        return create_engine(
            f"postgresql://{self.settings.DB_USER}:{self.settings.DB_PASSWORD}@{self.settings.DB_HOST}:{self.settings.DB_PORT}/{self.settings.DB_NAME}"
        )

    def __setup_initial_data(self):
        logger.info("setup initial data STARTING")
        with self.engine.connect() as con:
            tmp = con.execute("SELECT * FROM method;")
            if list(tmp):
                logger.info("initial data EXIST -- skiping")
                return

            data = (
                {"id": uuid4(), "name": "GET", "created": str(datetime.now())},
                {"id": uuid4(), "name": "POST", "created": str(datetime.now())},
                {"id": uuid4(), "name": "PUT", "created": str(datetime.now())},
                {"id": uuid4(), "name": "PATCH", "created": str(datetime.now())},
                {"id": uuid4(), "name": "DELETE", "created": str(datetime.now())},
            )

            statement = text(
                """INSERT INTO method(id,name,created) VALUES(:id,:name,:created)"""
            )

            for line in data:
                con.execute(statement, **line)

        logger.info("setup initial data SUCCESS")

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

            self.__setup_initial_data()
            logger.info("Migration setup SUCCESS")

            return True
        except MigrationError as err:
            logger.error(err, exc_info=True)
