const fs = require('fs');

const dmapData = JSON.parse(fs.readFileSync('./public/dmap_data.json'));
const guidexData = JSON.parse(fs.readFileSync('./public/guidex_data.json'));

const match = dmapData[0]; // Suma Nova L6

const safeObjStr = encodeURIComponent(JSON.stringify(match)).replace(/'/g, "%27");

// Simulating window.openGuidexDMapDetail
const obj = JSON.parse(decodeURIComponent(safeObjStr));
console.log("Parsed object:", obj.DiverseyShort);

const ecolabImgName = obj.Ecolab.replace(/ /g, '%20') + '.jpg';
console.log("ecolabImgName:", ecolabImgName);

const keys = Object.keys(guidexData);
const normalizeKey = (str) => str.toLowerCase().replace(/[-_ ]/g, '');
const targetNormalized = normalizeKey(obj.Ecolab);

const bestMatch = keys.find(k => {
    const kNorm = normalizeKey(k.replace('_Catsheet', ''));
    return kNorm.includes(targetNormalized) || targetNormalized.includes(kNorm);
});

console.log("bestMatch:", bestMatch);
