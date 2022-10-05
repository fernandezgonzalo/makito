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
    block = ForeignKeyField(Block, backref="logs", on_delete='CASCADE')
    address = CharField(index=True, null=True)
    data = TextField(null=True)
    topic0 = TextField(null=False, index=True)
    topic1 = CharField(null=True, index=True)
    topic2 = CharField(null=True, index=True)
    topic3 = CharField(null=True, index=True)
    transaction_hash = CharField(null=True)

    class Meta:
        database = database_proxy

    @property
    def topics(self):
        topics = []
        topics.append(self.topic0)
        if self.topic1:
            topics.append(self.topic1)
        if self.topic2:
            topics.append(self.topic2)
        if self.topic3:
            topics.append(self.topic3)

        return topics

    
def clean_database():
    Block.truncate_table(restart_identity=True, cascade=True)
    Log.truncate_table(restart_identity=True, cascade=True)



MODE = os.environ.get('MODE')
if MODE == "DEBUG":
    db = SqliteDatabase('makito.db')
elif MODE == 'TESTING':
    db = SqliteDatabase(':memory:')
else:
    db = PostgresqlDatabase(os.environ.get("POSTGRES_DATABASE", 'postgres'), user=os.environ.get("POSTGRES_USER", "postgres"), password=os.environ.get("POSTGRES_PASSWORD", "example"), host=os.environ.get("POSTGRES_HOST", "localhost"), port=os.environ.get("POSTGRES_PORT", 5435))

# Configure our proxy to use the db we specified in config.
database_proxy.initialize(db)

db.connect()
db.create_tables([Block, Log])