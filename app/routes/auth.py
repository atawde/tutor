from urllib import response

from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from fastapi.responses import JSONResponse
from ..auth_utils import create_access_token

from ..db.session import SessionLocal
from ..models.user import User
from ..security import verify_password

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

class LoginRequest(BaseModel):
    email: str
    password: str

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

@router.post("/login")
def login(data: LoginRequest):

    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == data.email
        ).first()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        if not user.is_active:
            raise HTTPException(
            status_code=403,
            detail="Account is disabled"
        )
        
        if not verify_password(
            data.password,
            user.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        token = create_access_token({
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        })

        response = JSONResponse(
        {
            "redirect":
                "/admin" if user.role == "admin"
                else "/student"
        }
        )

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,      # Change to True when deployed over HTTPS
            samesite="lax",
            max_age=60 * 60,   # 1 hour
        )

        return response

    finally:
        db.close()

@router.get("/logout")
def logout():

    response = RedirectResponse("/login")

    response.delete_cookie("access_token")

    return response