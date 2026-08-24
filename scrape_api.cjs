const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    try {
        const browser = await puppeteer.launch({ headless: true });
        const page = await browser.newPage();
        
        let apiResponses = [];
        page.on('response', async (response) => {
            if (response.url().includes('get_') || response.url().includes('search') || response.url().includes('php')) {
                try {
                    const text = await response.text();
                    if(text.includes('Solid Power') || text.includes('Wash')) {
                        apiResponses.push({ url: response.url(), data: text });
                    }
                } catch(e) {}
            }
        });

        await page.goto('https://ecolabwallchart.azurewebsites.net/ecolab/home.php?l=3', { waitUntil: 'networkidle2' });
        
        await page.click('#vn');
        await new Promise(r => setTimeout(r, 3000));
        
        fs.writeFileSync('api_responses.json', JSON.stringify(apiResponses, null, 2));
        console.log("API responses saved.");
        await browser.close();
    } catch (e) {
        console.error(e);
    }
})();
