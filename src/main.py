import uvicorn
import logging
from fastapi import FastAPI, File, Form
from lib.pdf import PDFHandler
from typing import Annotated
from lib.conversation import Conversation

app = FastAPI()
logger = logging.getLogger(__name__)
convo = Conversation()

@app.get("/")
async def root():
    return {"message": "Hello There"}

@app.post("/pdf/upload")
async def upload_pdf(file: Annotated[bytes, File()], name: str = Form(..., description="File name")):
    logger.log(
        logging.INFO,
        f"Received PDF file: {name} of size {len(name) / (1024)} kilobytes"
    )
    # Code to handle the PDF upload
    PDFHandler.add_file(file, name)
    return {"message": "PDF uploaded successfully"}

@app.post("/conversation/ask")
async def ask_question(data: dict):
    question = data.get("question")
    file = PDFHandler.get_file(data.get("file"))
    logger.log(
        logging.INFO,
        f"Received question: {question} for file: {file}"
    )
    answer = convo.answer_question(question, file.file_path)
    return {"answer": answer}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
