from fastapi import APIRouter, HTTPException, Depends, status,Query
from .db import users_collection,User,InvoiceRequest,invoice_collection
from .auth import PasswordAuth
from .auth import JwtToken
from .invoice import create_invoice
from bson import ObjectId


client = APIRouter()

@client.post("/createUser")
def create_user(user: User):
    """Create a new user in the database."""
    try:
        if(users_collection.find_one({"Email": user.Email})):
            raise HTTPException(status_code=400, detail="User already exists")
        user.Password = PasswordAuth.hash_password(user.Password)
        
        user_dict = user.dict()  # Convert Pydantic model to dictionary
        result = users_collection.insert_one(user_dict)
        userid= result.inserted_id
        token=JwtToken.create_access_token(data={"id":userid,"email": user.Email, "name": user.Name, "companyName": user.companyName, "address": user.Address, "phone": user.Phone})
        return {"message": "User created successfully", "id": str(result.inserted_id), "access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")

@client.get("/login")
def login_user(email: str = Query(...), password: str = Query(...)):
    """Login a user and return an access token."""
    try:
        # Retrieve the user from the database
        user_data = users_collection.find_one({"Email": email})
        
        # Check if user exists
        if user_data is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify the password
        if not PasswordAuth.verify_password(password, user_data["Password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Prepare the payload for the JWT (you can add more user details if needed)
        user_payload = {"email": user_data["Email"], "id": str(user_data["_id"]), "name": user_data["Name"], "companyName": user_data["companyName"], "address": user_data["Address"], "phone": user_data["Phone"]}
        
        # Create an access token
        access_token = JwtToken.create_access_token(data=user_payload)
        
        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")

@client.post("/createinvoice",status_code=status.HTTP_201_CREATED)
def create_invoice_endpoint(file_data:InvoiceRequest,
                   user: dict = Depends(JwtToken.verify_and_decode_jwt)):
    """Create an invoice for the logged-in user."""
    try:
        # print(f"Received Data: {file_data}")
        user_id = user["id"]
        if(user_id is None):
            raise HTTPException(status_code=401, detail="Unauthorized")
        user_Doc=users_collection.find_one({"_id":ObjectId(user_id)})
        user_Doc.pop("_id")
        user_Doc.pop("Password")
        filename="invoice.pdf"
        print(f"User data: {user_Doc}")
        company_info = {}
        company_info["name"]=user_Doc["companyName"]
        company_info["address"]=user_Doc["Address"]
        company_info["phone"]=user_Doc["Phone"]
        company_info["email"]=user_Doc["Email"]
        if "companyName" not in user_Doc:
           print("Missing companyName in user_Doc:", user_Doc)
        print(f"Company Info: {company_info}")
        url=create_invoice(filename, 
                           company_info,
                            file_data.client_info, 
                            file_data.invoice_info,
                            file_data.items,
                            user_id)
        return {"message": "Invoice created successfully","Url":url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")
    
@client.get("/getinvoices")
def get_invoice(user: dict = Depends(JwtToken.verify_and_decode_jwt)):
    """Get all invoices for the logged-in user."""
    try:
        user_id = user["id"]
        if(user_id is None):
            raise HTTPException(status_code=401, detail="Unauthorized")
        invoices = invoice_collection.find({"userID": ObjectId(user_id)})
        invoices_list = []
        for invoice in invoices:
            invoice["_id"] = str(invoice["_id"])
            invoice["userID"]=str(invoice["userID"])
            invoices_list.append(invoice)
        return invoices_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")

@client.get("/getinvoice/{invoice_id}")
def get_invoice_by_id(invoice_id: str):
    """Get an invoice by ID for the logged-in user."""
    try:
        invoice = invoice_collection.find_one({"_id": ObjectId(invoice_id)})
        if invoice is None:
            raise HTTPException(status_code=404, detail="Invoice not found")
        invoice["_id"] = str(invoice["_id"])
        invoice["userID"]=str(invoice["userID"])
        return invoice
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")
