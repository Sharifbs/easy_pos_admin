from http.server import BaseHTTPRequestHandler
import json
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))

        cust_name = str(post_data.get('custName', 'Valued Customer'))
        phone = str(post_data.get('phone', 'N/A'))
        item = str(post_data.get('item', 'Item'))
        qty = float(post_data.get('qty', 1))
        price = float(post_data.get('price', 0))
        advance = float(post_data.get('advance', 0))
        received = float(post_data.get('received', 0))

        total = qty * price
        net_payable = total - advance
        due = net_payable - received

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Header
        c.setFont("Helvetica-Bold", 18)
        c.drawString(200, height - 50, "EASY POS - SALES INVOICE")
        c.setLineWidth(1)
        c.line(50, height - 60, width - 50, height - 60)

        # Customer Info
        c.setFont("Helvetica", 11)
        c.drawString(50, height - 90, f"Customer Name: {cust_name}")
        c.drawString(50, height - 105, f"Phone Number: {phone}")

        # Table Header
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, height - 140, "Item Description")
        c.drawString(300, height - 140, "Qty")
        c.drawString(380, height - 140, "Price")
        c.drawString(480, height - 140, "Total")
        c.line(50, height - 148, width - 50, height - 148)

        # Content
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 170, item)
        c.drawString(300, height - 170, str(qty))
        c.drawString(380, height - 170, f"TK {price:.2f}")
        c.drawString(480, height - 170, f"TK {total:.2f}")

        # Summary Breakdown
        c.line(50, height - 190, width - 50, height - 190)
        c.setFont("Helvetica", 10)
        c.drawString(350, height - 210, f"Total Bill: TK {total:.2f}")
        c.drawString(350, height - 225, f"Advance Paid: TK {advance:.2f}")
        c.drawString(350, height - 240, f"Today Received: TK {received:.2f}")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(350, height - 260, f"Current Due: TK {due:.2f}")

        c.save()
        buffer.seek(0)

        self.send_response(200)
        self.send_header('Content-type', 'application/pdf')
        self.send_header('Content-Disposition', f'attachment; filename="Invoice_{cust_name}.pdf"')
        self.end_headers()
        self.wfile.write(buffer.getvalue())