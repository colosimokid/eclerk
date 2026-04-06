
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from routers import user





app = FastAPI()

app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}   

@app.get("/jesus")
async def root():
    return {"message": "todo va a salir bien"}   



