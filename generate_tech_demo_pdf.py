import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY = colors.HexColor("#0F172A")        # Dark Slate
    ACCENT_CYAN = colors.HexColor("#0284C7")    # Deep Cyan
    ACCENT_PURPLE = colors.HexColor("#7C3AED")  # Electric Purple
    BG_LIGHT = colors.HexColor("#F8FAFC")       # Off White
    TEXT_DARK = colors.HexColor("#1E293B")      # Charcoal Body Text
    TEXT_MUTED = colors.HexColor("#64748B")     # Muted Subtitles
    BORDER_COLOR = colors.HexColor("#CBD5E1")   # Border

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=PRIMARY,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=TEXT_MUTED,
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=ACCENT_CYAN,
        spaceBefore=12,
        spaceAfter=6
    )

    h3_style = ParagraphStyle(
        'Heading3Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=PRIMARY,
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        spaceAfter=5
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("EventHub — Technical Stack & Demo Presentation Guide", title_style))
    story.append(Paragraph("Technical specifications, database models, algorithms, and talking points for project demonstration", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT_CYAN, spaceAfter=12))

    # 1. Tech Stack Overview Table
    story.append(Paragraph("1. Technology Stack Specifications", h2_style))
    
    stack_data = [
        [Paragraph("Category", table_header_style), Paragraph("Technology Used", table_header_style), Paragraph("Technical Purpose & Implementation", table_header_style)],
        [Paragraph("Backend Framework", table_cell_bold), Paragraph("Python 3.11 + Django 5.2", table_cell_style), Paragraph("Model-View-Template (MVT) web architecture handling routing, views & auth.", table_cell_style)],
        [Paragraph("Database & ORM", table_cell_bold), Paragraph("SQLite3 + Django ORM", table_cell_style), Paragraph("Relational database with auto-computed properties & SQL query optimization.", table_cell_style)],
        [Paragraph("Frontend Stack", table_cell_bold), Paragraph("HTML5 + Vanilla CSS3", table_cell_style), Paragraph("Semantic HTML5 structure styled with CSS Grid, Flexbox & custom properties.", table_cell_style)],
        [Paragraph("Design System", table_cell_bold), Paragraph("Cyberpunk Neon Theme", table_cell_style), Paragraph("Dark glass backdrop blurs, glow shadows, CSS keyframes & smooth transitions.", table_cell_style)],
        [Paragraph("Authentication", table_cell_bold), Paragraph("Django Auth Engine", table_cell_style), Paragraph("Session-based authentication with PBKDF2/SHA256 password hashing.", table_cell_style)],
        [Paragraph("Icons & Fonts", table_cell_bold), Paragraph("Font Awesome + Google Fonts", table_cell_style), Paragraph("Vector icons with Space Grotesk & Plus Jakarta Sans typography.", table_cell_style)]
    ]

    t_stack = Table(stack_data, colWidths=[110, 140, 290])
    t_stack.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_stack)
    story.append(Spacer(1, 10))

    # 2. Database Models
    story.append(Paragraph("2. Database Schema & Models (`events/models.py`)", h2_style))
    story.append(Paragraph("<b>• UserProfile (Extension):</b> OneToOne link to User. Stores <code>role</code> ('ATTENDEE' vs 'ORGANIZER') to enforce RBAC.", body_style))
    story.append(Paragraph("<b>• Category:</b> Organizes events with auto-slugification and custom Font Awesome icons.", body_style))
    story.append(Paragraph("<b>• Event:</b> Primary entity with title, slug, venue, start/end datetimes, capacity, and image URL.", body_style))
    story.append(Paragraph("<b>• Dynamic ORM Properties:</b> <code>registered_count</code>, <code>seats_available</code>, <code>is_full</code>, <code>is_past</code>, and <code>occupancy_percentage</code> calculate metrics live without DB redundancy.", body_style))
    story.append(Paragraph("<b>• Registration:</b> Foreign key junction between User and Event with <code>unique_together</code> constraint to prevent duplicate tickets.", body_style))
    story.append(Spacer(1, 10))

    # 3. Core Algorithms & Logic
    story.append(Paragraph("3. Technical Algorithms & Security Mechanics", h2_style))
    story.append(Paragraph("<b>1. Role-Based Access Control (RBAC):</b> View-level security decorators check <code>request.user.profile.is_organizer</code> before granting access to <code>/event/create/</code>.", body_style))
    story.append(Paragraph("<b>2. Overbooking Prevention Engine:</b> Validates requested ticket quantity against <code>event.seats_available</code> prior to committing registration SQL transactions.", body_style))
    story.append(Paragraph("<b>3. Multi-Parametric Search (Django Q Objects):</b> Combines title, description, and location filters using <code>Q(title__icontains=...) | Q(...)</code> alongside category & time filters.", body_style))
    story.append(Paragraph("<b>4. Custom Form Validation:</b> Form level <code>clean()</code> method guarantees <code>end_time > start_time</code>.", body_style))
    story.append(Paragraph("<b>5. Automated Seeding Script (`seed.py`):</b> Programmatically initializes admin accounts, demo organizer/attendees, categories, and initial events.", body_style))
    story.append(Spacer(1, 10))

    # 4. Presentation & Demo Talking Points
    story.append(Paragraph("4. Live Project Demonstration Talking Points", h2_style))
    
    demo_points = [
        [Paragraph("Demo Action", table_header_style), Paragraph("Key Technical Concept to Highlight", table_header_style)],
        [Paragraph("1. Log in as alex_dev (Attendee)", table_cell_bold), Paragraph("Show that '+ Create Event' is hidden and RBAC permission checks are active.", table_cell_style)],
        [Paragraph("2. Reserve 2 Tickets on an Event", table_cell_bold), Paragraph("Demonstrate real-time seat availability deduction & occupancy progress meter update.", table_cell_style)],
        [Paragraph("3. Log in as sarah_organizer", table_cell_bold), Paragraph("Show Organizer Dashboard featuring 'Events You Organize' & ticket management.", table_cell_style)],
        [Paragraph("4. Host a New Event", table_cell_bold), Paragraph("Demonstrate EventForm datetime-local inputs, auto-slugification & immediate live grid rendering.", table_cell_style)],
        [Paragraph("5. Filter by Category & Search 'AI'", table_cell_bold), Paragraph("Explain Django ORM Q object multi-filtering queries in views.py.", table_cell_style)]
    ]

    t_demo = Table(demo_points, colWidths=[160, 380])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_demo)

    # Footer
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR, spaceAfter=6))
    story.append(Paragraph("EventHub Project Demo Sheet — Created for Project Presentation & Evaluation © 2026", subtitle_style))

    doc.build(story)
    print(f"Successfully generated Technical PDF: {filename}")

if __name__ == '__main__':
    # Save to workspace root
    build_pdf(r"c:\Users\Lenovo\OneDrive\Desktop\Pavithra\EventHub_Technical_Demo_Presentation.pdf")
    # Save copy to artifacts directory
    artifact_path = r"C:\Users\Lenovo\.gemini\antigravity-ide\brain\37ecec4f-4dfe-44b9-af46-658e3d9b51a0\EventHub_Technical_Demo_Presentation.pdf"
    build_pdf(artifact_path)
