# Chat RFPS: Multi Document Chatbot

Chat RFPS is a web application that allows users to upload multiple documents and interact with them through a chatbot interface. Documents are Docx, Docs, and PDFs. 

The backend is powered by **FastAPI**, integrated with **LangChain**, **Google Gemini**, and **FAISS** for document processing, vector storage, and conversational AI. The frontend is built with **React** and communicates with the backend using fetch requests for Documents uploads and chat interactions.

State management also implemented like documents that are uploaded are stored in json file so the chatbot's memory on the previously uploaded documents is maintained.

## Backend Setup

### Requirements

- Python 3.8 or higher
- Required Python Libraries:
  - `fastapi`
  - `uvicorn`
  - `PyPDF2`
  - `langchain`
  - `google-generativeai`
  - `faiss-cpu`
  - `pydantic`
  - `python-dotenv`

### Setup Steps

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd backend
   ```
2.**Create a .env file in the root directory(backend) and add your Google API key:**

```bash
GOOGLE_API_KEY=your-google-api-key
```
3.**Install the required Python dependencies inside virtual environment:**

```bash
pip install -r requirements.txt
```
4.**Run the FastAPI backend server:**

```bash
uvicorn app:app --reload
```
The backend will be running at http://localhost:8000.

## Frontend Setup

```bash
cd client
```

then install the dependencies

```bash
npm install
```

then run

```bash
npm run dev
```
