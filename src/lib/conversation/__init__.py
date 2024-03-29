import torch
from transformers import BertForQuestionAnswering, BertTokenizer
import fitz  # PyMuPDF
import os

model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

def extract_text_from_pdf( pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def answer_question(question, pdf_path):
    text = extract_text_from_pdf(pdf_path)
    import requests
    
    url = "https://api.perplexity.ai/chat/completions"
    
    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": f"Context: {text} \n Considering this context, answer the users questions appropriately"
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer " + os.environ["PERPLEXITY_API_KEY"]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(response.text)
    
    return response.json()["choices"][0]["message"]["content"]
