from fastapi import FastAPI
from .client import client 
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.include_router(client,prefix="/client",tags=["client"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}