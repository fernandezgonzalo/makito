import os
from peewee import *


database_proxy = Proxy()


class Block(Model):
    number = BigIntegerField(index=True)
    hash = CharField(index=True)

    class Meta:
        database = database_proxy

    @classmethod
    def get_last_block(cls):
        query = cls.select().order_by(cls.number.desc()).limit(1)
        if query.exists():
            b = query.get()
            block = {
                "block_number": b.number,
                "block_hash": b.hash
            }

            return block
        return None

    @classmethod
    def get_block(cls, number):
        try:

            b = cls.get(cls.number == number)
            block = {
                "block_number": b.number,
                "block_hash": b.hash
            }
            return block
        except cls.DoesNotExist:
            return None

    @classmethod
    def upsert(cls, block_number, block_hash):
        try:
            block = cls.get(cls.number==block_number)
            block.hash = block_hash
            block.save()

            Log.delete().where(Log.block == block).execute()
                
        except cls.DoesNotExist:
            block = cls()
            block.hash = block_hash
            block.number = block_number
            block.save()

        return block

class Log(Model):
    block = ForeignKeyField(Block, backref="logs")
    address = CharField(index=True, null=True)
    data = TextField(null=True)
    topics = TextField(null=True)
    transaction_hash = CharField(null=True)

    class Meta:
        database = database_proxy

    




MODE = os.environ.get('MODE')
if MODE == "DEBUG":
    db = SqliteDatabase('makito.db')
elif MODE == 'TESTING':
    db = SqliteDatabase(':memory:')
else:
    db = PostgresqlDatabase(os.environ.get("POSTGRES_DATABASE", 'postgres'), user=os.environ.get("POSTGRES_USER", "postgres"), password=os.environ.get("POSTGRES_PASSWORD", "example"), host=os.environ.get("POSTGRES_HOST", "localhost"), port=os.environ.get("POSTGRES_HOST", 5435))

# Configure our proxy to use the db we specified in config.
database_proxy.initialize(db)

db.connect()
db.create_tables([Block, Log])