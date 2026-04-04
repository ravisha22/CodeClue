"""Convert the explainer markdown to print-ready HTML then PDF."""
import markdown
from pathlib import Path

md_path = Path("paper/codeclue-explainer.md")
md_text = md_path.read_text(encoding="utf-8")

html_body = markdown.markdown(
    md_text,
    extensions=["tables", "fenced_code", "toc"],
)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CodeClue: The Explainer</title>
<style>
@page {{
    size: A4;
    margin: 2cm;
}}
body {{
    font-family: 'Segoe UI', 'Calibri', 'Helvetica Neue', sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    max-width: 780px;
    margin: 0 auto;
    padding: 20px;
    color: #222;
}}
h1 {{
    font-size: 24pt;
    color: #1a5276;
    text-align: center;
    margin-top: 40px;
    margin-bottom: 30px;
    border-bottom: 3px solid #1a5276;
    padding-bottom: 15px;
}}
h2 {{
    font-size: 16pt;
    color: #1a5276;
    margin-top: 35px;
    border-bottom: 1px solid #aed6f1;
    padding-bottom: 5px;
}}
h3 {{
    font-size: 13pt;
    color: #2874a6;
    margin-top: 22px;
}}
p {{
    margin-bottom: 10px;
}}
strong {{
    color: #1a5276;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 15px 0;
    font-size: 10pt;
}}
th, td {{
    border: 1px solid #adb5bd;
    padding: 8px 10px;
    text-align: left;
}}
th {{
    background-color: #d6eaf8;
    font-weight: bold;
    color: #1a5276;
}}
tr:nth-child(even) {{
    background-color: #f8f9fa;
}}
code {{
    font-family: 'Cascadia Code', 'Consolas', 'Courier New', monospace;
    font-size: 9.5pt;
    background: #eef3f8;
    padding: 2px 5px;
    border-radius: 3px;
    color: #c0392b;
}}
pre {{
    background: #f4f6f9;
    padding: 14px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.5;
    border: 1px solid #d5dbdb;
}}
pre code {{
    background: none;
    padding: 0;
    color: #2c3e50;
}}
blockquote {{
    border-left: 4px solid #1a5276;
    margin-left: 0;
    padding: 10px 15px;
    background: #eaf2f8;
    border-radius: 0 4px 4px 0;
}}
ul, ol {{
    margin-bottom: 10px;
}}
li {{
    margin-bottom: 4px;
}}
hr {{
    border: none;
    border-top: 2px solid #d6eaf8;
    margin: 30px 0;
}}
/* Callout boxes for key findings */
@media print {{
    body {{
        font-size: 10pt;
        max-width: none;
        padding: 0;
    }}
    h1 {{
        page-break-before: avoid;
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
        color: #222;
        text-decoration: none;
    }}
}}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

html_path = Path("paper/codeclue-explainer.html")
html_path.write_text(html, encoding="utf-8")
print(f"HTML written to {html_path}")
