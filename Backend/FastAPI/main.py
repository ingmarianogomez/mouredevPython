#instala FastAPI: py -m pip install "fastapi[all]"

from fastapi import FastAPI
from routers import products, users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(users_db.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Url local: http://127.0.0.1:8000/
@app.get("/")
async def root():
    return "Hola FastAPI!"

# Url local: http://127.0.0.1:8000/url
@app.get("/url")
async def url():
    return {"url_curso":"https://fastapi.tiangolo.com/"}

# Iniciar el server: py -m uvicorn main:app --reload
# Para el server: Control + C
# Documentation con swagger: http://127.0.0.1:8080/docs
# Documentation con redocly: http://127.0.0.1:8080/redoc





