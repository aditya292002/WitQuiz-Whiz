from fastapi import Depends, FastAPI, HTTPException, Request, Response, status, Form, Cookie
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import secrets
from database import SessionLocal
from models import Users
from starlette.responses import RedirectResponse


app = FastAPI()

templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_session(user_id: int, db: Session):
    session_id = secrets.token_hex(16)
    user = db.query(Users).filter(Users.id == user_id).first()
    if user:
        user.session_id = session_id
        db.commit()
    return session_id


def get_current_user(session_id: str = Cookie(None), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.session_id == session_id).first()
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session"
        )


@app.get("/")
async def root(request: Request, current_user: Users = Depends(get_current_user)):
    return templates.TemplateResponse("app.html", {"request": request, "user": current_user})


@app.post("/login")
async def login(
    response: Response,
    db: Session = Depends(get_db),
    request: Request = Depends(),
    username: str = Form(...),
    password: str = Form(...),
):
    user = db.query(Users).filter_by(username=username).first()

    if not user or not bcrypt_context.verify(password, user.hashed_password):
        return templates.TemplateResponse("error.html", {"request": request})
    else:
        session_id = await create_session(user.id, db)
        response.set_cookie(key="session_id", value=session_id)
        # return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
        return templates.TemplateResponse("app.html", {"request": request})


@app.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="session_id")
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
