from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import io
from datetime import datetime


def generate_pdf(cr_text: str, patient_name: str = "", doctor_name: str = "", specialty: str = "") -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'Title',
        parent=styles['Normal'],
        fontSize=14,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1e3a5f'),
        spaceAfter=4,
        alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        textColor=colors.HexColor('#555555'),
        spaceAfter=2,
        alignment=TA_CENTER
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        leading=16,
        spaceAfter=6,
        textColor=colors.black
    )

    story = []

    # Header
    story.append(Paragraph(f"Dr. {doctor_name}" if doctor_name else "Dr. ________________", title_style))
    story.append(Paragraph(specialty if specialty else "Médecin", subtitle_style))
    story.append(Paragraph(f"Date : {datetime.now().strftime('%d/%m/%Y')}", subtitle_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1e3a5f')))
    story.append(Spacer(1, 0.3*cm))

    if patient_name:
        story.append(Paragraph(f"<b>Patient :</b> {patient_name}", body_style))
        story.append(Spacer(1, 0.2*cm))

    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 0.4*cm))

    # CR content
    for line in cr_text.split('\n'):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 0.2*cm))
            continue
        # Bold section headers (lines ending with : or starting with **)
        if line.endswith(':') or (line.startswith('**') and line.endswith('**')):
            clean = line.replace('**', '').rstrip(':')
            story.append(Paragraph(f"<b>{clean} :</b>", body_style))
        elif line.startswith('##'):
            clean = line.replace('#', '').strip()
            story.append(Paragraph(f"<b><u>{clean}</u></b>", body_style))
        elif line.startswith('-') or line.startswith('•'):
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;{line}", body_style))
        else:
            story.append(Paragraph(line, body_style))

    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(f"Généré via ClinIA — {datetime.now().strftime('%d/%m/%Y à %H:%M')}", subtitle_style))

    doc.build(story)
    return buffer.getvalue()
