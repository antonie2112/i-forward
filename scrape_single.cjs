const puppeteer = require('puppeteer');

(async () => {
    try {
        const browser = await puppeteer.launch({ headless: true });
        const page = await browser.newPage();
        
        await page.goto('https://ecolabwallchart.azurewebsites.net/ecolab/home.php?l=3', { waitUntil: 'networkidle2' });
        
        await page.click('#vn');
        await new Promise(r => setTimeout(r, 2000));
        
        await page.type('.query', 'Solid Power');
        await page.click('.btn-search');
        await new Promise(r => setTimeout(r, 3000));
        
        const html = await page.evaluate(() => {
            const results = document.querySelector('#result');
            return results ? results.innerHTML : 'No #result found';
        });
        
        require('fs').writeFileSync('search_result.html', html);
        console.log("Search result saved.");
        await browser.close();
    } catch (e) {
        console.error(e);
    }
})();
