"""
PDF Export Module for EchoWorld Nexus
Generates financial roadmap PDFs
"""

import io
from datetime import datetime
from typing import Dict, Any, List
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    Image, PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


def generate_financial_roadmap_pdf(
    country: str,
    city: str,
    user_salary: float,
    user_savings: float,
    vtc_summary: Dict[str, Any],
    monte_carlo_results: Dict[str, Any],
    sim_feed: List[Dict[str, Any]],
    recommendations: List[str]
) -> bytes:
    """
    Generate a comprehensive financial roadmap PDF
    
    Returns:
        PDF file as bytes
    """
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        rightMargin=1*cm,
        leftMargin=1*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1a365d')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.HexColor('#2d3748')
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        textColor=colors.HexColor('#4a5568')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=8,
        leading=14
    )
    
    story = []
    
    story.append(Paragraph("EchoWorld Nexus", title_style))
    story.append(Paragraph("Financial Roadmap Report", heading_style))
    story.append(Spacer(1, 10))
    
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#3182ce')))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(f"Destination: {city}, {country}", body_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}", body_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Executive Summary", heading_style))
    
    top_path = monte_carlo_results.get("top_paths", [{}])[0] if monte_carlo_results else {}
    success_prob = top_path.get("approval_prob", 0.75) * 100
    
    summary_data = [
        ["Metric", "Value", "Status"],
        ["Expected Salary", f"€{user_salary:,.0f}/month", "✓"],
        ["Current Savings", f"€{user_savings:,.0f}", "✓" if user_savings >= 5000 else "⚠"],
        ["VTC Approval Rate", f"{vtc_summary.get('approval_rate', 0):.0f}%", "✓" if vtc_summary.get('approval_rate', 0) >= 70 else "⚠"],
        ["Success Probability", f"{success_prob:.0f}%", "✓" if success_prob >= 70 else "⚠"],
        ["Recommended Path", top_path.get("path_name", "Balanced Growth"), "→"]
    ]
    
    summary_table = Table(summary_data, colWidths=[5*cm, 5*cm, 2*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3182ce')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("VTC Simulation Results", heading_style))
    story.append(Paragraph(
        f"Your Visa Transaction Controls simulation analyzed {vtc_summary.get('total_transactions', 0)} transactions.",
        body_style
    ))
    
    vtc_data = [
        ["Category", "Approved", "Declined", "Savings Impact"],
    ]
    
    for category, data in vtc_summary.get("category_breakdown", {}).items():
        vtc_data.append([
            category.capitalize(),
            f"€{data.get('approved', 0):,.0f}",
            f"€{data.get('declined', 0):,.0f}",
            f"€{data.get('declined', 0):,.0f}"
        ])
    
    if len(vtc_data) > 1:
        vtc_table = Table(vtc_data, colWidths=[4*cm, 3*cm, 3*cm, 3*cm])
        vtc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#48bb78')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fff4')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#c6f6d5'))
        ]))
        story.append(vtc_table)
    
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Alternative Financial Paths", heading_style))
    
    paths = monte_carlo_results.get("top_paths", [])
    for i, path in enumerate(paths[:3], 1):
        story.append(Paragraph(f"Path {i}: {path.get('path_name', 'Unknown')}", subheading_style))
        story.append(Paragraph(f"• Description: {path.get('path_description', 'N/A')}", body_style))
        story.append(Paragraph(f"• Success Probability: {path.get('approval_prob', 0)*100:.0f}%", body_style))
        story.append(Paragraph(f"• Projected Monthly Savings: €{path.get('monthly_savings', 0):,.0f}", body_style))
        story.append(Paragraph(f"• 12-Month Projection: €{path.get('total_savings_12m', 0):,.0f}", body_style))
        story.append(Spacer(1, 10))
    
    story.append(Paragraph("Key Recommendations", heading_style))
    
    for i, rec in enumerate(recommendations[:5], 1):
        story.append(Paragraph(f"{i}. {rec}", body_style))
    
    story.append(Spacer(1, 30))
    
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e0')))
    story.append(Spacer(1, 10))
    
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#718096'),
        alignment=TA_CENTER
    )
    
    story.append(Paragraph(
        "DISCLAIMER: This report is generated by EchoWorld Nexus Financial Guardian Simulator. "
        "All projections are estimates based on simulated data. This does not constitute financial advice. "
        "Consult qualified financial advisors before making relocation decisions.",
        disclaimer_style
    ))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Powered by EchoWorld Nexus | AI Financial Guardian for Global Mobility",
        disclaimer_style
    ))
    
    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def get_pdf_filename(country: str, city: str) -> str:
    """Generate a filename for the PDF"""
    date_str = datetime.now().strftime('%Y%m%d')
    return f"EchoWorld_Roadmap_{city}_{country}_{date_str}.pdf"
