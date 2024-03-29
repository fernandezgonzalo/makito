import os
import requests
from http import HTTPStatus
from hexbytes import HexBytes
from web3.datastructures import AttributeDict


class MakitoClient():
    def __init__(self, host):
        self.host = host

    def normalize_filter(self, filters):
        # if filters.get("topics") is None:
        #     filters["topics"] = []
        # if filters.get("address") is None:
        #     filters["address"] = []

        return filters

    def normalize_log(self, logs):
        for log in logs:
            log["blockNumber"] = log.get("block_number")
            del log["block_number"]
            log["blockHash"] = HexBytes(log.get("block_hash"))
            del log["block_hash"]
            log["logIndex"] = 1
            log["removed"] = False
            log["topics"] = [HexBytes(topic) for topic in log.get("topics")]
            log["transactionHash"] = HexBytes(log.get("transaction_hash"))
            del log["transaction_hash"]
            log["transactionIndex"] = 1


        return logs

    def get_block(self, block_identifier):
        endpoint = "get_block"
        url = requests.compat.urljoin(self.host, endpoint)
        
        if isinstance(block_identifier, int):
            block_identifier = str(block_identifier)
        
        response = requests.get(url + block_identifier)

        if response.status_code == HTTPStatus.NOT_FOUND:
            output_block = None
        else:
            block = response.json()

            output_block = AttributeDict({
                "number": block.get("block_number"),
                "hash": HexBytes(block.get("block_hash"))
            })

        return output_block

    def get_logs(self, filters):
        normalized_filters = self.normalize_filter(filters)
        endpoint = "get_logs"
        url = requests.compat.urljoin(self.host, endpoint)
        logs = requests.get(url, json=filters).json()
        normalized_log = self.normalize_log(logs)

        return normalized_log

    def add_blocks(self, blocks):
        """
        {
    "blocks": [
        {
            "block_number": 3,
            "block_hash": "0x333",
            "logs": [
                {
                    "address": "0x",
                    "data": "0x",
                    "topics": ["0x1", "0x2"],
                    "transaction_hash": "0x1"
                },
                {
                    "address": "0x1",
                    "data": "0x",
                    "topics": ["0x1", "0x2"],
                    "transaction_hash": "0x1"
                }
            ]
        },
        {
            "block_number": 4,
            "block_hash": "0x4",
            "logs": [
                {
                    "address": "0x",
                    "data": "0x",
                    "topics": ["0x1"],
                    "transaction_hash": "0x1"
                }
            ]
        },
        {
            "block_number": 5,
            "block_hash": "0x4",
            "logs": [
                {
                    "address": "0x",
                    "data": "0x",
                    "topics": ["0x1"],
                    "transaction_hash": "0x1"
                }
            ]
        }
    ]
}
        """

        endpoint = "add_blocks"
        url = requests.compat.urljoin(self.host, endpoint)
        response = requests.post(url, json=blocks)

        return response

    def delete_data(self):
        endpoint = "clean_database"
        url = requests.compat.urljoin(self.host, endpoint)
        response = requests.post(url)

        return response