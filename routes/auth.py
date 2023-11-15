from datetime import timedelta, datetime
from typing import Annotated
from fastapi import Form, APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status # to return correct status code back to user
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from icecream import ic
from starlette.responses import RedirectResponse

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUserRequest(BaseModel):
    username:str
    password:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]


templates = Jinja2Templates(directory="templates")


async def check_valid_user(db: db_dependency,
    create_user_request: CreateUserRequest, status_code=status.HTTP_200_OK):

    user = db.query(Users).filter_by(username=create_user_request.username).first()
    if not user or not bcrypt_context.verify(create_user_request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
        
    else:
        return {"status": "Valid user"}


@auth_router.get("/")
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@auth_router.post("/login")
async def process_login(db: db_dependency, request: Request, username: str = Form(...), password: str = Form(...)):   
    ic(username, password)
    user = db.query(Users).filter_by(username=username).first()
    if not user or not bcrypt_context.verify(password, user.hashed_password):
        # raise HTTPException(
            # status_code=status.HTTP_401_UNAUTHORIZED,
            # detail="Invalid credentials",
        # )
        return templates.TemplateResponse("error.html", {"request": request})
        
    else:
        return templates.TemplateResponse("app.html", {"request": request})
    

@auth_router.get("/register")
async def root(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# create a new user
@auth_router.post("/new_user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, username: str = Form(...), password: str = Form(...)):
    create_user_model = Users(
        username=username,
        hashed_password = bcrypt_context.hash(password),
    )
    
    db.add(create_user_model)
    db.commit()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    
