from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_invoice(file_name:str, company_info:dict, client_info:dict, invoice_info:dict, items:list):
    c = canvas.Canvas(file_name, pagesize=letter)

    # Company Information
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, company_info["name"])
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, company_info["address"])
    c.drawString(50, 715, company_info["city_state_zip"])
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

    # Save PDF
    c.save()

# Sample data
company_info = {
    "name": "Company Name",
    "address": "Address Line 1",
    "city_state_zip": "City, State, Zip",
    "phone": "(555) 555-5555",
    "email": "company@example.com"
}

client_info = {
    "name": "Client Name",
    "address": "Address Line 1",
    "city_state_zip": "City, State, Zip"
}

invoice_info = {
    "invoice_number": "12345",
    "date": "2025-02-14",
    "due_date": "2025-03-14"
}

items = [
    ("Item 1", 2, 20.0),
    ("Item 2", 1, 50.0),
    ("Item 3", 3, 15.0),
    ("Item 4", 1, 100.0)
]

# Generate the invoice
create_invoice("invoice.pdf", company_info, client_info, invoice_info, items)
