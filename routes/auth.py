from fastapi import Depends, HTTPException, Request, Response, status, Form, Cookie, APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import secrets
from database import SessionLocal
from models import Users, CreateUserRequest
from starlette.responses import RedirectResponse
from typing import Annotated
from icecream import ic
import time

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

templates = Jinja2Templates(directory="templates")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

async def create_session(user_id: int, db: Session):
    session_id = secrets.token_hex(16)
    user = db.query(Users).filter(Users.id == user_id).first()
    if user:
        user.session_id = session_id
        db.commit()
    return session_id

def get_current_user(session_id: str = Cookie(None), db: Session = Depends(get_db)):
    ic("inside get current user function")
    ic(session_id)
    if(session_id):
        user = db.query(Users).filter(Users.session_id == session_id).first()
        if user:
            return user 
    return None

def is_valid_session(session_id: str, db: Session):
    ic("inside is valid session")
    ic(session_id)
    ic(db)
    user = db.query(Users).filter(Users.session_id == session_id).first()
    ic(user)
    if user:
        return True
    return False


@router.get("/")
async def root(request: Request, db: Session = Depends(get_db)):
    ic('inside login')
    
    session_id = request.cookies.get("session_id")
    ic(session_id)
    if session_id and is_valid_session(session_id, db):
        ic("inside if")
        return templates.TemplateResponse("app.html", {"request": request})
    
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/app")
async def my_app(request: Request, db: Session =  Depends(get_db), current_user: Users = Depends(get_current_user)):
    ic("inside app")
    session_id = request.cookies.get("session_id")
    ic(session_id)
    if session_id and is_valid_session(session_id, db):
        ic("inside if")
        return templates.TemplateResponse("app.html", {"request": request, "user": current_user})
    else:
        return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register")
async def root(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/sign_up", status_code=status.HTTP_201_CREATED)
async def create_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Users).filter_by(username=username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
        
    create_user_model = Users(
        username=username,
        hashed_password=bcrypt_context.hash(password),
    )
    
    db.add(create_user_model)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    print("Done creating user")
    return RedirectResponse("/auth/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/login")
async def login(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    username: str = Form(...),
    password: str = Form(...),
):  
    
    user = db.query(Users).filter_by(username=username).first()

    if not user or not bcrypt_context.verify(password, user.hashed_password):
        return templates.TemplateResponse("error.html", {"request": request})
    else:
        session_id = await create_session(user.id, db)
        response.set_cookie(key="session_id", value=session_id)
        user.session_id = session_id
        db.commit()
        return {"message": "Successfully logged in"}
        # return templates.TemplateResponse("app.html", {"request": request})


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="session_id")
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
