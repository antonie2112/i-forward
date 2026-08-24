const fs = require('fs');

const dmapData = JSON.parse(fs.readFileSync('./public/dmap_data.json'));
const rawData = JSON.parse(fs.readFileSync('./public/guidex_data.json'));

const guidexData = {};
for (const [key, value] of Object.entries(rawData)) {
    if (key.length > 2) guidexData[key] = value;
}

const match = dmapData.find(x => x.DiverseyShort === 'Forward DC');

const safeObjStr = encodeURIComponent(JSON.stringify(match)).replace(/'/g, "%27");

const obj = JSON.parse(decodeURIComponent(safeObjStr));
console.log("Parsed object:", obj.DiverseyShort);

const keys = Object.keys(guidexData);
const normalizeKey = (str) => str.toLowerCase().replace(/[-_ ]/g, '');
const targetNormalized = normalizeKey(obj.Ecolab);

const bestMatch = keys.find(k => {
    const kNorm = normalizeKey(k.replace('_Catsheet', ''));
    return kNorm.includes(targetNormalized) || targetNormalized.includes(kNorm);
});

console.log("bestMatch:", bestMatch);

try {
    const langKey = 'vi';
    let prodData = guidexData[obj.Ecolab] || guidexData[obj.Ecolab + "_Catsheet"];
    
    if (!prodData && bestMatch) {
        prodData = guidexData[bestMatch];
    }
    
    const details = prodData ? (prodData[langKey] || prodData['vi'] || prodData['en']) : null;
    console.log("details:", details ? "Found" : "Not Found");
    console.log("pH:", obj.Technical.pH);
    console.log("Saftey:", obj.Safety.Signal);
} catch (e) {
    console.error("ERROR:", e);
}

