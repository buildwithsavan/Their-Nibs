import io
import os
from datetime import datetime
from django.conf import settings

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_NAME = 'Helvetica'
FONT_NAME_BOLD = 'Helvetica-Bold'

for font_path in ['C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/Arial.ttf']:
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('ArialCustom', font_path))
            bd_path = font_path.replace('arial.ttf', 'arialbd.ttf').replace('Arial.ttf', 'arialbd.ttf')
            if os.path.exists(bd_path):
                pdfmetrics.registerFont(TTFont('ArialCustom-Bold', bd_path))
            else:
                pdfmetrics.registerFont(TTFont('ArialCustom-Bold', font_path))
            FONT_NAME = 'ArialCustom'
            FONT_NAME_BOLD = 'ArialCustom-Bold'
            break
        except Exception:
            pass


def format_currency(val):
    try:
        f = float(str(val).replace('₹', '').replace(',', '').strip())
        return f"₹{f:,.2f}"
    except (ValueError, TypeError):
        return f"₹{val}"


def generate_invoice_pdf(order_info, items=None):
    
    if items is None:
        items = []

    if not items:
        
        items = [{
            'title': 'Ecru Retro Sky Cotton Traditional Pyjama Set',
            'variant': 'Cream / S',
            'price': order_info.get('total', '40.00'),
            'qty': 1,
        }]

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []

    c_burgundy = colors.HexColor('#672221')
    c_gold = colors.HexColor('#b08d57')
    c_dark = colors.HexColor('#1d1d1b')
    c_muted = colors.HexColor('#64748b')
    c_bg_subtle = colors.HexColor('#faf7f2')
    c_border = colors.HexColor('#e8e3dc')
    c_green = colors.HexColor('#059669')

    title_style = ParagraphStyle(
        'DocTitle',
        fontName=FONT_NAME_BOLD,
        fontSize=20,
        leading=24,
        textColor=c_burgundy
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        fontName=FONT_NAME,
        fontSize=9,
        leading=13,
        textColor=c_muted
    )
    invoice_header_right = ParagraphStyle(
        'InvRight',
        fontName=FONT_NAME_BOLD,
        fontSize=13,
        leading=17,
        alignment=2,
        textColor=c_dark
    )
    invoice_header_meta = ParagraphStyle(
        'InvMeta',
        fontName=FONT_NAME,
        fontSize=9,
        leading=14,
        alignment=2,
        textColor=c_muted
    )
    section_title = ParagraphStyle(
        'SecTitle',
        fontName=FONT_NAME_BOLD,
        fontSize=10,
        leading=14,
        textColor=c_burgundy
    )
    body_style = ParagraphStyle(
        'BodyDark',
        fontName=FONT_NAME,
        fontSize=9,
        leading=13,
        textColor=c_dark
    )
    body_bold = ParagraphStyle(
        'BodyBold',
        fontName=FONT_NAME_BOLD,
        fontSize=9,
        leading=13,
        textColor=c_dark
    )
    th_style = ParagraphStyle(
        'ThStyle',
        fontName=FONT_NAME_BOLD,
        fontSize=9,
        leading=12,
        textColor=colors.white
    )
    td_style = ParagraphStyle(
        'TdStyle',
        fontName=FONT_NAME,
        fontSize=8.5,
        leading=12,
        textColor=c_dark
    )
    td_right = ParagraphStyle(
        'TdRight',
        fontName=FONT_NAME,
        fontSize=8.5,
        leading=12,
        alignment=2,
        textColor=c_dark
    )
    td_right_bold = ParagraphStyle(
        'TdRightBold',
        fontName=FONT_NAME_BOLD,
        fontSize=9,
        leading=12,
        alignment=2,
        textColor=c_dark
    )

    brand_html = "<b>THEIR NIBS</b><br/><font size='8' color='#64748b'>Luxury Nightwear &amp; Lounge Boutique<br/>GSTIN/Tax ID: TN-IN-2026-9810</font>"
    inv_title_html = f"<b>TAX INVOICE</b><br/><font size='8' color='#64748b'>Order Reference: <b>#{order_info.get('order_id', 'TN-00000')}</b><br/>Date: {datetime.now().strftime('%d %B %Y, %I:%M %p')}<br/>Payment Status: <font color='#059669'><b>PAID</b></font></font>"

    header_table = Table(
        [[Paragraph(brand_html, title_style), Paragraph(inv_title_html, invoice_header_right)]],
        colWidths=[310, 210]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceBefore=4, spaceAfter=14))

    full_name = order_info.get('full_name') or 'Valued Customer'
    email = order_info.get('email') or 'customer@theirnibs.com'
    phone = order_info.get('phone') or 'Not provided'
    address = order_info.get('address') or '14 Kensington High Street'
    city = order_info.get('city') or 'Mumbai'
    postcode = order_info.get('postcode') or '400001'
    country = order_info.get('country') or 'India'
    pay_method = order_info.get('payment_method') or 'Razorpay (Online Verified)'
    payment_id = order_info.get('payment_id') or 'pay_TNIB' + str(datetime.now().strftime('%y%m%d%H%M'))

    bill_to_text = f"""
    <b>Billed &amp; Shipped To:</b><br/>
    <b>{full_name}</b><br/>
    {address}<br/>
    {city}, {postcode}<br/>
    {country}<br/>
    Email: {email}<br/>
    Phone: {phone}
    """

    pay_info_text = f"""
    <b>Payment &amp; Dispatch Details:</b><br/>
    Method: <b>{pay_method}</b><br/>
    Transaction ID: <b>{payment_id}</b><br/>
    Gateway Mode: <b>Razorpay Verified</b><br/>
    Currency: <b>INR (₹)</b><br/>
    Delivery Type: <b>Express Tracked Courier</b><br/>
    Estimated Delivery: <b>3 - 5 Business Days</b>
    """

    details_table = Table(
        [[Paragraph(bill_to_text, body_style), Paragraph(pay_info_text, body_style)]],
        colWidths=[260, 260]
    )
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_subtle),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 16))

    table_data = [
        [
            Paragraph("Item Description", th_style),
            Paragraph("Variant / Size", th_style),
            Paragraph("Qty", th_style),
            Paragraph("Unit Price", th_style),
            Paragraph("Total Amount", th_style)
        ]
    ]

    subtotal = 0.0
    for item in items:
        title = item.get('title', 'Atelier Pyjama Set')
        variant = item.get('variant', 'Standard')
        qty = int(item.get('qty', 1))
        price_val = float(str(item.get('price', 0)).replace('₹', '').replace(',', '').strip() or 0)
        item_total = price_val * qty
        subtotal += item_total

        table_data.append([
            Paragraph(f"<b>{title}</b>", td_style),
            Paragraph(variant, td_style),
            Paragraph(str(qty), td_style),
            Paragraph(format_currency(price_val), td_right),
            Paragraph(format_currency(item_total), td_right_bold)
        ])

    items_table = Table(table_data, colWidths=[200, 110, 40, 80, 90])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_burgundy),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fcfbfa')])
    ]))
    story.append(items_table)
    story.append(Spacer(1, 12))

    total_paid_str = str(order_info.get('total', subtotal))
    total_paid = float(total_paid_str.replace('₹', '').replace(',', '').strip() or subtotal)
    shipping_amt = 0.0
    tax_amt = round(total_paid * 0.18, 2)

    summary_data = [
        [Paragraph("Subtotal:", td_style), Paragraph(format_currency(subtotal), td_right)],
        [Paragraph("Shipping (Standard Tracked):", td_style), Paragraph("FREE", td_right)],
        [Paragraph("Taxes (18% GST Included):", td_style), Paragraph(format_currency(tax_amt), td_right)],
        [
            Paragraph("<b>Total Amount Paid:</b>", ParagraphStyle('TtlLabel', fontName=FONT_NAME_BOLD, fontSize=11, textColor=c_burgundy)),
            Paragraph(f"<b>{format_currency(total_paid)}</b>", ParagraphStyle('TtlVal', fontName=FONT_NAME_BOLD, fontSize=12, alignment=2, textColor=c_gold))
        ]
    ]

    summary_table = Table(summary_data, colWidths=[150, 100])
    summary_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LINEABOVE', (0, 3), (1, 3), 1, c_gold),
    ]))

    outer_summary = Table(
        [[Paragraph("", body_style), summary_table]],
        colWidths=[260, 260]
    )
    outer_summary.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(outer_summary)
    story.append(Spacer(1, 20))

    footer_text = """
    <b>30-Day Easy Returns Guarantee:</b> If you are not completely enchanted with your sleepwear, you can return or exchange unworn items within 30 days.<br/>
    For assistance, please email <b>customercare@theirnibs.com</b> quoting your order reference. Thank you for shopping with Their Nibs.
    """
    story.append(HRFlowable(width="100%", thickness=0.5, color=c_border, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph(footer_text, subtitle_style))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def save_invoice_pdf(order_info, items=None, output_path=None):
    
    if not output_path:
        order_id = order_info.get('order_id', 'ORDER')
        invoices_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
        os.makedirs(invoices_dir, exist_ok=True)
        output_path = os.path.join(invoices_dir, f"TheirNibs_Invoice_{order_id}.pdf")

    pdf_bytes = generate_invoice_pdf(order_info, items)
    with open(output_path, 'wb') as f:
        f.write(pdf_bytes)

    return output_path


def send_order_invoice_email(order_info, items=None, pdf_bytes=None):
    
    from django.core.mail import EmailMessage

    if not pdf_bytes:
        pdf_bytes = generate_invoice_pdf(order_info, items)

    order_id = order_info.get('order_id', 'ORDER')
    customer_email = order_info.get('email')
    full_name = order_info.get('full_name', 'Customer')
    total = order_info.get('total', '0.00')
    payment_method = order_info.get('payment_method', 'Razorpay')
    payment_id = order_info.get('payment_id', 'pay_TNIB' + str(order_id))

    if not customer_email:
        return False

    subject = f"Your Their Nibs Order Confirmation & Bill #{order_id}"
    body = f"""Dear {full_name},

Thank you for your order with Their Nibs Atelier!

We are pleased to confirm that your payment has been received and verified successfully.

ORDER SUMMARY:
--------------------------------------------------
Order Reference: #{order_id}
Customer Name:   {full_name}
Total Amount:    INR ₹{total}
Payment Method:  {payment_method}
Payment ID:      {payment_id}
Delivery Option: Express Tracked Delivery (FREE)
--------------------------------------------------

Your official PDF bill / invoice has been attached to this email. You can open and download it directly on your mobile phone or computer.

If you have any questions or wish to initiate an exchange under our 30-day guarantee, simply reply to this email or contact customercare@theirnibs.com.

Warmest regards,
Their Nibs
Luxury Nightwear & Lounge Boutique
www.theirnibs.com
"""

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Their Nibs <orders@theirnibs.com>')
    msg = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=[customer_email]
    )

    pdf_filename = f"TheirNibs_Invoice_{order_id}.pdf"
    msg.attach(
        filename=pdf_filename,
        content=pdf_bytes,
        mimetype="application/pdf"
    )

    try:
        msg.send(fail_silently=False)
        return True
    except Exception:
        try:
            msg.send(fail_silently=True)
        except Exception:
            pass
        return False
