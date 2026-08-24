const fs = require('fs');

const guidexData = JSON.parse(fs.readFileSync('./public/guidex_data.json', 'utf8'));
const images = fs.readdirSync('./public/catsheet_images').filter(f => f.endsWith('.jpg') || f.endsWith('.png'));

const products = Object.keys(guidexData).filter(k => k.length > 2); // Exclude EN, TH, etc.

let hasImage = [];
let missingImage = [];

products.forEach(p => {
    const expectedName = p.replace(/ /g, '%20') + '.jpg';
    // Sometimes the files are saved with actual spaces instead of %20 in the filesystem
    // Let's check both
    const exists = images.includes(p + '.jpg') || images.includes(expectedName) || images.includes(p + '.png');
    
    if (exists) {
        hasImage.push(p);
    } else {
        missingImage.push(p);
    }
});

console.log(`Total Products: ${products.length}`);
console.log(`Products WITH images: ${hasImage.length}`);
console.log(`Products MISSING images: ${missingImage.length}`);

fs.writeFileSync('./missing_images_report.json', JSON.stringify({
    hasImage,
    missingImage
}, null, 2));
