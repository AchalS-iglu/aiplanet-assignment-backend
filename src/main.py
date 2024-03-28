import uvicorn
import logging
from fastapi import FastAPI, File, Form, Response
from lib.pdf import PDFHandler
from typing import Annotated
from lib.conversation import answer_question

app = FastAPI()
logger = logging.getLogger(__name__)

@app.get("/pdf/status", status_code=200)
async def root():
    # test error 500
    return Response(content="Hello World", media_type="text/plain")

@app.post("/pdf/upload", status_code=201)
async def upload_pdf(file: Annotated[bytes, File()], name: str = Form(..., description="File name")):
    logger.log(
        logging.INFO,
        f"Received PDF file: {name} of size {len(name) / (1024)} kilobytes"
    )
    # Code to handle the PDF upload
    PDFHandler.add_file(file, name)
    return {"message": "PDF uploaded successfully"}

@app.get("/pdf/getlist", status_code=200)
async def get_pdf_list():
    logger.log(
        logging.INFO,
        "Received request for PDF list"
    )
    # Code to get the list of PDFs
    return {"files": PDFHandler.files}

@app.delete("/pdf/remove", status_code=200)
async def remove_pdf(file: str):
    logger.log(
        logging.INFO,
        f"Received request to remove file: {file}"
    )
    # Code to remove the PDF
    PDFHandler.remove_file(file)
    return {"message": "File removed successfully"}

@app.get("/pdf/get", status_code=200)
async def get_pdf(file: str):
    logger.log(
        logging.INFO,
        f"Received request to get file: {file}"
    )
    # Code to get the PDF
    pdf = PDFHandler.get_file(file)
    if pdf is None:
        return {"message": "File not found"}

    # Return the PDF bytes as a response
    response = Response(content=pdf, media_type="application/pdf")
    response.headers["Content-Disposition"] = f"attachment; filename={file}"
    return response
    

@app.post("/conversation/ask", status_code=200)
async def ask_question(question: str, file: str):
    # get file path
    file = PDFHandler.get_filepath(file)
    logger.log(
        logging.INFO,
        f"Received question: {question} for file: {file}"
    )
    answer = answer_question(question, PDFHandler.get_filepath(file))
    return {"answer": answer}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
