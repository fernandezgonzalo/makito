from pydantic import BaseModel
from typing import List, Optional


class Log(BaseModel):
    address: str
    data: str
    topics: List[str]
    transaction_hash: str


class Block(BaseModel):
    block_number: int
    block_hash: str
    logs: Optional[List[Log]] = None


class Blocks(BaseModel):
    blocks: List[Block]


class Filters(BaseModel):
    fromBlock: int
    toBlock: int
    address: Optional[List[str]]
    topics: Optional[List[str]]