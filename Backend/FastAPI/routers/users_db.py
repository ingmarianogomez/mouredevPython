#User DB API

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema,users_schema
from db.client import db_client
from bson import ObjectId


router = APIRouter(prefix="/userdb",
                   tags= ["userdb"])

users_list = []


@router.get("", response_model = list[User])
async def users():
    return users_schema(db_client.users.find())

#Path
@router.get("/{id}")
async def user(id: str):
    try:
        return search_user("_id", ObjectId(id))
    except:
        return {"error":"No se ha encontrado el usuario"}
    
#Query
@router.get("/")
async def user(id: str):
    try:
        return search_user("_id", ObjectId(id))
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No se ha encontrado el usuario")  
    

@router.post("/", response_model= User, status_code=201)
async def user(user:User):
    if type(search_user_by_email(user.email))==User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")   
    else:
        
        user_dict = dict(user)
        del user_dict["id"]

        id = db_client.users.insert_one(user_dict).inserted_id

        new_user = user_schema(db_client.users.find_one({"_id":id}))

        return User (**new_user)

def search_user_by_email (email: str):
    try:
        user = db_client.users.find_one({"email":email})
        return User(**user_schema(user))
    except:
        return {"error":"No se ha encontrado el usuario"}
    
def search_user (field: str, key):
    try:
        user = db_client.users.find_one({field:key})
        return User(**user_schema(user))
    except:
        return {"error":"No se ha encontrado el usuario"}
    

@router.put("/", response_model= User, status_code=201)
async def user(user: User):
    
    user_dict = dict (user)
#    del user_dict["id"] No es necesario borrar la clave
    
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)},user_dict)
    
    except:
        return {"error":"No se ha encontrado el usuario a editar"}
    
    else:
        return search_user ("_id", ObjectId(user.id))
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        return {"error":"No se ha encontrado el usuario a borrar"}
 