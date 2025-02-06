# from fastapi import FastAPI, File, UploadFile,HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from PyPDF2 import PdfReader
# import os
# import zipfile
# import xml.etree.ElementTree as ET
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import google.generativeai as genai
# from langchain.vectorstores import FAISS
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.question_answering import load_qa_chain
# from langchain.prompts import PromptTemplate
# from dotenv import load_dotenv
# import io
# from typing import List

# load_dotenv()

# genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# global_faiss_index = None

# def get_text_from_pdf(pdf_file):
#     text = ""
#     reader = PdfReader(pdf_file)
#     for page in reader.pages:
#         text += page.extract_text()
#     return text

# def extract_text_from_docx(docx_file):
#     with zipfile.ZipFile(docx_file, "r") as docx_zip:
#         xml_content = docx_zip.read("word/document.xml")
#         tree = ET.fromstring(xml_content)
        
#         # Extract text from XML structure
#         text = []
#         for elem in tree.iter():
#             if elem.tag.endswith("}t"):  # Extract text from <w:t> elements
#                 text.append(elem.text)

#     return "\n".join(filter(None, text))  # Join and remove empty entries

# def get_text_chunks(text):
#     splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
#     chunks = splitter.split_text(text)
#     return chunks

# def get_embeddings(text_chunks):
#     embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
#     vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
#     return vector_store

# def get_conversational_chain():
#     prompt_template = """
#         You are an RFP Analyzer bot designed to extract and provide answers *strictly* from the uploaded RFP document.  Your primary function is to answer questions related to specific sections or headings within the RFP.

#         **Instructions:**

#         1. **RFP Section/Heading Questions:** If the user provides a specific RFP section or heading, extract and provide the *complete* content related to that section/heading from the document.  Be thorough and detailed in your response.  Clearly indicate the section/heading being addressed.

#         2. **RFP-Related Questions:** If the user asks a question that is directly related to the content of the RFP (but not a specific section/heading), answer the question using information from the document.  Provide context where relevant.

#         3. **Out-of-Scope Questions:** If the user asks a question that is *not* related to the RFP document's content (e.g., general knowledge, personal opinions, etc.), respond with: "I am only able to answer questions based on the provided RFP document."

#         4. **Greetings/Introductions:** If the user greets you (e.g., "Hi," "Hello," "Who are you?"), introduce yourself as an RFP Analyzer bot.  For example: "Hello, I am an RFP Analyzer bot. I can answer questions based on the content of the RFP document you provide."

#         5. **No External Information:** Do not access or use any information outside of the provided RFP document.

#         **Input Format:**

#         The user's input will consist of either a specific RFP section/heading or a question related to the RFP.

#         **Response Format:**

#         Your response should be clear, concise, and directly address the user's input.  If answering a question about a specific section/heading, clearly state the section/heading before providing the content.  If the answer is not found in the document, use the specific out-of-scope message: "I am only able to answer questions based on the provided RFP document."

#         **Context:**

#         {context}

#         **User Input:**

#         {question}

#         **Answer:**
#     """
    
#     model = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0.3)
#     prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
#     chain = load_qa_chain(model, chain_type='stuff', prompt=prompt)
#     return chain

# # @app.post("/upload")
# # async def process_pdfs(files: List[UploadFile] = File(...)):
# #     global global_faiss_index
# #     try:
# #         all_text = ""
# #         for file in files:
# #             pdf_content = await file.read()
# #             pdf_file = io.BytesIO(pdf_content)
# #             text = get_text_from_pdf(pdf_file)
# #             all_text += text + "\n\n"
        
# #         text_chunks = get_text_chunks(all_text)
# #         global_faiss_index = get_embeddings(text_chunks)
        
# #         return JSONResponse(content={"message": f"Successfully processed {len(files)} files"})
    
# #     except Exception as e:
# #         return JSONResponse(content={"error": str(e)}, status_code=400)

# @app.post("/upload")
# async def process_files(files: List[UploadFile] = File(...)):
#     global global_faiss_index
#     try:
#         all_text = ""
#         for file in files:
#             file_content = await file.read()
#             file_io = io.BytesIO(file_content)

#             if file.filename.lower().endswith(".pdf"):
#                 text = get_text_from_pdf(file_io)
#             elif file.filename.lower().endswith(".docx"):
#                 text = extract_text_from_docx(file_io)
#             else:
#                 return JSONResponse(content={"error": f"Unsupported file type: {file.filename}"}, status_code=400)

#             all_text += text + "\n\n"
        
#         text_chunks = get_text_chunks(all_text)
#         global_faiss_index = get_embeddings(text_chunks)

#         return JSONResponse(content={"message": f"Successfully processed {len(files)} files"})
    
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=400)

# class ChatRequest(BaseModel):
#     question: str

# @app.post("/chat")
# async def chat(chat_request: ChatRequest):
#     global global_faiss_index
#     try:
#         if global_faiss_index is None:
#             raise HTTPException(status_code=400, detail="No PDFs have been uploaded yet")
        
#         docs = global_faiss_index.similarity_search(chat_request.question)
#         chain = get_conversational_chain()
#         response = chain({"input_documents": docs, "question": chat_request.question}, return_only_outputs=True)

#         return JSONResponse(content={"response": response['output_text']})
    
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


#  -------------------------------------------------------------------------------------------


#                 WITH 


