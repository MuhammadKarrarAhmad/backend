from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from database import db
from GLH.models import UserAccount, ProducerAccount, UserLogin, UserProfile, UserUpdate, UserDelete, UserResponse, UserLoginResponse, UserProfileResponse

GLH_router = APIRouter(prefix="/api")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
