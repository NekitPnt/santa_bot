from peewee import *

import playhouse.migrate
from loguru import logger

from santa_vk_bot.config import settings

# -------------------------------------------- DB INIT --------------------------------------------
database = PostgresqlDatabase(
    settings.postgres_db,
    user=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.postgres_host,
)


# -------------------------------------------- MODELS --------------------------------------------
class BaseModel(Model):
    class Meta:
        database = database


class Rooms(BaseModel):
    id = PrimaryKeyField(null=False)
    shuffled = BooleanField(default=False)


class Users(BaseModel):
    id = PrimaryKeyField(null=False)
    user_social_id = CharField(max_length=30)
    room_id = IntegerField(null=True)
    getter_id = IntegerField(null=True)
    is_admin = BooleanField(default=False)
    message_allow = BooleanField(default=True)
    state = TextField(null=True)
    group_sub = BooleanField(default=False)
    wish_list = TextField(null=True)


ALL_TABLES = [Users, Rooms]
# -------------------------------------------- MIGRATIONS --------------------------------------------


def dev_drop_tables(db: PostgresqlDatabase, tables: list):
    with db:
        db.drop_tables(tables, safe=True)
    logger.info("Tables dropped")


def create_tables(db: PostgresqlDatabase, tables: list):
    with db:
        db.create_tables(tables, safe=True)
    logger.info("Tables created")


def make_migrations():
    migrator = playhouse.migrate.PostgresqlMigrator(database)
    try:
        with database.atomic():
            playhouse.migrate.migrate(
                # migrator.add_column('users', 'getter_id', IntegerField(null=True)),
                # migrator.add_column('users', 'state', TextField(null=True)),
            )
        logger.info("Tables migrated")
    except ProgrammingError:
        pass


# psql postgresql://santa_bot:santa_bot@localhost:54345/santa_bot
# dev_drop_tables(database, ALL_TABLES)
create_tables(database, ALL_TABLES)
make_migrations()