# Backend (app.py):

# Add a JSON-based storage system to save uploaded documents and their processed data.

# Add endpoints to reset/delete documents and manage document history.

# Ensure the chatbot uses the saved JSON data for memory and context.


from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PyPDF2 import PdfReader
import os
import zipfile
import xml.etree.ElementTree as ET
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import io
from typing import List, Dict
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
global_faiss_index = None
uploaded_files = []  # Stores metadata of uploaded files

# File to store uploaded files metadata
UPLOADED_FILES_JSON = "uploaded_files.json"

def load_uploaded_files():
    """Load uploaded files metadata from JSON file."""
    if os.path.exists(UPLOADED_FILES_JSON):
        with open(UPLOADED_FILES_JSON, "r") as f:
            return json.load(f)
    return []

def save_uploaded_files(files):
    """Save uploaded files metadata to JSON file."""
    with open(UPLOADED_FILES_JSON, "w") as f:
        json.dump(files, f)

def get_text_from_pdf(pdf_file):
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_file):
    with zipfile.ZipFile(docx_file, "r") as docx_zip:
        xml_content = docx_zip.read("word/document.xml")
        tree = ET.fromstring(xml_content)
        text = []
        for elem in tree.iter():
            if elem.tag.endswith("}t"):
                text.append(elem.text)
    return "\n".join(filter(None, text))

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = splitter.split_text(text)
    return chunks

def get_embeddings(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store

def get_conversational_chain():
    prompt_template = """
        You are an RFP Analyzer bot designed to extract and provide answers *strictly* from the uploaded RFP document.  Your primary function is to answer questions related to specific sections or headings within the RFP.

        **Instructions:**

        1. **RFP Section/Heading Questions:** If the user provides a specific RFP section or heading, extract and provide the *complete* content related to that section/heading from the document.  Be thorough and detailed in your response.  Clearly indicate the section/heading being addressed.

        2. **RFP-Related Questions:** If the user asks a question that is directly related to the content of the RFP (but not a specific section/heading), answer the question using information from the document.  Provide context where relevant.

        3. **Out-of-Scope Questions:** If the user asks a question that is *not* related to the RFP document's content (e.g., general knowledge, personal opinions, etc.), respond with: "I am only able to answer questions based on the provided RFP document."

        4. **Greetings/Introductions:** If the user greets you (e.g., "Hi," "Hello," "Who are you?"), introduce yourself as an RFP Analyzer bot.  For example: "Hello, I am an RFP Analyzer bot. I can answer questions based on the content of the RFP document you provide."

        5. **No External Information:** Do not access or use any information outside of the provided RFP document.

        **Input Format:**

        The user's input will consist of either a specific RFP section/heading or a question related to the RFP.

        **Response Format:**

        Your response should be clear, concise, and directly address the user's input.  If answering a question about a specific section/heading, clearly state the section/heading before providing the content.  If the answer is not found in the document, use the specific out-of-scope message: "I am only able to answer questions based on the provided RFP document."

        **Context:**

        {context}

        **User Input:**

        {question}

        **Answer:**
    """
    model = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
    chain = load_qa_chain(model, chain_type='stuff', prompt=prompt)
    return chain

@app.post("/upload")
async def process_files(files: List[UploadFile] = File(...)):
    global global_faiss_index, uploaded_files
    try:
        all_text = ""
        uploaded_files = load_uploaded_files()

        for file in files:
            file_content = await file.read()
            file_io = io.BytesIO(file_content)

            if file.filename.lower().endswith(".pdf"):
                text = get_text_from_pdf(file_io)
            elif file.filename.lower().endswith(".docx"):
                text = extract_text_from_docx(file_io)
            else:
                return JSONResponse(content={"error": f"Unsupported file type: {file.filename}"}, status_code=400)

            all_text += text + "\n\n"
            uploaded_files.append({"filename": file.filename, "size": len(file_content)})

        text_chunks = get_text_chunks(all_text)
        global_faiss_index = get_embeddings(text_chunks)
        save_uploaded_files(uploaded_files)

        return JSONResponse(content={"message": f"Successfully processed {len(files)} files", "files": uploaded_files})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.get("/upload")
async def get_uploaded_files():
    try:
        uploaded_files = load_uploaded_files()
        return JSONResponse(content={"files": uploaded_files})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.post("/reset")
async def reset_files():
    global global_faiss_index, uploaded_files
    try:
        global_faiss_index = None
        uploaded_files = []
        save_uploaded_files(uploaded_files)
        return JSONResponse(content={"message": "All files and history have been reset."})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.post("/delete/{filename}")
async def delete_file(filename: str):
    global uploaded_files
    try:
        uploaded_files = load_uploaded_files()
        uploaded_files = [file for file in uploaded_files if file["filename"] != filename]
        save_uploaded_files(uploaded_files)
        return JSONResponse(content={"message": f"File '{filename}' deleted successfully.", "files": uploaded_files})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat(chat_request: ChatRequest):
    global global_faiss_index
    try:
        if global_faiss_index is None:
            raise HTTPException(status_code=400, detail="No files have been uploaded yet")
        
        docs = global_faiss_index.similarity_search(chat_request.question)
        chain = get_conversational_chain()
        response = chain({"input_documents": docs, "question": chat_request.question}, return_only_outputs=True)

        return JSONResponse(content={"response": response['output_text']})
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)