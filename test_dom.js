const fs = require('fs');
const html = fs.readFileSync('/Users/nguyenphong/Desktop/Inst.sale/index.html', 'utf8');

const extractValue = (html, id) => {
    let regex = new RegExp(`id="${id}"[^>]*value="([^"]*)"`);
    let match = html.match(regex);
    if (match) return match[1];
    
    // check text content if no value attribute
    regex = new RegExp(`id="${id}"[^>]*>([^<]*)<`);
    match = html.match(regex);
    if (match) return match[1];
    
    return null;
};

const ids = [
    'tvd-loads', 'tvd-kg-load', 'tvd-chem-std', 'tvd-chem-lt', 
    'tvd-water-sav', 'tvd-energy-sav', 'tvd-time-sav',
    'tvd-elec-price', 'tvd-water-price', 'tvd-gas-price', 'tvd-labor-rate'
];

ids.forEach(id => {
    console.log(`${id}: ${extractValue(html, id)}`);
});
