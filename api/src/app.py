from fastapi import FastAPI
from fastapi import Response
from fastapi import status

from models import db
from models import Log as LogModel
from models import Block as BlockModel
from models import clean_database

from schema import Blocks
from schema import Filters


app = FastAPI()


@app.get("/get_block/{block}")
def get_block(block: str, response: Response):
    if block == 'latest':
        block = BlockModel.get_last_block()
    else:
        block_number = int(block, 10)
        block = BlockModel.get_block(block_number)
    if block is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    return block


@app.post("/add_blocks", response_model=Blocks)
def add_blocks(data: Blocks):
    with db.atomic():
        for block in data.blocks:
            b = BlockModel.upsert(block.block_number, block.block_hash)
            if block.logs:
                for log in block.logs:
                    l = LogModel()
                    l.address = log.address
                    l.data = log.data
                    l.topics = ",".join(log.topics)
                    l.transaction_hash = log.transaction_hash
                    l.block = b
                    l.save()

    return data


@app.get("/get_logs")
def get_blocks(filters: Filters):
    logs = LogModel.select().where(
            LogModel.block.number >= filters.fromBlock,
            LogModel.block.number <= filters.toBlock
        ).join(BlockModel).order_by(LogModel.id).execute()

    output_logs = []
    for log in logs:
        l = {
            "block_number": log.block.number,
            "block_hash": log.block.hash,
            "address": log.address,
            "data": log.data,
            "topics": log.topics.split(","),
            "transaction_hash": log.transaction_hash
        }
        output_logs.append(l)

    return output_logs

@app.post("/clean_database")
def clean_makito():
    clean_database()
    return {"message": "success"}

