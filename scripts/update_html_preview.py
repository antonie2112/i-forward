import sys

file_path = '/Users/nguyenphong/Desktop/Inst.sale/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace flipbookWrapper with Presentation Controls
to_replace = """        <!-- FLIPBOOK CONTAINER (Presentation Mode) -->
        <div id="flipbookWrapper"
          style="display: none; width: 100%; text-align: center; padding: 10px 0; background-color: #f4f6f8; border-radius: 8px; box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);">
          <div id="flipbook" style="margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.2);"></div>
        </div>"""

replacement = """        <!-- PRESENTATION OVERLAY CONTROLS -->
        <div id="presentationControls" style="display: none; position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 9999; background: rgba(0,0,0,0.8); padding: 10px 20px; border-radius: 30px; gap: 15px; align-items: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
           <span style="color: white; font-weight: bold; margin-right: 10px;">Chế độ Trình chiếu</span>
           <button class="btn btn-primary" onclick="window.exportProposalPdf()">📄 Xuất PDF Đề Xuất</button>
           <button class="btn btn-outline" style="color:white; border-color:white;" onclick="toggleProposalMode('edit')">❌ Chuyển sang Soạn thảo</button>
        </div>"""

text = text.replace(to_replace, replacement)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated index.html")
