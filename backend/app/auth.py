"""Single-editor access gate. No accounts, signup, or credentials in the browser bundle."""
import hashlib
import hmac
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from .config import get_settings
from .database import get_db
from .limits import reserve_request
from .gemini import AIError

router = APIRouter(prefix="/api/auth")
COOKIE = "fieldnotes_session"
SESSION_SECONDS = 8 * 60 * 60


class LoginInput(BaseModel):
    password: str = Field(min_length=1, max_length=512)


def serializer(settings):
    if len(settings.session_secret) < 32:
        raise HTTPException(503, "Workspace session configuration is incomplete.")
    salt = "fieldnotes-owner-" + hashlib.sha256(settings.workspace_password.encode()).hexdigest()
    return URLSafeTimedSerializer(settings.session_secret, salt=salt)


def authenticated(request, settings):
    if not settings.workspace_password:
        return not settings.cloud
    token = request.cookies.get(COOKIE)
    if not token:
        return False
    try:
        return serializer(settings).loads(token, max_age=SESSION_SECONDS) == "owner"
    except (BadSignature, SignatureExpired):
        return False


@router.get("/session")
def session(request: Request):
    settings = get_settings()
    return {"required": bool(settings.workspace_password) or settings.cloud, "authenticated": authenticated(request, settings)}


@router.post("/login")
def login(data: LoginInput, response: Response, db: Session = Depends(get_db)):
    settings = get_settings()
    if not settings.workspace_password:
        raise HTTPException(503, "Workspace access is not configured.")
    key = "login:" + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")
    try:
        reserve_request(db, key, 10)
        db.commit()
    except AIError:
        raise HTTPException(429, "Too many login attempts. Wait a minute before trying again.") from None
    supplied = hashlib.sha256(data.password.encode()).digest()
    expected = hashlib.sha256(settings.workspace_password.encode()).digest()
    if not hmac.compare_digest(supplied, expected):
        raise HTTPException(401, "Incorrect workspace password.")
    response.set_cookie(COOKIE, serializer(settings).dumps("owner"), max_age=SESSION_SECONDS,
                        httponly=True, secure=settings.cloud, samesite="lax", path="/")
    return {"authenticated": True}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(COOKIE, path="/")
    return {"authenticated": False}
