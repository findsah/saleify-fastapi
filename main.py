from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware

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

fake_db = {
    "users": []
}

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

@app.post("/login", summary="User Login", description="Login a user with email and password")
async def login(login: Login):
    for user in fake_db["users"]:
        if user["email"] == login.email and user["password"] == login.password:
            user_details = {
                "username": user.get("username"),
                "email": user["email"]
            }
            return {"message": "Login successful", "user": user_details}
    raise HTTPException(status_code=400, detail="Invalid credentials")

@app.post("/signup", summary="User Signup", description="Register a new user with username, email, password, and terms acceptance")
async def signup(signup: Signup):
    for user in fake_db["users"]:
        if user["email"] == signup.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    if not signup.terms:
        raise HTTPException(status_code=400, detail="You must accept the terms and conditions")
    fake_db["users"].append(signup.dict())
    return {"message": "Signup successful"}

@app.post("/login/google", summary="Google Login", description="Login or register a user with Google account information")
async def login_with_google(response: GoogleResponse):
    for user in fake_db["users"]:
        if user["email"] == response.email:
            return {"message": "Login with Google successful"}
    fake_db["users"].append({"email": response.email, "google_id": response.google_id})
    return {"message": "User registered with Google"}

@app.post("/login/facebook", summary="Facebook Login", description="Login or register a user with Facebook account information")
async def login_with_facebook(response: FacebookResponse):
    for user in fake_db["users"]:
        if user["email"] == response.email:
            return {"message": "Login with Facebook successful"}
    fake_db["users"].append({"email": response.email, "facebook_id": response.facebook_id})
    return {"message": "User registered with Facebook"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
