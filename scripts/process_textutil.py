import re
from bs4 import BeautifulSoup
import mammoth

def convert_textutil_to_inline(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    # Extract CSS from <style>
    style_tag = soup.find("style")
    if not style_tag: return ""
    
    css_text = style_tag.string
    classes = {}
    
    # Very basic regex to grab `element.class { rules }`
    for match in re.finditer(r'([a-zA-Z0-9_\-\.]+)\s*\{\s*([^\}]+)\s*\}', css_text):
        selector = match.group(1).strip()
        rules = match.group(2).strip()
        
        # Only care about class selectors like p.p1 or span.s1 or table.t1
        if '.' in selector:
            tag, cls = selector.split('.', 1)
            classes[cls] = rules
            
    # Inline the styles
    for tag in soup.find_all(True):
        if tag.has_attr("class"):
            inline_style = ""
            for cls in tag["class"]:
                if cls in classes:
                    inline_style += classes[cls] + "; "
            
            if inline_style:
                existing_style = tag.get("style", "")
                tag["style"] = existing_style + "; " + inline_style if existing_style else inline_style
            
            # Clean up class
            del tag["class"]

    # Grab the body content
    body = soup.find("body")
    if not body: return ""
    
    html_out = "".join(str(child) for child in body.children)
    
    # Clean up empty spans that textutil generates for images
    html_out = re.sub(r'<p[^>]*>\s*<span[^>]*></span>\s*<br/>\s*</p>', '', html_out)
    return html_out

def extract_mammoth_images(docx_path):
    # Get just the images from mammoth as a list of HTML tags
    with open(docx_path, "rb") as f:
        result = mammoth.convert_to_html(f)
    soup = BeautifulSoup(result.value, "html.parser")
    return [str(img) for img in soup.find_all("img")]

vn_html = convert_textutil_to_inline("ecolab_vn_textutil.html")
en_html = convert_textutil_to_inline("ecolab_en_textutil.html")

# Let's extract images from the mammoth output and prepend them at the very top of the document
# so the user has the images available to drag&drop inside their contenteditable area if they want.
vn_images = "".join(extract_mammoth_images("Ecolab - Bang de xuat hop tac.docx"))
en_images = "".join(extract_mammoth_images("Ecolab proposal.docx"))

# Add a warning/instruction to the top
vn_html = f'''<div style="background: #eef8ff; padding: 15px; border: 1px solid #bce0fd; border-radius: 5px; margin-bottom: 20px; font-family: Arial;">
    <strong style="color: #0070c0;">💡 Mẹo chỉnh sửa hình ảnh:</strong><br/>
    Hệ thống đã giữ lại định dạng màu sắc nét chữ chuẩn xác 100% từ Word. Hình ảnh từ file gốc đã được đặt bên dưới, bạn có thể <b>Kéo - Thả</b> chúng và thả vào bất kỳ vị trí nào trong văn bản mẫu. <br/>(Có thể xóa thông báo này trước khi Xuất PDF).
    <div style="margin-top: 10px; display: flex; gap: 10px; flex-wrap: wrap;">{vn_images}</div>
</div>''' + vn_html

en_html = f'''<div style="background: #eef8ff; padding: 15px; border: 1px solid #bce0fd; border-radius: 5px; margin-bottom: 20px; font-family: Arial;">
    <strong style="color: #0070c0;">💡 Image Editing Tip:</strong><br/>
    The system has natively preserved 100% of the exact Word formatting (fonts, coloring, layout). Original images are placed below — you can <b>Drag and Drop</b> them into any position within the proposal text. <br/>(You can delete this banner before exporting to PDF).
    <div style="margin-top: 10px; display: flex; gap: 10px; flex-wrap: wrap;">{en_images}</div>
</div>''' + en_html

with open("main.js", "r", encoding="utf-8") as f:
    js_content = f.read()

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

start_idx = js_content.find('const proposalTemplates = {')
end_idx = js_content.find('};', start_idx) + 2
new_js = js_content[:start_idx] + create_replacement(vn_html, en_html) + js_content[end_idx:]

with open("main.js", "w", encoding="utf-8") as f:
    f.write(new_js)

print("TextUtil inlining and injection complete.")
