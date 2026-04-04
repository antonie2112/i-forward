// ==========================================
// Phase 219: GuideX Architecure
// ==========================================
window.guidexData = null;
window.currentGuidexLang = 'vi'; // default
window.currentGuidexMode = 'catsheet'; // 'catsheet' | 'dmap'

window.initGuideX = async () => {
    if (window.guidexData) return;
    try {
        const res = await fetch('./guidex_data.json');
        if (!res.ok) throw new Error('HTTP ' + res.status);
        window.guidexData = await res.json();
    } catch (e) {
        console.error('Failed to load GuideX data:', e);
    }
};

window.switchGuidexMode = (mode) => {
    window.currentGuidexMode = mode;
    const btnCat = document.getElementById('guidexModeCatsheet');
    const btnMap = document.getElementById('guidexModeDmap');
    const dmapArea = document.getElementById('guidexDmapPlaceholder');
    const searchWrapper = document.getElementById('guidexSearchInput').parentElement.parentElement;
    
    if(mode === 'catsheet') {
        btnCat.className = 'px-4 py-1.5 text-sm font-bold rounded-lg bg-white shadow-sm text-indigo-600 transition-all';
        btnMap.className = 'px-4 py-1.5 text-sm font-bold rounded-lg text-slate-500 hover:text-slate-700 transition-all';
        dmapArea.classList.add('hidden');
        searchWrapper.style.display = 'block';
    } else {
        btnMap.className = 'px-4 py-1.5 text-sm font-bold rounded-lg bg-white shadow-sm text-indigo-600 transition-all';
        btnCat.className = 'px-4 py-1.5 text-sm font-bold rounded-lg text-slate-500 hover:text-slate-700 transition-all';
        dmapArea.classList.remove('hidden');
        searchWrapper.style.display = 'none';
    }
}

window.toggleGuidexLang = () => {
    window.currentGuidexLang = window.currentGuidexLang === 'vi' ? 'en' : 'vi';
    document.getElementById('guidexLangText').innerText = window.currentGuidexLang === 'vi' ? 'VNM' : 'ENG';
    
    // Refresh search results if popup is open
    window.handleGuidexSearchInput({target: document.getElementById('guidexSearchInput')});
}

window.handleGuidexSearchInput = (e) => {
    if(!window.guidexData) return;
    const q = (e.target.value || '').toLowerCase().trim();
    const resultBox = document.getElementById('guidexSearchResults');
    if(q.length < 2) {
        resultBox.classList.add('hidden');
        return;
    }
    
    let matches = [];
    for(const prodName in window.guidexData) {
        if(prodName.toLowerCase().includes(q)) {
            matches.push(prodName);
        }
    }
    
    // Sort and limit to 10
    matches.sort();
    matches = matches.slice(0, 10);
    
    if(matches.length === 0) {
        resultBox.innerHTML = '<div class="p-4 text-center text-slate-500 text-sm">Không tìm thấy sản phẩm.</div>';
        resultBox.classList.remove('hidden');
        return;
    }
    
    // Setup white fallback for image loading errors
    const imgErrBlock = "this.onerror=null; this.parentElement.innerHTML='<div class=\\'flex items-center justify-center h-full w-full bg-slate-100 text-slate-300\\'><span class=\\'material-symbols-outlined text-3xl\\'>image<\/span><\/div>';";

    let html = '';
    const langKey = window.currentGuidexLang; // 'vi' or 'en'
    
    for(const match of matches) {
        const prodData = window.guidexData[match][langKey] || window.guidexData[match]['en'] || window.guidexData[match]['vi'];
        if(!prodData) continue;
        
        // Use properties or anything for short desc
        let desc = prodData.properties || prodData.usage || '';
        // Extract first 100 chars generically
        desc = desc.substring(0, 80) + '...';
        
        // Image resolution
        const imgName = match.replace(/ /g, '%20') + '.jpg';
        const imgUrl = `./catsheet_images/${imgName}`;
        
        html += `
          <div class="flex items-center gap-4 p-4 hover:bg-slate-50 cursor-pointer border-b border-slate-100 last:border-0 transition-colors" onclick="window.openGuidexDetail('${match.replace(/'/g, "\\'")}')">
            <div class="w-14 h-14 bg-white border border-slate-200 rounded-xl overflow-hidden shrink-0 shadow-sm flex items-center justify-center p-1">
                <img src="${imgUrl}" onerror="${imgErrBlock}" class="w-full h-full object-contain" />
            </div>
            <div class="text-left flex-1">
                <h4 class="font-bold text-slate-800 text-sm">${match}</h4>
                <p class="text-xs text-slate-500 line-clamp-1 mt-0.5">${desc}</p>
            </div>
            <span class="material-symbols-outlined text-slate-300 pointer-events-none">chevron_right</span>
          </div>
        `;
    }
    
    resultBox.innerHTML = html;
    resultBox.classList.remove('hidden');
}

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    const searchWrapper = document.getElementById('guidexSearchInput')?.parentElement?.parentElement;
    const resultBox = document.getElementById('guidexSearchResults');
    if (searchWrapper && !searchWrapper.contains(e.target)) {
        if(resultBox) resultBox.classList.add('hidden');
    }
});

