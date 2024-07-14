from app import models, oauth, schemas
from app.database import engine
from app.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = oauth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = oauth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login/google", response_model=schemas.Token)
async def login_with_google(token: str, db: Session = Depends(get_db)):
    user = await oauth.google_login(db, token)
    access_token = oauth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login/facebook", response_model=schemas.Token)
async def login_with_facebook(token: str, db: Session = Depends(get_db)):
    user = await oauth.facebook_login(db, token)
    access_token = oauth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(oauth.get_current_user)):
    return current_user
