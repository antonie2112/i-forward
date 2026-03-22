import productData from "../image_urls.json";

const searchInput = document.getElementById('quoteProductSearch');
const searchDropdown = document.getElementById('quoteSearchDropdown');

// Handle typing in search bar
export const handleQuoteSearch = (query) => {
    if (!query || query.length < 2) {
        searchDropdown.classList.add('hidden');
        return;
    }

    const filtered = productData.filter(p => 
        p.name.toLowerCase().includes(query.toLowerCase()) || 
        p.code.toLowerCase().includes(query.toLowerCase())
    ).slice(0, 8);

    if (filtered.length > 0) {
        searchDropdown.innerHTML = filtered.map(p => `
            <div class="px-4 py-3 hover:bg-slate-50 cursor-pointer border-b border-slate-50 flex items-center justify-between group transition-colors" 
                 onclick="window.addProductToQuote('${p.code}')">
                <div class="flex flex-col">
                    <span class="text-xs font-black text-primary uppercase tracking-widest">${p.code}</span>
                    <span class="text-sm font-bold text-slate-700">${p.name}</span>
                </div>
                <span class="material-symbols-outlined text-slate-300 group-hover:text-primary transition-colors">add_circle</span>
            </div>
        `).join('');
        searchDropdown.classList.remove('hidden');
    } else {
        searchDropdown.classList.add('hidden');
    }
};

// Add product to the global quoteItems array
export const addProductToQuote = (code) => {
    const product = productData.find(p => p.code === code);
    if (!product) return;

    // Use a unique ID based on timestamp
    const id = Date.now();
    
    // Add to global array (defined in main.js)
    if (window.quoteItems) {
        window.quoteItems.push({
            id: id,
            code: product.code,
            name: product.name,
            specs: product.specs || "",
            image: "", // Logic in renderRows handles pathing
            unit: product.unit || "can",
            price: product.price || 0,
            discountPrice: 0,
            dilution: product.dilution || "1 ml/lit"
        });
        
        // Clear search
        searchInput.value = "";
        searchDropdown.classList.add('hidden');
        
        // Re-render via main.js
        if (window.renderRows) window.renderRows();
        
        // Autosave if available
        if (window.saveTvdDraft) window.saveTvdDraft('quotation');
    }
};

// Add a new section/category
export const addSectionPrompt = () => {
    const name = prompt("Enter Category Name (e.g., KITCHEN, LAUNDRY):");
    if (name && window.quoteItems) {
        window.quoteItems.push({
            id: Date.now(),
            type: 'section',
            name: name.toUpperCase()
        });
        if (window.renderRows) window.renderRows();
    }
};

// Clear all
export const clearQuotation = () => {
    if (confirm("Are you sure you want to clear the entire quotation?")) {
        if (window.quoteItems) {
            window.quoteItems = [];
            if (window.renderRows) window.renderRows();
        }
    }
};

// Attach to window for onclick handlers
window.handleQuoteSearch = handleQuoteSearch;
window.addProductToQuote = addProductToQuote;
window.addSectionPrompt = addSectionPrompt;
window.clearQuotation = clearQuotation;
