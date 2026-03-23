from pydantic import BaseModel, EmailStr
from typing import Optional, list 
from datetime import datetime

#User Account Model 

class UserRegistration(BaseModel):
    fullName : str
    emailAddress : EmailStr
    password : str
    confirmPassword : str
    userRole : str   # two role buyer or prducer 
    companyName : Optional[str] = None # Only for producers
    companyCategory : Optional[str] = None # Only for producers
    location : str #for both buyer and producer

class UserLogin(BaseModel):
    emailAddress : EmailStr
    password : str

class UserResponse(BaseModel):
    userID : str
    fullName : str  
    emailAddress : EmailStr
    userRole : str
    companyName : Optional[str] = None
    location : str