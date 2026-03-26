#!/usr/bin/env python3
"""
Generate a visually appealing PDF from codebase-analysis.md
Uses reportlab for PDF generation with custom styling.
"""

import re
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


# Color scheme - Professional and accessible
COLORS = {
    'primary': colors.HexColor('#2563EB'),
    'secondary': colors.HexColor('#10B981'),
    'accent': colors.HexColor('#F59E0B'),
    'dark': colors.HexColor('#1F2937'),
    'light': colors.HexColor('#F3F4F6'),
    'code_bg': colors.HexColor('#F1F5F9'),
    'heading1': colors.HexColor('#1E40AF'),
    'heading2': colors.HexColor('#059669'),
    'heading3': colors.HexColor('#B45309'),
    'table_header': colors.HexColor('#3B82F6'),
    'table_row_even': colors.HexColor('#F9FAFB'),
    'table_row_odd': colors.HexColor('#FFFFFF'),
}


def create_styles():
    """Create custom paragraph styles."""
    styles = getSampleStyleSheet()

    # Title
    styles.add(ParagraphStyle(
        name='CustomTitle',
        fontSize=26,
        textColor=COLORS['heading1'],
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))

    # Subtitle/meta info
    styles.add(ParagraphStyle(
        name='Meta',
        fontSize=10,
        textColor=COLORS['dark'],
        spaceAfter=15,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    ))

    # H1
    styles.add(ParagraphStyle(
        name='H1',
        fontSize=18,
        textColor=COLORS['heading1'],
        spaceBefore=20,
        spaceAfter=12,
        fontName='Helvetica-Bold',
    ))

    # H2
    styles.add(ParagraphStyle(
        name='H2',
        fontSize=14,
        textColor=COLORS['heading2'],
        spaceBefore=15,
        spaceAfter=8,
        fontName='Helvetica-Bold',
    ))

    # H3
    styles.add(ParagraphStyle(
        name='H3',
        fontSize=12,
        textColor=COLORS['heading3'],
        spaceBefore=10,
        spaceAfter=6,
        fontName='Helvetica-Bold',
    ))

    # H4
    styles.add(ParagraphStyle(
        name='H4',
        fontSize=11,
        textColor=COLORS['dark'],
        spaceBefore=8,
        spaceAfter=4,
        fontName='Helvetica-Bold',
    ))

    # Body text
    styles.add(ParagraphStyle(
        name='Body',
        fontSize=10,
        textColor=COLORS['dark'],
        spaceBefore=3,
        spaceAfter=6,
        fontName='Helvetica',
        leading=14,
    ))

    # Code block
    styles.add(ParagraphStyle(
        name='CodeBlock',
        fontSize=9,
        textColor=COLORS['dark'],
        backColor=COLORS['code_bg'],
        spaceBefore=6,
        spaceAfter=6,
        fontName='Courier',
        leftIndent=10,
        rightIndent=10,
        leading=12,
    ))

    # Bullet
    styles.add(ParagraphStyle(
        name='MyBullet',
        fontSize=10,
        textColor=COLORS['dark'],
        spaceBefore=2,
        spaceAfter=2,
        fontName='Helvetica',
        leftIndent=20,
        bulletIndent=10,
        leading=13,
    ))

    # Numbered item
    styles.add(ParagraphStyle(
        name='Numbered',
        fontSize=10,
        textColor=COLORS['dark'],
        spaceBefore=2,
        spaceAfter=2,
        fontName='Helvetica',
        leftIndent=20,
        leading=13,
    ))

    # Table cell
    styles.add(ParagraphStyle(
        name='TableCell',
        fontSize=9,
        textColor=COLORS['dark'],
        fontName='Helvetica',
        leading=11,
    ))

    # Table header cell
    styles.add(ParagraphStyle(
        name='HeaderCell',
        fontSize=9,
        textColor=colors.white,
        fontName='Helvetica-Bold',
        leading=11,
    ))

    return styles


