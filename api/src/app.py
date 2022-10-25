from fastapi import FastAPI

from routes.block import block_router
from routes.logs import logs_router

app = FastAPI()

app.include_router(block_router)
app.include_router(logs_router)


@app.post("/clean_database")
def clean_makito():
    clean_database()
    return {"message": "success"}

