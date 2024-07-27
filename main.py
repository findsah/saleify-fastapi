from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

# Database URL
DATABASE_URL = "sqlite:///./test.db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database setup for async usage
database = Database(DATABASE_URL)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(
    title="Saleify API",
    description="API for Saleify application, providing user authentication and social login functionality.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User database model
class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    terms = Column(Boolean)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class Login(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "yourpassword"
            }
        }

class Signup(BaseModel):
    username: str
    email: EmailStr
    password: str
    terms: bool

    class Config:
        schema_extra = {
            "example": {
                "username": "yourusername",
                "email": "user@example.com",
                "password": "yourpassword",
                "terms": True
            }
        }

class GoogleResponse(BaseModel):
    email: EmailStr
    google_id: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "google_id": "googleid"
            }
        }

class FacebookResponse(BaseModel):
    email: EmailStr
    facebook_id: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "facebook_id": "facebookid"
            }
        }

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password):
    return pwd_context.hash(password)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/login", summary="User Login", description="Login a user with email and password")
async def login(login: Login):
    query = "SELECT * FROM users WHERE email = :email"
    user = await database.fetch_one(query=query, values={"email": login.email})
    
    if user and pwd_context.verify(login.password, user['password']):
        user_details = {
            "username": user['username'],
            "email": user['email']
        }
        access_token = create_access_token(data={"sub": user['email']})
        return {
            "message": "Login successful",
            "user": user_details,
            "access_token": access_token,
            "token_type": "bearer"
        }
    raise HTTPException(status_code=400, detail="Invalid credentials")

@app.post("/signup", summary="User Signup", description="Register a new user with username, email, password, and terms acceptance")
async def signup(signup: Signup):
    query = "SELECT * FROM users WHERE email = :email"
    existing_user = await database.fetch_one(query=query, values={"email": signup
    .email})
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if not signup.terms:
        raise HTTPException(status_code=400, detail="You must accept the terms and conditions")
    
    user = User(
        email=signup.email,
        username=signup.username,
        password=get_password_hash(signup.password),
        terms=signup.terms
    )

    # Insert the new user into the database
    query = "INSERT INTO users(email, username, password, terms) VALUES (:email, :username, :password, :terms)"
    values = {
        "email": user.email,
        "username": user.username,
        "password": user.password,
        "terms": user.terms
    }
    await database.execute(query=query, values=values)
    
    return {"message": "Signup successful"}

@app.post("/login/google", summary="Google Login", description="Login or register a user with Google account information")
async def login_with_google(response: GoogleResponse):
    query = "SELECT * FROM users WHERE email = :email"
    user = await database.fetch_one(query=query, values={"email": response.email})
    
    if user:
        return {"message": "Login with Google successful"}
    
    query = "INSERT INTO users (email) VALUES (:email)"
    await database.execute(query=query, values={"email": response.email})
    
    return {"message": "User registered with Google"}

@app.post("/login/facebook", summary="Facebook Login", description="Login or register a user with Facebook account information")
async def login_with_facebook(response: FacebookResponse):
    query = "SELECT * FROM users WHERE email = :email"
    user = await database.fetch_one(query=query, values={"email": response.email})
    
    if user:
        return {"message": "Login with Facebook successful"}
    
    query = "INSERT INTO users (email) VALUES (:email)"
    await database.execute(query=query, values={"email": response.email})
    
    return {"message": "User registered with Facebook"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
