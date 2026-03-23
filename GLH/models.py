from pydantic import BaseModel, EmailStr
from typing import Optional 

class UserAccount(BaseModel):
    fullName: str
    email: EmailStr
    password: str
    

class ProducerAccount(BaseModel):
    fullName: str
    email: EmailStr
    password: str
    businessName: str
    businessAddress: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    fullName: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserUpdate(BaseModel):
    fullName: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
class UserDelete(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    fullName: str
    email: EmailStr
    role: str

class UserLoginResponse(BaseModel):
    id: str
    fullName: str
    email: EmailStr
    role: str

class UserProfileResponse(BaseModel):
    id: str
    fullName: str
    email: EmailStr
    role: str