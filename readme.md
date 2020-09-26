# Makito

## Endpoints

### Add blocks

url: localhost:8080/add_blocks

example:

```sh
curl --location --request POST 'localhost:8000/add_blocks' \
--header 'Content-Type: application/json' \
--data-raw '{
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
}'

```


### get block

url: localhost:8080/get_block

example: 

```sh
curl --location --request GET 'localhost:8000/get_block/3'
```

output:

```json
{
    "block_number": 3,
    "block_hash": "0x333"
}
```
### get logs

url: localhost:8080/get_logs

example:

```sh
curl --location --request GET 'localhost:8000/get_logs' \
--header 'Content-Type: application/json' \
--data-raw '{
    "fromBlock": 1,
    "toBlock": 4,
    "address": []
}'
```

output:

```json
[
    {
        "block_number": 3,
        "block_hash": "0x333",
        "address": "0x",
        "data": "0x",
        "topics": [
            "0x1",
            "0x2"
        ],
        "transaction_hash": "0x1"
    },
    {
        "block_number": 3,
        "block_hash": "0x333",
        "address": "0x1",
        "data": "0x",
        "topics": [
            "0x1",
            "0x2"
        ],
        "transaction_hash": "0x1"
    },
    {
        "block_number": 4,
        "block_hash": "0x4",
        "address": "0x",
        "data": "0x",
        "topics": [
            "0x1"
        ],
        "transaction_hash": "0x1"
    }
]
```