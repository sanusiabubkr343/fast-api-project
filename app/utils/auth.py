from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta

import os
from dotenv import load_dotenv

load_dotenv()

# Retrieve the values from the environment
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def  hash_password(password:str) -> str :
  return pwd_context.hash(password)

def  verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data:dict)-> str:
    to_encode =data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
