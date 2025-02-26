from pymongo import MongoClient
from pydantic import BaseModel,Field
from datetime import datetime, timezone
from typing import List
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()
dburl=os.getenv("DBURL")
# Create a MongoClient instance
client = MongoClient(dburl)

# Access the 'test2' database
db = client["invoice"]
users_collection=db["users"]
invoice_collection=db["invoice"]


class User(BaseModel):
    Email: str = Field(..., example=" [email protected]")
    Password: str = Field(..., example="password")
    Name: str = Field(..., example="John Doe")
    companyName: str = Field(..., example="ABC Company")
    Address: str = Field(..., example="123 Main Street, City, Country")
    Phone: str = Field(..., example="1234567890")

class InvoiceRequest(BaseModel):
    # file_name: str
    # company_info: dict
    client_info: dict
    invoice_info: dict
    items: list

print(f"Connected to database: {db.name}")