# from typing import Annotated
from fastapi import APIRouter
from icecream import ic
from fastapi import Request, Form, FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from routes.mcq_generator import * 
from scrapper import *
from openai_handler import *
import asyncio
from fastapi.templating import Jinja2Templates


router_gen_mcq = APIRouter(
    prefix='/process',
    tags=['process']
)


class URL(BaseModel): 
    url: str


templates = Jinja2Templates(directory="templates")




async def test(user_input):
    ic(user_input)
    
    thread = client.beta.threads.create()
    
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    ic(client.beta.threads.messages.list(thread_id=thread.id).data)
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions="""
        Generate a  multiple choice questions. 
        """
    )    
    
    

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        await asyncio.sleep(3)
        print(run.status)
        print(user_input[:10])
        if run.status in ("completed", "failed"):
            break
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    latest_message = messages.data[0]
    text = latest_message.content[0].text.value

    # deleting the thread
    response = client.beta.threads.delete(thread.id)
    ic(response)

    return text
        


@router_gen_mcq.post("/urls")
async def process_urls(request: Request, url: str = Form(...)):
    print(url)
    data_scrapper_obj = data_scrapper()
    print(data_scrapper_obj)
    data_scrapper_obj.scrape_web_content(url)
    data = data_scrapper_obj.myWebData
    
    # for the sake of simplicity and avoid overuse of API i am considering only 3 chunks of data
    data = data[:min(len(data), 1600)]
    chunks = []
    ind = 0
    count_chunks = 0
    while(ind < len(data) and count_chunks < 3):
        chunks.append(' '.join(data[ind:ind+500][:30]))
        ind += 500
        count_chunks += 1
        
    ic(chunks)

    
    mcqs = await asyncio.gather(*(test(chunk) for chunk in chunks))
    print(mcqs)
    ans = []
    # for mcq in mcqs:
        
    return templates.TemplateResponse("app.html", {"request": request, "mcqs": mcqs})
      
    
@router_gen_mcq.post("/pdf")
async def upload_pdf(request: Request, pdf: UploadFile = File(...)):
    ic("inside upload pdf post")
    # Check if the uploaded file is a PDF
    if pdf.filename.endswith(".pdf"):
        pdf_content = await pdf.read()  # Asynchronously read the contents of the PDF file
        data_scrapper_obj = data_scrapper()
        data_scrapper_obj.extract_pdf_content(pdf_content)
        data = data_scrapper_obj.myPdfData

        # For simplicity, consider only 3 chunks of data
        data = data[:min(len(data), 1600)]
        chunks = [' '.join(data[i:i+500][:30]) for i in range(0, len(data), 500)][:3]
        ic(chunks)

        mcqs = await asyncio.gather(*(test(chunk) for chunk in chunks))
        print(mcqs)

        return templates.TemplateResponse("app.html", {"request": request, "mcqs": mcqs})

    else:
        return JSONResponse(content={"error": "Please upload a PDF file"}, status_code=400)
    
@router_gen_mcq.get("/pdf")
async def upload_pdf(request: Request, pdf: UploadFile = File(...)):
    ic("inside upload pdf get")
    # Check if the uploaded file is a PDF
    if pdf.filename.endswith(".pdf"):
        data_scrapper_obj = data_scrapper()
        data_scrapper_obj.extract_pdf_content(pdf)
        data = data_scrapper_obj.myPdfData
        # for the sake of simplicity and avoid overuse of API i am considering only 3 chunks of data
        data = data[:min(len(data), 1600)]
        chunks = []
        ind = 0
        count_chunks = 0
        while(ind < len(data) and count_chunks < 3):
            chunks.append(' '.join(data[ind:ind+500][:30]))
            ind += 500
            count_chunks += 1
            
        ic(chunks)

        
        mcqs = await asyncio.gather(*(test(chunk) for chunk in chunks))
        print(mcqs)
        ans = []
        # for mcq in mcqs:
            
        return templates.TemplateResponse("app.html", {"request": request, "mcqs": mcqs})
        
    
        
        
    else:
        return JSONResponse(content={"error": "Please upload a PDF file"}, status_code=400)
    
    
@router_gen_mcq.post("/pdf")
async def upload_pdf(request: Request, pdf: UploadFile = File(...)):
    ic("inside upload pdf")
    # Check if the uploaded file is a PDF
    if pdf.filename.endswith(".pdf"):
        data_scrapper_obj = data_scrapper()
        data_scrapper_obj.extract_pdf_content(pdf)
        data = data_scrapper_obj.myPdfData
        # for the sake of simplicity and avoid overuse of API i am considering only 3 chunks of data
        data = data[:min(len(data), 1600)]
        chunks = []
        ind = 0
        count_chunks = 0
        while(ind < len(data) and count_chunks < 3):
            chunks.append(' '.join(data[ind:ind+500][:30]))
            ind += 500
            count_chunks += 1
            
        ic(chunks)

        
        mcqs = await asyncio.gather(*(test(chunk) for chunk in chunks))
        print(mcqs)
        ans = []
        # for mcq in mcqs:
            
        return templates.TemplateResponse("app.html", {"request": request, "mcqs": mcqs})
        
    
        
        
    else:
        return JSONResponse(content={"error": "Please upload a PDF file"}, status_code=400)
    
        
    
    
    
    
    
    
    
    