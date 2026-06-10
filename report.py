from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def export_pdf(tree, filename="PCB_Report.pdf"):
    doc = SimpleDocTemplate(filename)
    elements = []
    styles = getSampleStyleSheet()

    for row in tree.get_children():
        values = tree.item(row)["values"]
        text = " | ".join(str(v) for v in values)
        elements.append(Paragraph(text, styles["Normal"]))
        elements.append(Spacer(1, 6))

    doc.build(elements)