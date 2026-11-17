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

    # Custom Color Palette
    PRIMARY = colors.HexColor("#0F172A")        # Dark Slate
    ACCENT_CYAN = colors.HexColor("#11A9F6")    # Deep Cyan
    ACCENT_PURPLE = colors.HexColor("#7C3AED")  # Electric Purple
    BG_LIGHT = colors.HexColor("#F8FAFC")       # Off White
    TEXT_DARK = colors.HexColor("#1E293B")      # Charcoal Body Text
    TEXT_MUTED = colors.HexColor("#64748B")     # Muted Subtitles
    BORDER_COLOR = colors.HexColor("#D6DAE0")   # Border

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=TEXT_MUTED,
        spaceAfter=15
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=ACCENT_CYAN,
        spaceBefore=14,
        spaceAfter=8
    )

    h3_style = ParagraphStyle(
        'Heading3Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=TEXT_DARK,
        spaceAfter=6
    )

    bold_body_style = ParagraphStyle(
        'BoldBodyCustom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=TEXT_DARK
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # Document Header
    story.append(Paragraph("EventHub — Architecture & User Flow Guide", title_style))
    story.append(Paragraph("Complete visual reference for system workflow, role permissions, and code architecture", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT_CYAN, spaceAfter=15))

    # 1. System Overview
    story.append(Paragraph("1. System Architecture Overview", h2_style))
    story.append(Paragraph(
        "EventHub is built on Django with an SQLite database and a responsive CSS design system. "
        "HTTP requests from client browsers are routed through Django <b>urls.py</b>, processed by <b>views.py</b>, "
        "persisted in <b>db.sqlite3</b> via Django ORM, and rendered via dynamic HTML5 templates.", body_style
    ))
    story.append(Spacer(1, 10))

    # 2. User Roles Matrix Table
    story.append(Paragraph("2. User Role & Capability Matrix", h2_style))
    
    role_data = [
        [
            Paragraph("Role", table_header_style),
            Paragraph("Demo Login", table_header_style),
            Paragraph("Browse & Search", table_header_style),
            Paragraph("Reserve Tickets", table_header_style),
            Paragraph("Host New Events", table_header_style),
            Paragraph("Manage Own Events", table_header_style),
            Paragraph("Admin Panel", table_header_style)
        ],
        [
            Paragraph("Guest / Visitor", table_cell_bold),
            Paragraph("N/A", table_cell_style),
            Paragraph("YES", table_cell_style),
            Paragraph("NO", table_cell_style),
            Paragraph("NO", table_cell_style),
            Paragraph("NO", table_cell_style),
            Paragraph("NO", table_cell_style)
        ],
        [
            Paragraph("Attendee", table_cell_bold),
            Paragraph("alex_dev / demo123", table_cell_style),
            Paragraph("YES", table_cell_style),
            Paragraph("YES", table_cell_style),
            Paragraph("NO", table_cell_style),
            Paragraph("NO", table_cell_style),
            Paragraph("NO", table_cell_style)
        ],
        [
            Paragraph("Organizer", table_cell_bold),
            Paragraph("sarah_organizer / demo123", table_cell_style),
            Paragraph("YES", table_cell_style),
            Paragraph("YES", table_cell_style),
            Paragraph("YES", table_cell_style),
            Paragraph("YES", table_cell_style),
            Paragraph("NO", table_cell_style)
        ],
        [
            Paragraph("Superuser / Admin", table_cell_bold),
            Paragraph("admin / admin123", table_cell_style),
            Paragraph("YES", table_cell_style),
            Paragraph("YES", table_cell_style),
            Paragraph("YES", table_cell_style),
            Paragraph("YES (All)", table_cell_style),
            Paragraph("YES (/admin/)", table_cell_style)
        ]
    ]

    col_widths = [85, 115, 65, 65, 65, 75, 70]
    t = Table(role_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # 3. User Workflows
    story.append(Paragraph("3. Step-by-Step User Workflows", h2_style))

    # Workflow 1
    story.append(Paragraph("A. Event Discovery & Search Workflow", h3_style))
    story.append(Paragraph("<b>1. Visit Homepage:</b> Open http://127.0.0.1:8000/ to view the live event grid.", body_style))
    story.append(Paragraph("<b>2. Search Bar:</b> Enter title, description, or location keywords in the search field.", body_style))
    story.append(Paragraph("<b>3. Category Pills:</b> Filter events by Technology, Design & UX, Music & Arts, or Business.", body_style))
    story.append(Paragraph("<b>4. Time Filter:</b> Filter by Upcoming, Past Events, or All Events.", body_style))
    story.append(Spacer(1, 8))

    # Workflow 2
    story.append(Paragraph("B. Ticket Registration & RSVP Workflow (Attendee)", h3_style))
    story.append(Paragraph("<b>1. Log In:</b> Log in as <i>alex_dev</i> (password: <i>demo123</i>).", body_style))
    story.append(Paragraph("<b>2. Select Event:</b> Click <i>'Details'</i> on any upcoming event card.", body_style))
    story.append(Paragraph("<b>3. Reserve Pass:</b> Select ticket quantity (1–5 tickets) and click <i>'Confirm RSVP'</i>.", body_style))
    story.append(Paragraph("<b>4. Real-time Update:</b> Event seat availability decrements immediately, and ticket displays on user Dashboard.", body_style))
    story.append(Spacer(1, 8))

    # Workflow 3
    story.append(Paragraph("C. Host & Manage Events Workflow (Organizer)", h3_style))
    story.append(Paragraph("<b>1. Log In:</b> Log in as <i>sarah_organizer</i> (password: <i>demo123</i>).", body_style))
    story.append(Paragraph("<b>2. Click Create Event:</b> Access <i>'+ Create Event'</i> from top navigation bar.", body_style))
    story.append(Paragraph("<b>3. Submit Form:</b> Fill out Title, Category, Location, Start/End Datetime, Capacity, and Banner URL.", body_style))
    story.append(Paragraph("<b>4. Organizer Dashboard:</b> View live seat occupancy metrics, edit details, or delete hosted events.", body_style))
    story.append(Spacer(1, 14))

    # 4. Directory Map
    story.append(Paragraph("4. Project Directory & Code Map", h2_style))

    code_map_data = [
        [Paragraph("File Path", table_header_style), Paragraph("Component Purpose", table_header_style)],
        [Paragraph("events/models.py", table_cell_bold), Paragraph("Data Schemas: UserProfile, Category, Event, and Registration", table_cell_style)],
        [Paragraph("events/views.py", table_cell_bold), Paragraph("Logic Handlers: event_list, event_detail, event_create, RSVP & Dashboard", table_cell_style)],
        [Paragraph("events/forms.py", table_cell_bold), Paragraph("Form definitions: SignUpForm (Role selection), EventForm, RegistrationForm", table_cell_style)],
        [Paragraph("events/urls.py", table_cell_bold), Paragraph("URL Routes mapping requests to view functions", table_cell_style)],
        [Paragraph("static/css/style.css", table_cell_bold), Paragraph("Design System: Cyberpunk Neon & Playful styling, animations, transitions", table_cell_style)],
        [Paragraph("templates/events/", table_cell_bold), Paragraph("HTML5 templates for Event list, details, forms, and Dashboard", table_cell_style)],
        [Paragraph("seed.py", table_cell_bold), Paragraph("Initial database population script for users, categories, and events", table_cell_style)],
    ]

    t_map = Table(code_map_data, colWidths=[140, 390])
    t_map.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_map)

    # Footer Note
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR, spaceAfter=8))
    story.append(Paragraph("Generated automatically for EventHub Management Application © 2026", subtitle_style))

    doc.build(story)
    print(f"Successfully generated PDF: {filename}")

if __name__ == '__main__':
    # Save to workspace root
    build_pdf(r"c:\Users\Lenovo\OneDrive\Desktop\Pavithra\EventHub_User_Flow_Guide.pdf")
    # Save copy to artifacts directory
    artifact_path = r"C:\Users\Lenovo\.gemini\antigravity-ide\brain\37ecec4f-4dfe-44b9-af46-658e3d9b51a0\EventHub_User_Flow_Guide.pdf"
    build_pdf(artifact_path)
