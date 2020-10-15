from itertools import groupby


def patch_web3(w3_instance, makito_client):
    w3_instance.eth.getLogs = makito_client.get_logs
    w3_instance.eth.getBlock = makito_client.get_block

    return w3_instance


def w3logs2makitologs(w3_logs):
    g = groupby(w3_logs, lambda x: x.get("blockNumber"))
    makito_logs = {
        "blocks": []
    }

    for block_number, logs in g:
        block = {
            "logs": []
        }
        for log in logs:
            l = {
                "address": log.get("address"),
                "data": log.get("data"),
                "topics": [topic.hex() for topic in log.get("topics")],
                "transaction_hash": log.get("transactionHash").hex()
            }
            block["logs"].append(l)
        block["block_number"] = log.get("blockNumber")
        block["block_hash"] = log.get("blockHash").hex()

        makito_logs["blocks"].append(block)

    return makito_logs


def get_logs(w3_instance, addresses, from_block, to_block="latest", range_=1000):
    last_block = w3_instance.eth.getBlock(to_block)
    print("last_block: {}".format(last_block.get("number")))
    current_block = from_block - 1

    while True:
        to_block = min(last_block.number, current_block + 1 + range_)
        from_block = current_block + 1
        filters = {
            "fromBlock": from_block,
            "toBlock": to_block,
            "address": addresses
        }
        print("filters: {}".format(filters))

        logs = w3_instance.eth.getLogs(filters)

        yield logs

        current_block = to_block

        if to_block == last_block.get("number"):
            break


def fill_makito_with_w3logs(makito_client, w3_instance, addresses, from_block, to_block="latest", range_=1000):
    logs_generator = get_logs(w3_instance, addresses, from_block, to_block, range_)

    for logs in logs_generator:
        logs_makited = w3logs2makitologs(logs)
        makito_client.add_blocks(logs_makited)
        