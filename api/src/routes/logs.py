from fastapi import APIRouter

from .schema import Filters

from models import Log as LogModel
from models import Block as BlockModel


logs_router = APIRouter()


@logs_router.get("/get_logs")
def get_blocks(filters: Filters):
    query = LogModel.select()
    
    if filters.address:
        query = query.where(LogModel.address << filters.address)
    if filters.topics:
        query = query.where(LogModel.topic0 << filters.topics)

    query = query.where(
            LogModel.block.number >= filters.fromBlock,
            LogModel.block.number <= filters.toBlock
    )

    query = query.join(BlockModel).order_by(LogModel.id)
    logs = query.execute()

    output_logs = []
    for log in logs:
        l = {
            "block_number": log.block.number,
            "block_hash": log.block.hash,
            "address": log.address,
            "data": log.data,
            "topics": log.topics,
            "transaction_hash": log.transaction_hash
        }
        output_logs.append(l)

    return output_logs