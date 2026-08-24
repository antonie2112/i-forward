const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    try {
        const browser = await puppeteer.launch({ headless: true });
        const page = await browser.newPage();
        
        let apiResponses = [];
        page.on('response', async (response) => {
            if (response.request().resourceType() === 'xhr' || response.request().resourceType() === 'fetch') {
                try {
                    const text = await response.text();
                    apiResponses.push({ url: response.url(), data: text.substring(0, 500) });
                } catch(e) {}
            }
        });

        await page.goto('https://ecolabwallchart.azurewebsites.net/ecolab/home.php?l=3', { waitUntil: 'networkidle2' });
        
        await page.click('#vn');
        await new Promise(r => setTimeout(r, 2000));
        
        // Let's also try typing "Solid Power" in the search box
        await page.type('.query', 'Solid Power');
        await new Promise(r => setTimeout(r, 2000));
        
        fs.writeFileSync('api_responses.json', JSON.stringify(apiResponses, null, 2));
        
        // Also dump HTML again
        const html = await page.content();
        fs.writeFileSync('ecolab_home_after_search.html', html);
        
        console.log("API responses and HTML saved.");
        await browser.close();
    } catch (e) {
        console.error(e);
    }
})();
