import torch
from transformers import BertForQuestionAnswering, BertTokenizer
import fitz  # PyMuPDF

model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

def extract_text_from_pdf( pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def answer_question( question, pdf_path):
    text = extract_text_from_pdf(pdf_path)[:512]
    encoding = tokenizer.encode_plus(text=question,text_pair=text)

    inputs = encoding['input_ids']  #Token embeddings
    sentence_embedding = encoding['token_type_ids']  #Segment embeddings
    tokens = tokenizer.convert_ids_to_tokens(inputs) #input tokens
    
    start_scores, end_scores = model(input_ids=torch.tensor([inputs]), token_type_ids=torch.tensor([sentence_embedding]), return_dict=False)
    
    start_index = torch.argmax(start_scores)
    
    end_index = torch.argmax(end_scores)
    
    answer = ' '.join(tokens[start_index:end_index+1])
    
    corrected_answer = ''
    
    for word in answer.split():
        
        #If it's a subword token
        if word[0:2] == '##':
            corrected_answer += word[2:]
        else:
            corrected_answer += ' ' + word
    
    return corrected_answer
