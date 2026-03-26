#Frontent ile baglantı
# backend/src/api.py

from fastapi import FastAPI, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.reader.file_reader import process_file
from src.models import User
from src.utils import hash_password, verify_password
from pydantic import BaseModel
import os
from src.services.blockchain_services import router as blockchain_router

# FastAPI uygulaması
app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Blockchain router
app.include_router(blockchain_router, prefix="/api/blockchain")

# Pydantic modelleri
class UserRegister(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# REGISTER
@app.post("/api/auth/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "success", "user_id": new_user.user_id, "email": new_user.email}

# LOGIN
@app.post("/api/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user and verify_password(user.password, db_user.password):
        return {"status": "success", "user_id": db_user.user_id, "email": db_user.email}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# FILE UPLOAD
connection_string = "mysql+pymysql://root:1234@localhost:3306/fintech_db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

os.makedirs(DATA_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile, user_id: int = Form(...)):
    file_path = os.path.join(DATA_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    process_file(file_path, connection_string, user_id)
    return {"status": "ok", "message": "File processed"}
