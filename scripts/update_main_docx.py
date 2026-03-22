import sys

file_path = '/Users/nguyenphong/Desktop/Inst.sale/main.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "const proposalTemplates = {"
start_idx = content.find(start_marker)

if start_idx == -1:
    print("Could not find start marker.")
    sys.exit(1)

# Also remove prior exportProposalPdf and toggleProposalMode if they are before proposalTemplates
# Let's cleanly replace everything from start_idx
# Wait, let's find `let currentPropMode = 'edit';` or `// PROPOSAL PREVIEW & PDF EXPORT`
# because my previous edit added that before proposalTemplates

prev_marker = "// ---------------------------------------------------------\n// PROPOSAL PREVIEW & PDF EXPORT"
prev_idx = content.find(prev_marker)

if prev_idx != -1 and prev_idx < start_idx:
    start_idx = prev_idx

new_content = """// ---------------------------------------------------------
// DOCX PREVIEW LOGIC
// ---------------------------------------------------------
let currentDocxBlob = null;
let currentSelectedImage = null;

async function renderDocxPreview() {
    const container = document.getElementById('docxContainer');
    if (!container) return;
    
    container.innerHTML = '<div style="color: white; text-align: center; padding: 40px;">⏳ Đang tải Proposal Template...</div>';
    
    // Choose file based on language
    const fileName = currentProposalLang === 'en' ? 'Ecolab proposal.docx' : 'Ecolab - Bang de xuat hop tac.docx';
    
    try {
        const response = await fetch(fileName);
        if (!response.ok) throw new Error('File not found');
        currentDocxBlob = await response.blob();
        
        container.innerHTML = '';
        await docx.renderAsync(currentDocxBlob, container, null, {
            className: "docx",
            inWrapper: true,
            ignoreWidth: false,
            ignoreHeight: false,
            ignoreFonts: false,
            breakPages: true,
            ignoreLastRenderedPageBreak: true,
            experimental: true,
            trimXmlDeclaration: true,
            debug: false
        });
        
        // Setup image click listeners for replacement
        setupImageClickListeners();
        
    } catch (err) {
        console.error("Error loading docx:", err);
        container.innerHTML = `<div style="color: red; padding: 20px;">Lỗi tải template: ${err.message}.</div>`;
    }
}

function setupImageClickListeners() {
    const container = document.getElementById('docxContainer');
    if (!container) return;
    
    const images = container.querySelectorAll('img');
    images.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', (e) => {
            // Remove highlight from all
            images.forEach(i => i.style.outline = 'none');
            // Highlight current
            e.target.style.outline = '3px solid var(--color-primary)';
            currentSelectedImage = e.target;
            
            // Show tool 
            const btnChange = document.getElementById('btnChangeImage');
            if (btnChange) btnChange.style.display = 'inline-block';
        });
    });
    
    // Hide tool if clicking outside image
    container.addEventListener('click', (e) => {
        if (e.target.tagName !== 'IMG') {
            images.forEach(i => i.style.outline = 'none');
            currentSelectedImage = null;
            const btnChange = document.getElementById('btnChangeImage');
            if (btnChange) btnChange.style.display = 'none';
        }
    });
}

function triggerImageUpload() {
    if (!currentSelectedImage) {
        alert("Vui lòng click chọn 1 hình ảnh trong văn bản trước.");
        return;
    }
    const input = document.getElementById('replaceImageInput');
    if (input) input.click();
}
window.triggerImageUpload = triggerImageUpload;

function handleReplaceImage(event) {
    const file = event.target.files[0];
    if (!file || !currentSelectedImage) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        currentSelectedImage.src = e.target.result;
        // Keep outline so they know it changed
    };
    reader.readAsDataURL(file);
    // Reset file input
    event.target.value = '';
}
window.handleReplaceImage = handleReplaceImage;

function toggleProposalLang() {
    currentProposalLang = currentProposalLang === 'vn' ? 'en' : 'vn';
    const btn = document.getElementById('propLangToggle');
    if (btn) {
        btn.textContent = currentProposalLang === 'vn' ? 'Tiếng Việt' : 'English / Tiếng Anh';
    }
    renderDocxPreview();
}
window.toggleProposalLang = toggleProposalLang;

// Initialize proposal template on load
document.addEventListener('DOMContentLoaded', () => {
    // Wait for docx-preview script to be ready
    setTimeout(() => {
        if (typeof docx !== 'undefined') {
            renderDocxPreview();
        }
    }, 1000);
});

// Update exportProposalPdf
function exportProposalPdf() {
    const container = document.getElementById('docxContainer');
    if (!container) return;
    
    // Remove outlines before PDF
    const images = container.querySelectorAll('img');
    images.forEach(i => i.style.outline = 'none');
    
    const btnPdf = document.getElementById('btnExportPdf');
    const oriText = btnPdf ? btnPdf.innerHTML : "Xuất PDF Đề Xuất";
    if (btnPdf) btnPdf.innerHTML = "⏳ Đang tạo PDF...";

    setTimeout(() => {
        // Because docx-preview renders a wrapper (.docx-wrapper), we select it
        const docWrapper = container.querySelector('.docx-wrapper') || container;
        
        // Hide UI elements not meant for PDF
        const btnChange = document.getElementById('btnChangeImage');
        if (btnChange) btnChange.style.display = 'none';
        
        // Apply temporary styles for clean print
        const oriBg = container.style.background;
        container.style.background = '#ffffff';
        container.style.paddingBottom = '0px';

        html2canvas(docWrapper, {
            scale: 2, 
            useCORS: true,
            backgroundColor: '#ffffff'
        }).then(canvas => {
            container.style.background = oriBg;
            container.style.paddingBottom = '50px';
            
            const { jsPDF } = window.jspdf;
            const pdf = new jsPDF('p', 'mm', 'a4');
            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = pdf.internal.pageSize.getHeight();
            
            const pageHeight = Math.floor(canvas.width * 1.4142); 
            let position = 0;
            const imgHeight = canvas.height;
            
            let isFirstPage = true;
            
            while (position < imgHeight) {
                if (!isFirstPage) pdf.addPage();
                
                const sliceCanvas = document.createElement('canvas');
                sliceCanvas.width = canvas.width;
                sliceCanvas.height = Math.min(pageHeight, imgHeight - position);
                const ctx = sliceCanvas.getContext('2d');
                
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, sliceCanvas.width, sliceCanvas.height);
                ctx.drawImage(canvas, 0, position, canvas.width, sliceCanvas.height, 0, 0, sliceCanvas.width, sliceCanvas.height);
                
                const sliceDataUrl = sliceCanvas.toDataURL('image/jpeg', 0.95);
                const drawHeight = (sliceCanvas.height * pdfWidth) / sliceCanvas.width;
                
                pdf.addImage(sliceDataUrl, 'JPEG', 0, 0, pdfWidth, drawHeight);
                
                position += pageHeight;
                isFirstPage = false;
            }
            
            pdf.save("DeXuatHopTac_Ecolab.pdf");
            if (btnPdf) btnPdf.innerHTML = oriText;
        }).catch(err => {
            console.error("Lỗi xuất PDF:", err);
            container.style.background = oriBg;
            container.style.paddingBottom = '50px';
            alert("Có lỗi xảy ra: " + err);
            if (btnPdf) btnPdf.innerHTML = oriText;
        });
    }, 100);
}
window.exportProposalPdf = exportProposalPdf;
"""

final_content = content[:start_idx] + new_content

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Updated main.js with DOXC logic")
