from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from core.config import get_settings
import os
import tempfile
import shutil

from schema.models import QueryRequest, QueryResponse
from prompts.rag_prompt import RagPrompt
from parser.document_loader import DocumentLoader
from memory.redis_memory import RedisMemoryManager

from langchain_groq import ChatGroq

from pipeline.rag_pipeline import RagPipeline

from dotenv import load_dotenv
load_dotenv()

settings = get_settings()



MODEL_VERSION = "1.0.0"  

llm = ChatGroq(model= settings.GROQ_MODEL, api_key= settings.GROQ_API_KEY)

pipeline = RagPipeline(llm = llm)

app = FastAPI(
    title= "Advanced RAG Pipeline",
    description= "RAG Pipeline API",
    version= MODEL_VERSION,
)



#----------------
# LANDING PAGE
#----------------

@app.get("/")
def read_root():
    return JSONResponse(
        status_code=200,
        content= {"message": "Welcome to the RAG Pipeline API",
                 "version": MODEL_VERSION
            }
    )


#----------------
# HEALTH CHECK
#----------------

@app.get("/health")
def check_health():
    return JSONResponse(
        status_code=200,
        content= {
            "status": "success",
            "Model Version": MODEL_VERSION,
            "api": "Up and Running",
            "message": "Healthy"
        }         
    )


#------------------------------
# Build Index/ Ingest Documents
#------------------------------

@app.post("/upload")
async def build_index(file: UploadFile = File(..., description="Upload a PDF or DOCX file")):

    tmp_path = None

    try :
        '''Validate file type'''
        ext = file.filename.split(".")[-1].lower()

        if ext not in ["pdf", "docx"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload a PDF or DOCX file."
            )
        
        with tempfile.NamedTemporaryFile(delete= False, suffix= f".{ext}") as tmp_file:
            tmp_path = tmp_file.name

            '''copies file stream to new real file'''
            shutil.copyfileobj(file.file, tmp_file)

            result = pipeline.build_index(tmp_path)

            return JSONResponse(
                status_code=200,
                content= {
                    "status": result["status"],
                    "message": result["message"],
                    "chunks": result["chunks"]
                }
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error ingesting document: {e}"
        )
    
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)



# -------------
# User Input
#-------------

@app.post("/query", response_model= QueryResponse)
async def query_documents(request: QueryRequest):
    session_id = request.session_id
    question = request.question
    try:
        response = pipeline.user_input(session_id, question)
        return {"answer": response}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing user input: {e}"
        )

        