// Fullscreen Guidex Layout Overlay Logic
window.openGuidexDetail = (prodName) => {
    const data = window.guidexData[prodName];
    if(!data) return;
    
    const langKey = window.currentGuidexLang;
    const prodContent = data[langKey] || data['en'] || data['vi'];
    if(!prodContent) return;
    
    const ui = document.getElementById('guidexDetailRenderer');
    const overlay = document.getElementById('guidexDetailOverlay');
    
    // Resolve High Fidelity Image via Fallback Chain
    const imgName = prodName.replace(/ /g, '%20') + '.jpg';
    let localSrc = `./catsheet_images/${imgName}`;
    const imgFailedStr = "this.onerror=null; this.parentElement.style.opacity=0;";
    
    // AI keyword extraction logic (dumb fallback for now)
    let keywords = ['Khử khuẩn', 'Hiệu suất cao', 'An toàn'];
    if(langKey === 'en') {
       keywords = ['Fast-Acting', 'High Efficacy', 'Surface Safe'];
    }
    
    // Data sections formatters
    const propertiesText = prodContent.properties || 'Không có dữ liệu đặc tính.';
    const ingredientsText = prodContent.ingredients || 'Không có dữ liệu thành phần.';
    const dilutionText = prodContent.dilution || 'Không có dữ liệu tỷ lệ pha.';
    let usageText = prodContent.usage || 'Không có dữ liệu cách dùng.';
    
    // Convert numbered steps naturally
    const formatUsage = (text) => {
        const parts = text.split(/(?=\d+\.\s+)/);
        let html = '';
        if(parts.length <= 1) return `<p class="text-sm text-on-surface-variant leading-relaxed whitespace-pre-wrap">${text}</p>`;
        
        parts.forEach((p) => {
            const m = p.match(/^(\d+)\.\s+(.*)/s);
            if(m) {
                html += `
                  <div class="flex gap-4 mb-4">
                    <div class="flex-shrink-0 w-8 h-8 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center font-bold text-sm shadow-inner">${m[1]}</div>
                    <div class="pt-1 text-sm text-on-surface-variant leading-relaxed flex-1">${m[2]}</div>
                  </div>
                `;
            } else {
               if(p.trim()) html += `<p class="text-sm text-on-surface-variant mb-4">${p.trim()}</p>`;
            }
        });
        return html;
    };
    
    const formatIngredients = (text) => {
        const lines = text.split('\n');
        let html = '<ul class="space-y-2">';
        lines.forEach(l => {
            if(!l.trim()) return;
            html += `<li class="flex items-center gap-2 text-sm border-b border-outline-variant/10 pb-2 mb-2"><span class="w-1.5 h-1.5 rounded-full bg-primary block"></span><span class="text-on-surface-variant flex-1">${l.trim()}</span></li>`;
        });
        html += '</ul>';
        return html;
    };

    const uiHtml = `
      <!-- Hero Section: Product Image & Identity -->
      <section class="relative overflow-hidden rounded-xl bg-surface-container-lowest shadow-sm border border-slate-200">
        <div class="aspect-[4/3] relative flex items-center justify-center p-8 bg-gradient-to-br from-[#ffffff] to-[#f3f4f4]">
          <div class="absolute inset-x-8 inset-y-16 bg-[#ba1a1a] rounded-2xl rotate-3 opacity-10"></div>
          <img src="${localSrc}" onerror="${imgFailedStr}" class="relative z-10 w-full h-full object-contain mb-8 drop-shadow-2xl" />
        </div>
        <div class="p-6 space-y-3">
          <div class="flex items-center gap-2">
            <span class="px-2 py-0.5 bg-primary-fixed text-on-primary-fixed text-[10px] font-bold tracking-widest uppercase rounded">Professional</span>
            <span class="px-2 py-0.5 bg-error-container text-on-error-container text-[10px] font-bold tracking-widest uppercase rounded">Ecolab</span>
          </div>
          <h2 class="text-2xl font-extrabold text-[#0053a6] tracking-tight leading-none">${prodName}</h2>
        </div>
      </section>

      <!-- Features: Bento Style -->
      <section class="grid grid-cols-2 gap-3">
        <div class="col-span-2 p-5 bg-[#0053a6] text-on-primary rounded-xl flex items-center justify-between overflow-hidden relative shadow-md">
          <div class="relative z-10">
            <p class="text-[10px] font-bold tracking-widest uppercase opacity-80 mb-1">Highlight</p>
            <h3 class="text-xl font-bold">${keywords[0]}</h3>
          </div>
          <span class="material-symbols-outlined text-6xl opacity-20 absolute -right-2 -bottom-2">verified</span>
        </div>
        <div class="p-5 bg-surface-container-low rounded-xl border border-slate-200">
          <span class="material-symbols-outlined text-primary mb-3">timer</span>
          <h4 class="text-sm font-bold text-on-surface mb-1">Efficiency</h4>
          <p class="text-xs text-on-surface-variant leading-relaxed">${keywords[1]}</p>
        </div>
        <div class="p-5 bg-surface-container-low rounded-xl border border-slate-200">
          <span class="material-symbols-outlined text-primary mb-3">health_and_safety</span>
          <h4 class="text-sm font-bold text-on-surface mb-1">Safety</h4>
          <p class="text-xs text-on-surface-variant leading-relaxed">${keywords[2]}</p>
        </div>
      </section>

      <!-- Details Sections: Tonal Layering -->
      <div class="space-y-4">
        <!-- Công dụng -->
        <section class="p-6 bg-surface-container-lowest rounded-xl border border-slate-200 shadow-sm">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-1 h-6 bg-[#006bd3] rounded-full shrink-0"></div>
            <h3 class="text-lg font-bold tracking-tight">${langKey === 'en' ? 'Properties & Benefits' : 'Cộng Dụng & Đặc tính'}</h3>
          </div>
          <p class="text-sm text-on-surface-variant leading-relaxed whitespace-pre-wrap">${propertiesText}</p>
        </section>
        
        <!-- Thành phần -->
        <section class="p-6 bg-surface-container-lowest rounded-xl border border-slate-200 shadow-sm">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-1 h-6 bg-[#006bd3] rounded-full shrink-0"></div>
            <h3 class="text-lg font-bold tracking-tight">${langKey === 'en' ? 'Ingredients' : 'Thành phần'}</h3>
          </div>
          ${formatIngredients(ingredientsText)}
        </section>

        <!-- Tỉ lệ Pha -->
        <section class="p-6 bg-primary-fixed/40 rounded-xl border border-primary/20">
          <div class="flex items-center gap-3 mb-4">
            <span class="material-symbols-outlined text-primary">opacity</span>
            <h3 class="text-lg font-bold tracking-tight text-primary">${langKey === 'en' ? 'Dilution Ratio' : 'Tỉ lệ Pha'}</h3>
          </div>
          <p class="text-sm font-bold text-on-surface">
            ${dilutionText}
          </p>
        </section>

        <!-- Hướng dẫn sử dụng -->
        <section class="p-6 bg-surface-container-lowest rounded-xl border border-slate-200 shadow-sm">
          <div class="flex items-center gap-3 mb-6">
            <div class="w-1 h-6 bg-[#006bd3] rounded-full shrink-0"></div>
            <h3 class="text-lg font-bold tracking-tight">${langKey === 'en' ? 'Usage Directions' : 'Hướng dẫn sử dụng'}</h3>
          </div>
          <div class="pt-2">
            ${formatUsage(usageText)}
          </div>
        </section>
      </div>

      <div class="h-8"></div> <!-- spacer -->
    `;
    
    ui.innerHTML = uiHtml;
    
    // Hide search view
    document.getElementById('guidexSearchResults').classList.add('hidden');
    
    // Transition overlay
    overlay.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    setTimeout(() => {
        overlay.classList.remove('opacity-0');
    }, 10);
};

