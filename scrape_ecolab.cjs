const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    try {
        const browser = await puppeteer.launch({ headless: true });
        const page = await browser.newPage();
        await page.goto('https://ecolabwallchart.azurewebsites.net/ecolab/home.php?l=3', { waitUntil: 'networkidle2' });
        await page.screenshot({ path: 'ecolab_home.png' });
        const html = await page.content();
        fs.writeFileSync('ecolab_home.html', html);
        console.log("Screenshot and HTML saved.");
        await browser.close();
    } catch (e) {
        console.error(e);
    }
})();
