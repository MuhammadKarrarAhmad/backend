from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional, Literal 
from datetime import datetime

#User Account Model 

class UserRegistration(BaseModel):
    fullName : str
    emailAddress : EmailStr
    password : str
    confirmPassword : str
    userRole : Literal["buyer", "producer"]  # two role buyer or prducer 
    companyName : Optional[str] = None # Only for producers
    companyCategory : Optional[str] = None # Only for producers
    location : str #for both buyer and producer

    # Custom validation to ensure companyName and companyCategory are provided for producers
    @model_validator(mode = "after")
    def validate_producer_fields(self):
        if self.userRole == "producer":
            if not self.companyName:
                raise ValueError("companyName is required for producers")
            if not self.companyCategory:
                raise ValueError("companyCategory is required for producers")
        return self


#User Login Model
class UserLogin(BaseModel):
    emailAddress : EmailStr
    password : str

#User Response Model
class UserResponse(BaseModel):
    userID : str
    fullName : str  
    emailAddress : EmailStr
    userRole : str
    companyName : Optional[str] = None
    location : str