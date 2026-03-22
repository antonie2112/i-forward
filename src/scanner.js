import { Html5Qrcode } from "html5-qrcode";
import productData from "../image_urls.json";

let html5QrCode = null;
const scannerOverlay = document.getElementById('scanner-overlay');

export const openScanner = (type) => {
    scannerOverlay.classList.remove('hidden');
    html5QrCode = new Html5Qrcode("reader");
    
    const config = { fps: 10, qrbox: { width: 250, height: 250 } };
    
    html5QrCode.start(
        { facingMode: "environment" }, 
        config, 
        (decodedText) => {
            console.log("Scanned text:", decodedText);
            handleScanResult(decodedText, type);
        },
        (errorMessage) => {
            // parse error, ignore
        }
    ).catch(err => {
        console.error("Camera Error:", err);
        alert("Could not access camera. Please check permissions.");
        closeScanner();
    });
};

export const closeScanner = () => {
    if (html5QrCode) {
        html5QrCode.stop().then(() => {
            html5QrCode = null;
            scannerOverlay.classList.add('hidden');
        }).catch(err => {
            console.error("Stop Error:", err);
            scannerOverlay.classList.add('hidden');
        });
    } else {
        scannerOverlay.classList.add('hidden');
    }
};

const handleScanResult = (code, type) => {
    // 1. Lookup in productData
    const product = productData.find(p => p.code === code || p.name.includes(code));
    const searchQuery = product ? product.name : code;
    
    if (type === 'sds') {
        const input = document.getElementById('sdsSearchInput');
        if (input) {
            input.value = searchQuery;
            closeScanner();
            if (window.submitSdsSearch) window.submitSdsSearch();
        }
    } else if (type === 'quotation') {
        // Future: add to quote
        alert("Product identified: " + searchQuery);
        closeScanner();
    }
};

// Attach to global window for onclick handlers in index.html
window.openScanner = openScanner;
window.closeScanner = closeScanner;
