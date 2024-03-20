import uvicorn
import logging
from fastapi import FastAPI
from lib.pdf import PDFFile

app = FastAPI()
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
