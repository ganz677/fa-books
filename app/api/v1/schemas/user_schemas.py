from pydantic import  BaseModel, EmailStr


class UserRead(BaseModel):
    id: int
    email: EmailStr | None
    username: str
    active: bool

    class Config:
        from_attributes = True
        
        
class UserCreate(BaseModel):
    email: EmailStr | None
    username: str
    password: str
    
    
class UserLogin(BaseModel):
    username: str
    password: str



class AuthResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'