import mammoth
import re

def convert_docx_to_html(docx_path):
    # Mammoth supports basic mapping, let's keep it clean
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(
            docx_file,
            ignore_empty_paragraphs=False
        )
        html = result.value
        # Add basic styling to tables which mammoth leaves naked
        html = html.replace('<table>', '<table style="width: 100%; border-collapse: collapse; margin-block-end: 1rem; border: 1px solid #ccc; font-size: 13px;">')
        html = html.replace('<tr>', '<tr style="border-bottom: 1px solid #ddd;">')
        html = html.replace('<td>', '<td style="padding: 8px; border: 1px solid #ccc;">')
        html = html.replace('<th>', '<th style="padding: 8px; border: 1px solid #ccc; background: #f5f5f5; font-weight: bold;">')
        html = html.replace('<ul>', '<ul style="margin-left: 20px; margin-bottom: 10px; list-style-type: disc;">')
        html = html.replace('<h2>', '<h2 style="color: var(--color-primary); font-size: 1.25em; margin-top: 1.5em; margin-bottom: 0.5em;">')
        html = html.replace('<h3>', '<h3 style="color: var(--color-primary); font-size: 1.1em; margin-top: 1.2em; margin-bottom: 0.5em;">')
        return html

vn_html = convert_docx_to_html("Ecolab - Bang de xuat hop tac.docx")
en_html = convert_docx_to_html("Ecolab proposal.docx")

with open("main.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# Replace the payload directly
def create_replacement(v_html, e_html):
    return f"""const proposalTemplates = {{
    vn: {{
        title: "",
        lblTo: "",
        lblDate: "",
        lblContact: "",
        lblFrom: "",
        lblAppendixTitle: "",
        sigClient: "",
        sigEcolab: "",
        bodyHtml: `{v_html}`
    }},
    en: {{
        title: "",
        lblTo: "",
        lblDate: "",
        lblContact: "",
        lblFrom: "",
        lblAppendixTitle: "",
        sigClient: "",
        sigEcolab: "",
        bodyHtml: `{e_html}`
    }}
}};"""
# Find the template block and replace using string find and slice to avoid regex compilation errors
start_idx = js_content.find('const proposalTemplates = {')
end_idx = js_content.find('};', start_idx) + 2
new_js = js_content[:start_idx] + create_replacement(vn_html, en_html) + js_content[end_idx:]

with open("main.js", "w", encoding="utf-8") as f:
    f.write(new_js)

print("Mammoth DOCX translation completed.")
