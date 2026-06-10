from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def export_pdf(results, summary, filename):

    doc = SimpleDocTemplate(filename)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("PCB Validation Report", styles["Heading1"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        f"CRITICAL: {summary['CRITICAL']} | "
        f"WARNING: {summary['WARNING']} | "
        f"INFO: {summary['INFO']}",
        styles["Normal"]
    ))

    for r in results:
        elements.append(Paragraph(
            f"{r['rule']} - {r['status']} - {r['severity']} - {r['message']}",
            styles["Normal"]
        ))

    doc.build(elements)