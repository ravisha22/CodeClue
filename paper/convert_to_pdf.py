"""Convert the final paper markdown to PDF using fpdf2."""
import re
from pathlib import Path
from fpdf import FPDF


class PaperPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128)
            self.cell(0, 5, "CodeClue: Persistent LLM-Native Code Comprehension", align="C")
            self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def clean_text(text):
    """Remove markdown formatting and replace Unicode with ASCII equivalents."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)  # bold
    text = re.sub(r"\*(.+?)\*", r"\1", text)  # italic
    text = re.sub(r"`(.+?)`", r"\1", text)  # inline code
    text = re.sub(r"\$\$(.+?)\$\$", r"\1", text, flags=re.DOTALL)  # block math
    text = re.sub(r"\$(.+?)\$", r"\1", text)  # inline math
    # Replace Unicode characters with ASCII
    text = text.replace("\u2014", "--")  # em dash
    text = text.replace("\u2013", "-")   # en dash
    text = text.replace("\u2018", "'")   # left single quote
    text = text.replace("\u2019", "'")   # right single quote
    text = text.replace("\u201c", '"')   # left double quote
    text = text.replace("\u201d", '"')   # right double quote
    text = text.replace("\u2026", "...")  # ellipsis
    text = text.replace("\u2022", "-")   # bullet
    text = text.replace("\u2264", "<=")  # <=
    text = text.replace("\u2265", ">=")  # >=
    text = text.replace("\u00d7", "x")   # multiplication
    text = text.replace("\u2212", "-")   # minus
    text = text.replace("\u03c1", "rho") # rho
    text = text.replace("\u2192", "->")  # arrow
    text = text.replace("\u2713", "[x]") # checkmark
    text = text.replace("\u2717", "[ ]") # cross
    # Strip any remaining non-latin1 characters
    text = text.encode("latin-1", errors="replace").decode("latin-1")
    return text


def render_table(pdf, lines):
    """Render a markdown table."""
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)

    if len(rows) < 2:
        return

    # Skip separator row
    data_rows = [rows[0]] + [r for r in rows[1:] if not all(set(c) <= {"-", ":", " "} for c in r)]

    if not data_rows:
        return

    ncols = len(data_rows[0])
    col_width = (pdf.w - 2 * pdf.l_margin) / max(ncols, 1)

    # Header
    pdf.set_font("Helvetica", "B", 8)
    for cell in data_rows[0]:
        pdf.cell(col_width, 6, clean_text(cell)[:30], border=1, align="C")
    pdf.ln()

    # Data
    pdf.set_font("Helvetica", "", 7.5)
    for row in data_rows[1:]:
        for i, cell in enumerate(row):
            text = clean_text(cell)[:35]
            pdf.cell(col_width, 5.5, text, border=1, align="C" if i > 0 else "L")
        pdf.ln()

    pdf.ln(3)


def main():
    md_path = Path("paper/codeclue-arxiv-final.md")
    if not md_path.exists():
        print("ERROR: paper/codeclue-arxiv-final.md not found")
        return

    text = md_path.read_text(encoding="utf-8")
    lines = text.split("\n")

    pdf = PaperPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title page
    pdf.set_font("Helvetica", "B", 18)
    pdf.ln(20)
    pdf.multi_cell(0, 10, "CodeClue: Persistent LLM-Native\nCode Comprehension with\nConfidence-Gated Source Drill-Down", align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, "Ravi Nandagopalan", align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 8, "April 2026", align="C")
    pdf.ln(20)

    # Skip the title/author/date lines in markdown
    i = 0
    while i < len(lines) and not lines[i].startswith("## Abstract"):
        i += 1

    in_code_block = False
    in_table = False
    table_lines = []

    while i < len(lines):
        line = lines[i]
        i += 1

        # Code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            if in_code_block:
                pdf.set_font("Courier", "", 7.5)
                pdf.set_fill_color(240, 240, 240)
            else:
                pdf.set_font("Helvetica", "", 9.5)
                pdf.ln(2)
            continue

        if in_code_block:
            pdf.cell(0, 4.5, line[:100], fill=True)
            pdf.ln()
            continue

        # Table detection
        if "|" in line and line.strip().startswith("|"):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            continue
        elif in_table:
            render_table(pdf, table_lines)
            in_table = False
            table_lines = []

        # Headers
        if line.startswith("## "):
            if "Abstract" not in line:
                pdf.add_page()
            pdf.set_font("Helvetica", "B", 14)
            pdf.ln(3)
            pdf.cell(0, 8, clean_text(line[3:].strip()))
            pdf.ln(10)
            pdf.set_font("Helvetica", "", 9.5)
            continue

        if line.startswith("### "):
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 7, clean_text(line[4:].strip()))
            pdf.ln(8)
            pdf.set_font("Helvetica", "", 9.5)
            continue

        # Math blocks
        if line.strip().startswith("$$"):
            pdf.set_font("Courier", "I", 9)
            pdf.ln(2)
            continue

        # Horizontal rules
        if line.strip() == "---":
            pdf.ln(3)
            continue

        # Empty lines
        if not line.strip():
            pdf.ln(3)
            continue

        # Bullet points
        if line.strip().startswith("- ") or line.strip().startswith("* "):
            text = "  -  " + clean_text(line.strip()[2:])
            pdf.set_font("Helvetica", "", 9.5)
            pdf.multi_cell(0, 5, text)
            continue

        if re.match(r"^\d+\.\s", line.strip()):
            text = clean_text(line.strip())
            pdf.set_font("Helvetica", "", 9.5)
            pdf.multi_cell(0, 5, text)
            continue

        # Normal paragraph text
        text = clean_text(line.strip())
        if text:
            pdf.set_font("Helvetica", "", 9.5)
            pdf.multi_cell(0, 5, text)

    # Flush any remaining table
    if in_table and table_lines:
        render_table(pdf, table_lines)

    out_path = Path("paper/codeclue-arxiv-final.pdf")
    pdf.output(str(out_path))
    print(f"PDF written to {out_path} ({out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
