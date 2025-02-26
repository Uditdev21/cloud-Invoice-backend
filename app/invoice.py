from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# import io
from .db import invoice_collection
from .cloud import upload_file
# from .payment import create_payment_link
from bson import ObjectId

def create_invoice(file_name: str, company_info: dict, client_info: dict, invoice_info: dict, items: list,userID:str):
    # buffer = io.BytesIO()  # Create an in-memory buffer
    c = canvas.Canvas(filename=file_name,pagesize=letter)

    # Company Information
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, company_info["name"])
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, company_info["address"])
    # c.drawString(50, 715, company_info["city_state_zip"])
    c.drawString(50, 700, f"Phone: {company_info['phone']}")
    c.drawString(50, 685, f"Email: {company_info['email']}")

    # Client Information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, 750, "Bill To:")
    c.setFont("Helvetica", 12)
    c.drawString(350, 730, client_info["name"])
    c.drawString(350, 715, client_info["address"])
    c.drawString(350, 700, client_info["city_state_zip"])

    # Invoice Information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 650, f"Invoice #: {invoice_info['invoice_number']}")
    c.drawString(50, 635, f"Date: {invoice_info['date']}")
    c.drawString(50, 620, f"Due Date: {invoice_info['due_date']}")

    # Table Header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 580, "Item")
    c.drawString(300, 580, "Quantity")
    c.drawString(400, 580, "Price")
    c.drawString(500, 580, "Total")

    # Table Content
    c.setFont("Helvetica", 12)
    y_position = 560
    total_amount = 0
    for item, quantity, price in items:
        total = quantity * price
        c.drawString(50, y_position, item)
        c.drawString(300, y_position, str(quantity))
        c.drawString(400, y_position, f"${price:.2f}")
        c.drawString(500, y_position, f"${total:.2f}")
        total_amount += total
        y_position -= 20

    # Total Amount
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, y_position - 10, "Total Amount:")
    c.drawString(500, y_position - 10, f"${total_amount:.2f}")

    # Save PDF to buffer
    c.save()
    # Upload directly without saving to disk
    url=upload_file(file_name) # Close the buffer to free memory
    document=invoice_collection.insert_one({"userID":ObjectId(userID),
                                            "file_name":file_name,
                                            "InvoiceURL":url,
                                            "Cost":total_amount,
                                            "status":"pending"})
    # create_payment_link(total_amount, "INR", documentID)

    return url
