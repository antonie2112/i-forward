// Export Image Logic
if (exportImgBtn) {
    exportImgBtn.addEventListener('click', async () => {
        if (dropdownMenu) dropdownMenu.classList.remove('show');
        const element = document.querySelector('.panel');
        const originalTheme = document.body.dataset.theme;

        document.body.dataset.theme = 'light';
        document.body.classList.add('exporting');

        // Backup inputs and replace with spans for html2canvas to render text perfectly without borders
        const inputs = element.querySelectorAll('input:not([type="checkbox"]):not([type="radio"]), textarea');
        const wrappers = [];

        inputs.forEach(input => {
            const computed = window.getComputedStyle(input);
            const span = document.createElement('span');
            span.className = 'export-temp-span';
            span.textContent = input.value || '';

            // Copy essential styles
            span.style.fontFamily = computed.fontFamily;
            span.style.fontSize = computed.fontSize;
            span.style.fontWeight = computed.fontWeight;
            span.style.color = computed.color;
            span.style.textAlign = computed.textAlign;
            span.style.display = 'inline-block';
            span.style.width = '100%';

            // For bold textareas
            if (input.style.fontWeight === 'bold') {
                span.style.fontWeight = 'bold';
            }

            // Special handling for textareas (respect line breaks)
            if (input.tagName.toLowerCase() === 'textarea') {
                span.style.whiteSpace = 'pre-wrap';
            }

            input.style.display = 'none';
            input.parentNode.insertBefore(span, input);

            wrappers.push({ input, span });
        });

        try {
            // Short timeout to let DOM update
            await new Promise(r => setTimeout(r, 50));

            const canvas = await html2canvas(element, {
                scale: 2,
                backgroundColor: "#ffffff",
                ignoreElements: (el) => el.classList.contains('no-print'),
                logging: true,
                useCORS: true
            });

            const dataUrl = canvas.toDataURL("image/png");
            const win = window.open();
            if (win) {
                win.document.write('<img src="' + dataUrl + '" style="width:100%"/>');
                win.document.write('<br><h2 style="text-align:center;">Right click to Save Image</h2>');
                win.document.title = "Exported Quote";
                win.document.close();
            } else {
                alert("Please allow pop-ups.");
            }
        } catch (err) {
            console.error("Export failed:", err);
            alert("Could not export image.");
        } finally {
            // Restore inputs
            wrappers.forEach(w => {
                w.span.remove();
                w.input.style.display = '';
            });
            document.body.dataset.theme = originalTheme;
            document.body.classList.remove('exporting');
        }
    });
}
