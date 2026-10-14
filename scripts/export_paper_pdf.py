#!/usr/bin/env python3
"""
scratch/export_paper_pdf.py — High-fidelity Academic PDF Exporter

Renders Markdown documents to publication-grade academic PDFs using
MathJax and Microsoft Edge headless engine.
"""

import os
import re
import sys
import time
import subprocess
from pathlib import Path
import markdown

REPO_ROOT = Path(r"C:\Users\lenovo\Documents\Github Repo\hsri-research")
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true
  }},
  options: {{
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }}
}};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
@page {{
  size: A4;
  margin: 20mm 18mm 22mm 18mm;
  @bottom-right {{
    content: counter(page);
    font-size: 8pt;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: #666;
  }}
}}

body {{
  font-family: 'Georgia', 'Cambria', serif;
  font-size: 10.2pt;
  line-height: 1.55;
  color: #111;
  max-width: 100%;
  margin: 0;
  padding: 0;
}}

h1 {{
  font-size: 18pt;
  line-height: 1.25;
  color: #0b1d3a;
  margin-top: 0;
  margin-bottom: 12pt;
  text-align: center;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-weight: 700;
}}

h2 {{
  font-size: 13pt;
  line-height: 1.3;
  color: #1a365d;
  margin-top: 18pt;
  margin-bottom: 6pt;
  border-bottom: 1px solid #cbd5e1;
  padding-bottom: 3pt;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-weight: 600;
  page-break-after: avoid;
}}

h3 {{
  font-size: 11pt;
  line-height: 1.35;
  color: #2b4365;
  margin-top: 14pt;
  margin-bottom: 4pt;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-weight: 600;
  page-break-after: avoid;
}}

h4 {{
  font-size: 10pt;
  color: #334155;
  margin-top: 10pt;
  margin-bottom: 3pt;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-weight: 600;
  page-break-after: avoid;
}}

p {{
  margin-top: 0;
  margin-bottom: 8pt;
  text-align: justify;
  text-justify: inter-word;
}}

blockquote {{
  border-left: 3px solid #3b82f6;
  margin: 10pt 0;
  padding: 6pt 12pt;
  background-color: #f8fafc;
  font-size: 9.8pt;
  color: #334155;
  font-style: italic;
}}

table {{
  width: 100%;
  border-collapse: collapse;
  margin: 12pt 0;
  font-size: 8.5pt;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  page-break-inside: avoid;
}}

th, td {{
  border: 1px solid #cbd5e1;
  padding: 4.5pt 6pt;
  text-align: left;
}}

th {{
  background-color: #f1f5f9;
  font-weight: 600;
  color: #0f172a;
}}

tr:nth-child(even) {{
  background-color: #f8fafc;
}}

code {{
  font-family: 'Consolas', 'Menlo', monospace;
  font-size: 9pt;
  background-color: #f1f5f9;
  padding: 1pt 3pt;
  border-radius: 3px;
}}

pre {{
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 8pt 10pt;
  font-size: 8.5pt;
  overflow-x: auto;
  border-radius: 4px;
  page-break-inside: avoid;
}}

hr {{
  border: none;
  border-top: 1px solid #e2e8f0;
  margin: 16pt 0;
}}

ul, ol {{
  margin-top: 0;
  margin-bottom: 8pt;
  padding-left: 20pt;
}}

li {{
  margin-bottom: 3pt;
}}

.footer-notice {{
  margin-top: 24pt;
  padding-top: 8pt;
  border-top: 1px solid #cbd5e1;
  font-size: 8pt;
  color: #64748b;
  text-align: center;
}}
</style>
</head>
<body>
{body}
<div class="footer-notice">
  Human Superintelligence Readiness Index (HSRI) 2.0 &bull; Permanent DOI: 10.5281/zenodo.10842000 &bull; License: CC BY-SA 4.0
</div>
</body>
</html>
"""

def markdown_to_html(md_path: Path) -> str:
    content = md_path.read_text(encoding='utf-8')
    
    # Extract title from first H1
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else md_path.stem
    
    # Protect MathJax blocks
    math_tokens = []
    def save_math_block(match):
        math_tokens.append(match.group(0))
        return f"<!--MATH_BLOCK_{len(math_tokens)-1}-->"

    def save_math_inline(match):
        math_tokens.append(match.group(0))
        return f"<!--MATH_INLINE_{len(math_tokens)-1}-->"

    # Match display math $$...$$
    protected = re.sub(r'\$\$(.+?)\$\$', save_math_block, content, flags=re.DOTALL)
    # Match inline math $...$
    protected = re.sub(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', save_math_inline, protected)
    
    # Convert markdown
    html_body = markdown.markdown(protected, extensions=['extra', 'toc', 'tables', 'fenced_code'])
    
    # Restore math
    for idx, token in enumerate(math_tokens):
        html_body = html_body.replace(f"<!--MATH_BLOCK_{idx}-->", token)
        html_body = html_body.replace(f"<!--MATH_INLINE_{idx}-->", token)

    return HTML_TEMPLATE.format(title=title, body=html_body)

def render_pdf(html_path: Path, pdf_path: Path):
    cmd = [
        EDGE_EXE,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri()
    ]
    print(f"Rendering {pdf_path.name} via Edge Headless...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Warning/Error rendering PDF: {res.stderr}")
    else:
        if pdf_path.exists():
            print(f"Successfully generated: {pdf_path} ({pdf_path.stat().st_size:,} bytes)")
        else:
            print(f"PDF output file not found: {pdf_path}")

def main():
    targets = [
        REPO_ROOT / 'research' / 'preprint' / 'working-paper-v1.1.0.md',
        REPO_ROOT / 'reports' / 'grant-proposals' / 'ltff_update_memo_2026-10-14.md',
        REPO_ROOT / 'docs' / 'regulatory_crosswalk.md',
        REPO_ROOT / 'research' / 'preprint' / 'anticipated_objections_rebuttal.md'
    ]
    
    for md_path in targets:
        if not md_path.exists():
            print(f"Skipping non-existent: {md_path}")
            continue
            
        html_path = md_path.with_suffix('.html')
        pdf_path = md_path.with_suffix('.pdf')
        
        html_content = markdown_to_html(md_path)
        html_path.write_text(html_content, encoding='utf-8')
        print(f"Generated HTML: {html_path}")
        
        render_pdf(html_path, pdf_path)

if __name__ == '__main__':
    main()
