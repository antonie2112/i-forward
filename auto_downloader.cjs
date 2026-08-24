const fs = require('fs');
const path = require('path');
const https = require('https');

const missingProducts = require('./missing_images_report.json').missingImage;
const imageDir = path.join(__dirname, 'public', 'catsheet_images');

if (!fs.existsSync(imageDir)) {
    fs.mkdirSync(imageDir, { recursive: true });
}

function fetchPost(url, data) {
    return new Promise((resolve, reject) => {
        const req = https.request(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0'
            }
        }, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => resolve(body));
        });
        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

function downloadImage(url, dest) {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(dest);
        https.get(url, (response) => {
            if (response.statusCode === 200) {
                response.pipe(file);
                file.on('finish', () => {
                    file.close(resolve);
                });
            } else {
                reject(new Error(`Server responded with ${response.statusCode}: ${response.statusMessage}`));
            }
        }).on('error', (err) => {
            fs.unlink(dest, () => {});
            reject(err);
        });
    });
}

async function run() {
    let successCount = 0;
    let failCount = 0;

    for (const prodName of missingProducts) {
        // Prepare search term: often suffixes like "_Catsheet" or "(Ecolab)" or "RTU" might mess up the search.
        // Let's clean up the name slightly for the search.
        let searchName = prodName.replace(/_Catsheet/g, '').replace(/_CatSheet/g, '').trim();
        
        try {
            const postData = `q=${encodeURIComponent(searchName)}&s=&lang=vn&table=3&page=1`;
            const html = await fetchPost('https://ecolabwallchart.azurewebsites.net/ecolab/show_result.php', postData);
            
            // Look for <img src='img/product/TH...'>
            const match = html.match(/src='(img\/product\/[^']+)'/);
            if (match && match[1]) {
                const imgPath = match[1].split('?')[0]; // remove query params
                const imgUrl = `https://ecolabwallchart.azurewebsites.net/ecolab/${imgPath}`;
                const ext = path.extname(imgPath) || '.jpg';
                
                // Save it with the exact product name from guidex_data so the UI maps it correctly
                const destFile = path.join(imageDir, `${prodName}${ext}`);
                
                console.log(`Downloading ${prodName} -> ${imgUrl}`);
                await downloadImage(imgUrl, destFile);
                successCount++;
            } else {
                console.log(`No image found for: ${searchName}`);
                failCount++;
            }
        } catch (e) {
            console.log(`Error searching ${searchName}: ${e.message}`);
            failCount++;
        }
        
        // Wait a little bit to avoid hammering the server
        await new Promise(r => setTimeout(r, 300));
    }
    
    console.log(`\nDONE! Downloaded ${successCount} images. Failed/Not found: ${failCount}`);
}

run();
