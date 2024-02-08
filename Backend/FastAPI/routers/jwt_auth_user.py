from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

#Entidad user
class User(BaseModel):
    username: str
    full_name:str
    email: str
    disabled: bool

class UserDB(User):
    password: str
       

users_db = {
    "mariano": {
        "username": "mariano",
        "full_name": "Mariano Gomez",
        "email": "marianogomez@gmail.com",
        "disable": False,
        "password": "$2a$12$CdoOhQlKc0K.IoRk5u5vke7c0mKsx9ScasWRJty6GNdrRdVYdrEhC"
    },
    "mariano2": {
        "username": "mariano2",
        "full_name": "Santiago Gomez",
        "email": "santiagogomez@gmail.com",
        "disable": True,
        "password": "$2a$12$SYoSTZxJyIRdQyHWXiH8hOWANzkYDqXwAd2aGdlaqqy7EODkPytMG"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

@app.post("/login/")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta2")

    access_token = {"sub":user.username, 
                    "exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
                    

    return{"access_token": access_token, "token_type":"bearer"}