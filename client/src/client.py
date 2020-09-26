import os
import requests
from http import HTTPStatus
from web3.main import HexBytes
from web3.datastructures import AttributeDict


def patch_web3(w3_instance, makito_client):
    w3_instance.eth.getLogs = makito_client.getLogs
    w3_instance.eth.getBlock = makito_client.getBlock

    return w3_instance


class MakitoClient():
    def __init__(self, host):
        self.host = host

    def normalize_filter(self, filters):
        if filters.get("topics") is None:
            filters["topics"] = []
        if filters.get("address") is None:
            filters["address"] = []

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
            log["transactionIndex"] = 1


        return logs

    def getBlock(self, block_identifier):
        endpoint = "get_block/"
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

    def getLogs(self, filters):
        normalized_filters = self.normalize_filter(filters)
        endpoint = "get_logs/"
        url = requests.compat.urljoin(self.host, endpoint)
        logs = requests.get(url, json=filters).json()
        normalized_log = self.normalize_log(logs)

        return normalized_log