def escape_xml(text):
    """Escape special XML characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


def process_formatting(text):
    """
    Process markdown formatting for reportlab.
    Handles: **bold**, *italic*, `code`
    """
    # First escape XML special chars
    text = escape_xml(text)

    # Then apply formatting using reportlab's XML tags
    # **bold** -> <b>bold</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # *italic* -> <i>italic</i> (but not ** which is bold)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    # `code` -> <font name="Courier" color="#2563EB">code</font>
    text = re.sub(r'`(.+?)`', r'<font name="Courier" color="#2563EB">\1</font>', text)

    return text


def parse_markdown(content):
    """Parse markdown into structured blocks."""
    blocks = []
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        # Skip empty lines
        if not line.strip():
            i += 1
            continue

        # H1
        if line.startswith('# ') and not line.startswith('## '):
            blocks.append(('h1', line[2:].strip()))
            i += 1
        # H2
        elif line.startswith('## ') and not line.startswith('### '):
            blocks.append(('h2', line[3:].strip()))
            i += 1
        # H3
        elif line.startswith('### ') and not line.startswith('#### '):
            blocks.append(('h3', line[4:].strip()))
            i += 1
        # H4
        elif line.startswith('#### '):
            blocks.append(('h4', line[5:].strip()))
            i += 1
        # Code block
        elif line.startswith('```'):
            lang = line[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # Skip closing fence
            blocks.append(('code', '\n'.join(code_lines), lang))
        # Table
        elif line.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            blocks.append(('table', table_lines))
        # Horizontal rule
        elif line.strip() == '---':
            blocks.append(('hr', None))
            i += 1
        # Bullet
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            text = line.strip()[2:]
            blocks.append(('bullet', text))
            i += 1
        # Numbered list
        elif re.match(r'^\s*\d+\.\s', line):
            match = re.match(r'^\s*(\d+)\.\s+(.+)$', line)
            if match:
                blocks.append(('numbered', match.group(2), int(match.group(1))))
            i += 1
        # Regular paragraph
        else:
            para_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith('#') and not lines[i].startswith('|') and not lines[i].startswith('-') and not lines[i].startswith('*') and not re.match(r'^\s*\d+\.\s', lines[i]) and lines[i].strip() != '---':
                para_lines.append(lines[i].strip())
                i += 1
            blocks.append(('para', ' '.join(para_lines)))

    return blocks


def build_table(table_lines, styles):
    """Build a reportlab table from markdown table lines."""
    # Filter separator lines
    data_lines = [l for l in table_lines if not re.match(r'^\|[-:\s|]+\|$', l)]

    if not data_lines:
        return None

    # Parse cells
    rows = []
    for line in data_lines:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        rows.append(cells)

    if not rows:
        return None

    # Create table data with Paragraphs
    table_data = []
    for row_idx, row in enumerate(rows):
        row_paras = []
        for cell in row:
            cell_text = process_formatting(cell)
            try:
                if row_idx == 0:
                    para = Paragraph(cell_text, styles['HeaderCell'])
                else:
                    para = Paragraph(cell_text, styles['TableCell'])
                row_paras.append(para)
            except:
                row_paras.append(cell)
        table_data.append(row_paras)

    # Calculate column widths
    num_cols = len(rows[0])
    available_width = 7 * inch
    col_width = available_width / num_cols

    # Create table
    table = Table(table_data, colWidths=[col_width] * num_cols)

    # Style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['table_header']),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLORS['table_row_odd'], COLORS['table_row_even']]),
    ])
    table.setStyle(style)

    return table


def build_pdf(content, output_path):
    """Build the PDF document."""
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    styles = create_styles()
    story = []

    blocks = parse_markdown(content)
    page_break_next = False

    for block in blocks:
        block_type = block[0]

        # Handle page break before H1
        if block_type == 'h1':
            if page_break_next:
                story.append(PageBreak())
            page_break_next = True
            story.append(Paragraph(block[1], styles['CustomTitle']))
            story.append(HRFlowable(width="80%", thickness=2, color=COLORS['primary'], spaceAfter=15))

        elif block_type == 'h2':
            story.append(Spacer(1, 10))
            story.append(Paragraph(block[1], styles['H2']))

        elif block_type == 'h3':
            story.append(Paragraph(block[1], styles['H3']))

        elif block_type == 'h4':
            story.append(Paragraph(block[1], styles['H4']))

        elif block_type == 'para':
            text = process_formatting(block[1])
            try:
                story.append(Paragraph(text, styles['Body']))
            except:
                # Fallback for problematic text
                story.append(Paragraph(escape_xml(block[1]), styles['Body']))

        elif block_type == 'bullet':
            text = process_formatting(block[1])
            try:
                story.append(Paragraph(f"&bull; {text}", styles['MyBullet']))
            except:
                story.append(Paragraph(f"&bull; {escape_xml(block[1])}", styles['MyBullet']))

        elif block_type == 'numbered':
            text = process_formatting(block[1])
            num = block[2]
            try:
                story.append(Paragraph(f"{num}. {text}", styles['Numbered']))
            except:
                story.append(Paragraph(f"{num}. {escape_xml(block[1])}", styles['Numbered']))

        elif block_type == 'code':
            code_text = escape_xml(block[1])
            if code_text.strip():
                story.append(Paragraph(code_text, styles['CodeBlock']))

        elif block_type == 'table':
            table = build_table(block[1], styles)
            if table:
                story.append(Spacer(1, 8))
                story.append(table)
                story.append(Spacer(1, 8))

        elif block_type == 'hr':
            story.append(Spacer(1, 10))
            story.append(HRFlowable(width="40%", thickness=1, color=COLORS['light'], spaceAfter=10))

    doc.build(story)
    print(f"PDF generated: {output_path}")


def main():
    script_dir = Path(__file__).parent
    input_file = script_dir / "codebase-analysis.md"
    output_file = script_dir / "codebase-analysis-v2.pdf"

    print(f"Reading: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Generating PDF...")
    build_pdf(content, output_file)
    print("Done!")


if __name__ == "__main__":
    main()
