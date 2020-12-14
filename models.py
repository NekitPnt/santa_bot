from peewee import *
import settings
import playhouse.migrate

database = SqliteDatabase(settings.DATABASE)
migrator = playhouse.migrate.PostgresqlMigrator(database)


class BaseModel(Model):
    class Meta:
        database = database


class Rooms(BaseModel):
    id = PrimaryKeyField(null=False)
    shuffled = BooleanField(default=False)

    class Meta:
        db_table = "rooms"


class Users(BaseModel):
    id = PrimaryKeyField(null=False)
    user_social_id = CharField(max_length=30)
    social = CharField(max_length=30)
    room_id = IntegerField(null=True)
    is_admin = BooleanField(default=False)
    message_allow = BooleanField(default=True)
    group_sub = BooleanField(default=False)
    wish_list = TextField(null=True)

    class Meta:
        db_table = "users"


with database:
    database.create_tables([Rooms, Users])
with database.atomic():
    playhouse.migrate.migrate(
        migrator.add_column('users', 'wish_list', TextField(null=True)),
    )
