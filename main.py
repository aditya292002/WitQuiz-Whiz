from fastapi import FastAPI, Form, status, Depends, HTTPException, Request
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
import routes.auth as auth 
import routes.mcq_generator as mcq_generator
from fastapi.templating import Jinja2Templates
from icecream import ic


app = FastAPI()
app.include_router(auth.auth_router)
app.include_router(mcq_generator.router_gen_mcq)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about-us")
async def root(request: Request):
    return templates.TemplateResponse("about_us.html", {"request": request})

