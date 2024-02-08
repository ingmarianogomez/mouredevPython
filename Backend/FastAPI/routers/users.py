from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags= ["users"])
#basemodel = 

#Entidad user
class User(BaseModel):
    id: int
    name:str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="Mariano",surname="Gomez",url="https://chelita.com",age=36),
              User(id=2, name="Santiago",surname="Gomez",url="https://elamigo.com",age=32),
              User(id=3, name="Leticia",surname="Specogna",url="https://lele.com",age=36)]



@router.get("/usersjson")
async def usersjson():
    return [{"name":"Mariano", "surname":"Gomez", "url":"https://chelita.com","age":36},
            {"name":"Santiago", "surname":"Gomez", "url":"https://elamigo.com","age":32},
            {"name":"Leticia", "surname":"Specogna", "url":"https://lele.com","age":36}]

@router.get("/users")
async def users():
    return users_list

#Path
@router.get("/user/{id}")
async def user(id: int):
    users = filter(lambda user:user.id==id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}
    
#Query
@router.get("/userquery/")
async def user(id: int):
    users = filter(lambda user:user.id==id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}
    

@router.post("/user/", response_model= User, status_code=201)
async def user(user:User):
    if type(search_user(user.id))==User:
#        return {"error":"El usuario ya existe"}
        raise HTTPException(status_code=404, detail="El usuario ya existe")   
    else:
        users_list.append(user)
        return user



def search_user (id:int):
    users = filter(lambda user:user.id==id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}
    

@router.put("/user/")
async def user(user: User):
    try:
#    found = False

        for index, saved_user in enumerate(users_list):
            if saved_user.id == user.id:
                users_list [index] = user
#            found = True
    except:
#    if not found:
        return {"error":"No se ha encontrado el usuario"}
    else:
        return user
    
@router.delete("/user/{id}")
async def user(id: int):
    try:
#    found = False
        for index, saved_user in enumerate(users_list):
            if saved_user.id == id:
                del users_list [index]
#            found = True
    except:
#    if not found:
        return {"error":"No se ha encontrado el usuario a borrar"}
    else:
        return user