window.closeGuidexDetail = () => {
    const overlay = document.getElementById('guidexDetailOverlay');
    overlay.classList.add('opacity-0');
    document.body.style.overflow = 'auto'; // restore
    setTimeout(() => {
        overlay.classList.add('hidden');
    }, 300);
}

window.processGuidexOCR = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const loader = document.getElementById('ocrLoadingOverlay');
    const textEl = document.getElementById('ocrLoadingText');
    const dropInput = document.getElementById('guidexSearchInput');

    try {
        loader.classList.remove('hidden');
        textEl.innerText = "Analyzing Image...";
        setTimeout(() => loader.classList.remove('opacity-0'), 10);

        if (!window.guidexData) await window.initGuideX();

        const reader = new FileReader();
        reader.onload = async (e) => {
            try {
                const imgDataUrl = e.target.result;
                const worker = await Tesseract.createWorker('eng');
                const ret = await worker.recognize(imgDataUrl);
                const scannedText = ret.data.text.toLowerCase();
                await worker.terminate();

                let bestMatch = null;
                for (const prodName in window.guidexData) {
                    const normName = prodName.toLowerCase();
                    if (scannedText.includes(normName)) {
                        bestMatch = prodName;
                        break;
                    }
                }

                if (bestMatch) {
                     textEl.innerText = "Sản phẩm tìm thấy: " + bestMatch;
                     setTimeout(() => {
                         loader.classList.add('opacity-0');
                         setTimeout(() => loader.classList.add('hidden'), 300);
                         
                         dropInput.value = bestMatch;
                         window.openGuidexDetail(bestMatch);
                         
                     }, 1500);
                } else {
                     textEl.innerText = "Không tìm thấy tên hóa chất trong ảnh.";
                     setTimeout(() => {
                        loader.classList.add('opacity-0');
                        setTimeout(() => loader.classList.add('hidden'), 300);
                     }, 2500);
                }

            } catch(err) {
                console.error("OCR Error:", err);
                textEl.innerText = "Lỗi xử lý AI Tesseract.";
                setTimeout(() => {
                    loader.classList.add('opacity-0');
                    setTimeout(() => loader.classList.add('hidden'), 300);
                }, 2000);
            }
        };
        reader.readAsDataURL(file);

    } catch (err) {
        console.error(err);
        loader.classList.add('opacity-0');
        setTimeout(() => loader.classList.add('hidden'), 300);
    }
};
