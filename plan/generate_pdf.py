#!/usr/bin/env python3
"""
Generate a visually appealing PDF from codebase-analysis.md
Uses reportlab for PDF generation with custom styling.
"""

import re
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem, KeepTogether, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Color scheme - Professional and accessible
COLORS = {
    'primary': colors.HexColor('#2563EB'),      # Blue
    'secondary': colors.HexColor('#10B981'),    # Green
    'accent': colors.HexColor('#F59E0B'),       # Amber
    'dark': colors.HexColor('#1F2937'),         # Dark gray
    'light': colors.HexColor('#F3F4F6'),        # Light gray
    'code_bg': colors.HexColor('#1E293B'),      # Code background
    'code_text': colors.HexColor('#E2E8F0'),    # Code text
    'heading1': colors.HexColor('#1E40AF'),     # Dark blue
    'heading2': colors.HexColor('#059669'),     # Dark green
    'heading3': colors.HexColor('#D97706'),     # Dark amber
    'table_header': colors.HexColor('#3B82F6'), # Table header
    'table_row_even': colors.HexColor('#F9FAFB'), # Even rows
    'table_row_odd': colors.HexColor('#FFFFFF'),  # Odd rows
}

def create_styles():
    """Create custom paragraph styles."""
    styles = getSampleStyleSheet()

    # Title style
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Title'],
        fontSize=28,
        textColor=COLORS['heading1'],
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))

    # Subtitle
    styles.add(ParagraphStyle(
        name='Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=COLORS['dark'],
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    ))

    # H1
    styles.add(ParagraphStyle(
        name='Heading1Custom',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=COLORS['heading1'],
        spaceBefore=25,
        spaceAfter=15,
        fontName='Helvetica-Bold',
        borderColor=COLORS['primary'],
        borderWidth=0,
        borderPadding=5,
        leftIndent=0,
    ))

    # H2
    styles.add(ParagraphStyle(
        name='Heading2Custom',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=COLORS['heading2'],
        spaceBefore=18,
        spaceAfter=10,
        fontName='Helvetica-Bold',
        leftIndent=10,
    ))

    # H3
    styles.add(ParagraphStyle(
        name='Heading3Custom',
        parent=styles['Heading3'],
        fontSize=13,
        textColor=COLORS['heading3'],
        spaceBefore=12,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        leftIndent=15,
    ))

    # Body text
    styles.add(ParagraphStyle(
        name='BodyCustom',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLORS['dark'],
        spaceBefore=4,
        spaceAfter=8,
        fontName='Helvetica',
        leading=14,
        alignment=TA_JUSTIFY,
    ))

    # Code block
    styles.add(ParagraphStyle(
        name='CodeBlock',
        parent=styles['Normal'],
        fontSize=8,
        textColor=COLORS['code_text'],
        backColor=COLORS['code_bg'],
        spaceBefore=8,
        spaceAfter=8,
        fontName='Courier',
        leftIndent=15,
        rightIndent=15,
        leading=11,
    ))

    # Inline code
    styles.add(ParagraphStyle(
        name='InlineCode',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier',
        textColor=COLORS['primary'],
    ))

    # Bullet item
    styles.add(ParagraphStyle(
        name='BulletItem',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLORS['dark'],
        spaceBefore=2,
        spaceAfter=2,
        fontName='Helvetica',
        leftIndent=25,
        bulletIndent=10,
    ))

    # Table cell
    styles.add(ParagraphStyle(
        name='TableCell',
        parent=styles['Normal'],
        fontSize=9,
        textColor=COLORS['dark'],
        fontName='Helvetica',
        leading=12,
    ))

    # Header cell
    styles.add(ParagraphStyle(
        name='HeaderCell',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.white,
        fontName='Helvetica-Bold',
        leading=12,
    ))

    return styles


def parse_markdown(content):
    """Parse markdown content into structured data."""
    sections = []
    current_section = None
    current_content = []

    lines = content.split('\n')

    for line in lines:
        line = line.rstrip()

        # H1
        if line.startswith('# ') and not line.startswith('## '):
            if current_section:
                sections.append((current_section, current_content))
            current_section = ('h1', line[2:])
            current_content = []
        # H2
        elif line.startswith('## '):
            if current_section:
                if current_content:
                    current_content.append(('h2', line[3:]))
            else:
                current_section = ('h2', line[3:])
                current_content = []
        # H3
        elif line.startswith('### '):
            current_content.append(('h3', line[4:]))
        # H4
        elif line.startswith('#### '):
            current_content.append(('h4', line[5:]))
        # Code block
        elif line.startswith('```'):
            continue  # Skip code fence markers
        # Table
        elif line.startswith('|'):
            current_content.append(('table_line', line))
        # Horizontal rule
        elif line.startswith('---'):
            current_content.append(('hr', None))
        # Bullet point
        elif line.startswith('- ') or line.startswith('* ') or line.startswith('  - '):
            indent = len(line) - len(line.lstrip())
            text = line.lstrip('- ').lstrip('* ')
            current_content.append(('bullet', text, indent))
        # Numbered list
        elif re.match(r'^\d+\.\s', line):
            match = re.match(r'^(\d+)\.\s(.+)$', line)
            if match:
                current_content.append(('numbered', match.group(2), int(match.group(1))))
        # Regular paragraph
        elif line.strip():
            current_content.append(('text', line))

    if current_section:
        sections.append((current_section, current_content))

    return sections


