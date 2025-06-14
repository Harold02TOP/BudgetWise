from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_pdf_report(month: str, budget_amount: float, transactions: list, filename: str):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(f"Budget Report for {month}", styles['Heading1']))
    elements.append(Spacer(1, 12))

    # Budget Summary
    elements.append(Paragraph(f"Budget: ${budget_amount:.2f}", styles['Normal']))
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    balance = total_income - total_expense
    elements.append(Paragraph(f"Total Income: ${total_income:.2f}", styles['Normal']))
    elements.append(Paragraph(f"Total Expenses: ${total_expense:.2f}", styles['Normal']))
    elements.append(Paragraph(f"Balance: ${balance:.2f}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Transactions Table
    data = [["Date", "Type", "Amount", "Category", "Tags"]]
    for t in transactions:
        data.append([t.date.split('T')[0], t.type.capitalize(), f"${t.amount:.2f}", t.category, t.tags or ""])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    # Build PDF
    doc.build(elements)