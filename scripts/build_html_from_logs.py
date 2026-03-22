import re
import os

def parse_log_to_html(log_file):
    if not os.path.exists(log_file): return ""
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    html = '<div contenteditable="true" style="outline:none; font-family: \\\'Times New Roman\\\', serif; font-size: 14px; line-height: 1.5; color: #000;">\\n'
    
    in_table_section = False
    
    for row in lines:
        line = row.strip()
        if not line:
            html += '<br>\\n'
            continue
            
        if line.startswith("--- CONTENT OF"):
            continue
            
        if line.startswith("--- TABLES IN"):
            in_table_section = True
            html += '<br><h3 style="color: var(--color-primary); border-bottom: 2px solid var(--color-primary); padding-bottom: 5px;">PHỤ LỤC / APPENDIX (Tables)</h3>\\n'
            continue
            
        if in_table_section:
            if " | " in line:
                cells = line.split(" | ")
                html += '<table style="width: 100%; border-collapse: collapse; margin-bottom: 15px;" border="1">\\n<tr>\\n'
                for cell in cells:
                    html += f'<td style="padding: 5px; border: 1px solid #ccc;">{cell}</td>\\n'
                html += '</tr>\\n</table>\\n'
            else:
                 html += f'<p style="margin: 5px 0; font-weight:bold;">{line}</p>\\n'
        else:
            # Body text formatting
            if line.isupper() and len(line) < 100:
                html += f'<h2 style="color: var(--color-primary); font-size: 16px; margin-top: 20px;">{line}</h2>\\n'
            elif line.startswith("Kính gửi:") or line.startswith("To:") or "Dear" in line or "Chào anh" in line:
                html += f'<p style="margin: 5px 0; font-weight: bold;">{line}</p>\\n'
            elif line.startswith("■"):
                 html += f'<li style="margin-left: 20px;">{line[1:].strip()}</li>\\n'
            else:
                html += f'<p style="margin: 5px 0; text-align: justify;">{line}</p>\\n'
                
    html += '</div>\\n'
    return html

vn_html = parse_log_to_html("ecolab_vn.log")
en_html = parse_log_to_html("ecolab_en.log")

with open("main.js", "r", encoding="utf-8") as f:
    js_content = f.read()

replacement = f"""const proposalTemplates = {{
    vn: {{
        title: "",
        lblTo: "",
        lblDate: "",
        lblContact: "",
        lblFrom: "",
        lblAppendixTitle: "",
        sigClient: "",
        sigEcolab: "",
        bodyHtml: `{vn_html}`
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
        bodyHtml: `{en_html}`
    }}
}};"""

new_js = re.sub(r'const proposalTemplates = {.*?};', replacement, js_content, flags=re.DOTALL)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(new_js)

print("Injected raw DOCX logs into main.js!")