def process_inline_formatting(text, styles):
    """Process inline markdown formatting."""
    # Convert **bold** to bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Convert *italic* to italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # Convert `code` to font change
    text = re.sub(r'`(.+?)`', r'<font name="Courier" color="#2563EB">\1</font>', text)
    # Convert [links](url)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)

    # Escape special XML characters
    text = text.replace('&', '&amp;')
    text = text.replace('<b>', '<<<BOLD>>>')
    text = text.replace('</b>', '<<<ENDBOLD>>>')
    text = text.replace('<i>', '<<<ITALIC>>>')
    text = text.replace('</i>', '<<<ENDITALIC>>>')
    text = text.replace('<font', '<<<FONT')
    text = text.replace('</font>', '<<<ENDFONT>>>')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('<<<BOLD>>>', '<b>')
    text = text.replace('<<<ENDBOLD>>>', '</b>')
    text = text.replace('<<<ITALIC>>>', '<i>')
    text = text.replace('<<<ENDITALIC>>>', '</i>')
    text = text.replace('<<<FONT', '<font')
    text = text.replace('<<<ENDFONT>>>', '</font>')

    return text


def create_table_from_lines(table_lines, styles):
    """Create a reportlab table from markdown table lines."""
    # Filter out separator lines
    data_lines = [line for line in table_lines if not re.match(r'^\|[-:\s|]+\|$', line)]

    if not data_lines:
        return None

    # Parse cells
    rows = []
    for line in data_lines:
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        rows.append(cells)

    if not rows:
        return None

    # Create table content
    table_data = []
    for i, row in enumerate(rows):
        row_data = []
        for cell in row:
            cell_text = process_inline_formatting(cell, styles)
            try:
                if i == 0:
                    para = Paragraph(cell_text, styles['HeaderCell'])
                else:
                    para = Paragraph(cell_text, styles['TableCell'])
                row_data.append(para)
            except:
                row_data.append(cell)
        table_data.append(row_data)

    # Create table
    col_count = len(rows[0])
    col_width = 6.5 * inch / col_count

    table = Table(table_data, colWidths=[col_width] * col_count)

    # Style table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['table_header']),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, COLORS['light']),
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

    # Parse markdown
    sections = parse_markdown(content)

    for section_idx, (heading, content_items) in enumerate(sections):
        # Add heading
        if heading[0] == 'h1':
            if section_idx > 0:
                story.append(PageBreak())
            story.append(Paragraph(heading[1], styles['CustomTitle']))
            story.append(Spacer(1, 10))
        elif heading[0] == 'h2':
            story.append(Paragraph(heading[1], styles['Heading1Custom']))
            story.append(HRFlowable(width="100%", thickness=1, color=COLORS['primary'], spaceAfter=10))

        # Process content
        table_lines = []
        in_table = False

        i = 0
        while i < len(content_items):
            item = content_items[i]
            item_type = item[0]

            # Handle tables
            if item_type == 'table_line':
                if not in_table:
                    in_table = True
                    table_lines = []
                table_lines.append(item[1])
                i += 1
                continue
            elif in_table and item_type != 'table_line':
                # End of table
                table = create_table_from_lines(table_lines, styles)
                if table:
                    story.append(table)
                    story.append(Spacer(1, 10))
                in_table = False
                table_lines = []

            # Handle headers within content
            if item_type == 'h2':
                story.append(Paragraph(item[1], styles['Heading2Custom']))
            elif item_type == 'h3':
                story.append(Paragraph(item[1], styles['Heading3Custom']))
            elif item_type == 'h4':
                story.append(Paragraph(item[1], styles['Heading3Custom']))
            elif item_type == 'hr':
                story.append(Spacer(1, 10))
                story.append(HRFlowable(width="50%", thickness=0.5, color=COLORS['light'], spaceAfter=10))
            elif item_type == 'bullet':
                text = process_inline_formatting(item[1], styles)
                try:
                    story.append(Paragraph(f"<bullet>&bull;</bullet> {text}", styles['BulletItem']))
                except Exception as e:
                    story.append(Paragraph(f"&bull; {item[1]}", styles['BulletItem']))
            elif item_type == 'numbered':
                text = process_inline_formatting(item[1], styles)
                try:
                    story.append(Paragraph(f"{item[2]}. {text}", styles['BulletItem']))
                except:
                    story.append(Paragraph(f"{item[2]}. {item[1]}", styles['BulletItem']))
            elif item_type == 'text':
                text = process_inline_formatting(item[1], styles)
                # Check if it looks like code
                if '  ' in item[1] or item[1].startswith('    ') or '=' in item[1] or '{' in item[1]:
                    story.append(Paragraph(text, styles['CodeBlock']))
                else:
                    try:
                        story.append(Paragraph(text, styles['BodyCustom']))
                    except:
                        story.append(Paragraph(item[1], styles['BodyCustom']))

            i += 1

        # Handle table at end
        if in_table and table_lines:
            table = create_table_from_lines(table_lines, styles)
            if table:
                story.append(table)

    # Build PDF
    doc.build(story)
    print(f"PDF generated: {str(output_path)}")


def main():
    # Paths
    script_dir = Path(__file__).parent
    input_file = script_dir / "codebase-analysis.md"
    output_file = script_dir / "codebase-analysis.pdf"

    # Read markdown
    print(f"Reading: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate PDF
    print("Generating PDF...")
    build_pdf(content, output_file)
    print("Done!")


if __name__ == "__main__":
    main()
