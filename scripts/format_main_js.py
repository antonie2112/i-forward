import re

with open("main.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# Replace renderProposalTemplate
new_render_func = """function renderProposalTemplate() {
    const t = proposalTemplates[currentProposalLang];
    if (!t) return;
    
    // Update Dynamic Body (which now contains EVERYTHING except the logo)
    const body = document.getElementById('propDynamicBody');
    if (body) {
        body.innerHTML = t.bodyHtml;
    }
}"""

js_content = re.sub(r'function renderProposalTemplate\(\) \{.*?\n\}', new_render_func, js_content, flags=re.DOTALL)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("Updated render function in main.js")
