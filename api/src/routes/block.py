from fastapi import APIRouter, Response, status

from .schema import Blocks

from models import db
from models import Block as BlockModel

block_router = APIRouter()


@block_router.get("/get_block/{block}")
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


@block_router.post("/add_blocks", response_model=Blocks)
def add_blocks(data: Blocks):
    with db.atomic():
        for block in data.blocks:
            b = BlockModel.upsert(block.block_number, block.block_hash)
            if block.logs:
                for log in block.logs:
                    l = LogModel()
                    l.address = log.address
                    l.data = log.data
                    
                    for i, topic in enumerate(log.topics):
                        field = "topic{num}".format(num=i)
                        setattr(l, field, topic)

                    l.transaction_hash = log.transaction_hash
                    l.block = b
                    l.save()

    return data