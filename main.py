from fastapi import Depends, FastAPI, HTTPException, Request, Response, status, Form, Cookie
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import secrets
from database import SessionLocal
from models import Users
from starlette.responses import RedirectResponse
from routes.auth import router as auth_router
from routes.mcq_generator import router_gen_mcq
import models
from database import engine, SessionLocal
# from routes import auth as 


app = FastAPI()
app.include_router(auth_router)
app.include_router(router_gen_mcq)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about-us")
async def root(request: Request):
    return templates.TemplateResponse("about_us.html", {"request": request})