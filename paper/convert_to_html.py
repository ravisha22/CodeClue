"""Convert paper markdown to a print-ready HTML file.
Open the HTML in a browser, then File > Print > Save as PDF."""
import markdown
from pathlib import Path

md_path = Path("paper/codeclue-arxiv-final.md")
md_text = md_path.read_text(encoding="utf-8")

html_body = markdown.markdown(
    md_text,
    extensions=["tables", "fenced_code", "codehilite", "toc"],
    extension_configs={"codehilite": {"css_class": "code"}},
)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CodeClue: Persistent LLM-Native Code Comprehension</title>
<style>
@page {{
    size: A4;
    margin: 2.5cm;
}}
body {{
    font-family: 'Times New Roman', 'Georgia', serif;
    font-size: 11pt;
    line-height: 1.5;
    max-width: 750px;
    margin: 0 auto;
    padding: 20px;
    color: #1a1a1a;
}}
h1 {{
    font-size: 20pt;
    text-align: center;
    margin-top: 60px;
    margin-bottom: 10px;
    line-height: 1.3;
}}
h2 {{
    font-size: 14pt;
    margin-top: 30px;
    border-bottom: 1px solid #ccc;
    padding-bottom: 5px;
}}
h3 {{
    font-size: 12pt;
    margin-top: 20px;
}}
p {{
    text-align: justify;
    margin-bottom: 8px;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 15px 0;
    font-size: 9.5pt;
}}
th, td {{
    border: 1px solid #888;
    padding: 5px 8px;
    text-align: left;
}}
th {{
    background-color: #f0f0f0;
    font-weight: bold;
}}
tr:nth-child(even) {{
    background-color: #fafafa;
}}
code {{
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9pt;
    background: #f5f5f5;
    padding: 1px 4px;
    border-radius: 3px;
}}
pre {{
    background: #f5f5f5;
    padding: 12px;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 8.5pt;
    line-height: 1.4;
    border: 1px solid #ddd;
}}
pre code {{
    background: none;
    padding: 0;
}}
blockquote {{
    border-left: 3px solid #ccc;
    margin-left: 0;
    padding-left: 15px;
    color: #555;
}}
hr {{
    border: none;
    border-top: 1px solid #ccc;
    margin: 30px 0;
}}
/* Print styles */
@media print {{
    body {{
        font-size: 10pt;
        max-width: none;
        padding: 0;
    }}
    h2 {{
        page-break-before: always;
    }}
    h2:first-of-type {{
        page-break-before: avoid;
    }}
    table, pre {{
        page-break-inside: avoid;
    }}
    a {{
        color: #1a1a1a;
        text-decoration: none;
    }}
}}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

out_path = Path("paper/codeclue-arxiv-final.html")
out_path.write_text(html, encoding="utf-8")
print(f"HTML written to {out_path}")
print(f"To create PDF: Open {out_path} in a browser, then File > Print > Save as PDF")
print(f"Use A4 paper, no headers/footers, margins 'Default' or 'Minimum'")
