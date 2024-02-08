from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer (tokenUrl="login")

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
        "password": "123456"
    },
    "mariano2": {
        "username": "mariano2",
        "full_name": "Santiago Gomez",
        "email": "santiagogomez@gmail.com",
        "disable": True,
        "password": "654321"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# criterio de dependencia   
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales invalidas",
            headers={"WWW-Authenticate":"Bearer"}
            )
    if user.disabled:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, 
            detail="usuario inactivo2222")
    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")

    user = search_user (form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta2")
    
    return{"access_toke": user.username, "token_type":"bearer"}

@app.get ("/users/me")
async def me(user: User = Depends(current_user)):
    return user
