import sys

file_path = '/Users/nguyenphong/Desktop/Inst.sale/main.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Tab Switch Logic
tab_start_marker = "const targetTabContent = document.getElementById(targetTabId);"
tab_end_marker = "if (targetTabContent) targetTabContent.classList.add('active');"
start_idx = content.find(tab_start_marker)
end_idx = content.find(tab_end_marker, start_idx)

if start_idx == -1 or end_idx == -1:
    print("Could not find tab block to replace.", start_idx, end_idx)
    sys.exit(1)

tab_new_content = """const targetTabContent = document.getElementById(targetTabId);
            if (targetTabContent) targetTabContent.classList.add('active');
            
            // Auto-trigger Presentation Mode when Proposal tab is selected
            if (targetTabId === 'proposal' && typeof window.toggleProposalMode === 'function' && currentPropMode === 'edit') {
                // Short delay to allow DOM constraints to settle before capturing
                setTimeout(() => window.toggleProposalMode('presentation'), 50);
            }"""

content = content[:start_idx] + tab_new_content + content[end_idx + len(tab_end_marker):]

# Replace Language Toggle Logic
lang_start_marker = "function toggleProposalLang() {"
lang_end_marker = "window.toggleProposalLang = toggleProposalLang;"
start_idx = content.find(lang_start_marker)
end_idx = content.find(lang_end_marker, start_idx)

if start_idx == -1 or end_idx == -1:
    print("Could not find lang block to replace.")
    sys.exit(1)

lang_new_content = """function toggleProposalLang() {
    currentProposalLang = currentProposalLang === 'vn' ? 'en' : 'vn';
    const btn = document.getElementById('propLangToggle');
    if (btn) {
        btn.textContent = currentProposalLang === 'vn' ? 'Tiếng Việt' : 'English';
    }
    renderProposalTemplate();
    
    // If currently in presentation mode, re-generate it to reflect new language
    if (currentPropMode === 'presentation' && typeof window.toggleProposalMode === 'function') {
        currentPropMode = 'edit'; // force toggle back
        window.toggleProposalMode('presentation');
    }
}
window.toggleProposalLang = toggleProposalLang;"""

content = content[:start_idx] + lang_new_content + content[end_idx + len(lang_end_marker):]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated successfully")
