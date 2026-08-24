const fs = require('fs');

const dmapData = JSON.parse(fs.readFileSync('./public/dmap_data.json'));
const rawData = JSON.parse(fs.readFileSync('./public/guidex_data.json'));

const guidexData = {};
for (const [key, value] of Object.entries(rawData)) {
    if (key.length > 2) guidexData[key] = value;
}

for (const match of dmapData) {
    try {
        const safeObjStr = encodeURIComponent(JSON.stringify(match)).replace(/'/g, "%27");
        const obj = JSON.parse(decodeURIComponent(safeObjStr));
        
        const keys = Object.keys(guidexData);
        const normalizeKey = (str) => str.toLowerCase().replace(/[-_ ]/g, '');
        const targetNormalized = normalizeKey(obj.Ecolab);

        const bestMatch = keys.find(k => {
            const kNorm = normalizeKey(k.replace('_Catsheet', ''));
            return kNorm.includes(targetNormalized) || targetNormalized.includes(kNorm);
        });

        const langKey = 'vi';
        let prodData = guidexData[obj.Ecolab] || guidexData[obj.Ecolab + "_Catsheet"];
        if (!prodData && bestMatch) prodData = guidexData[bestMatch];
        
        const details = prodData ? (prodData[langKey] || prodData['vi'] || prodData['en']) : null;
        const ecoProperties = details ? details.properties : "";
        const ecoUsage = details ? details.usage : "";
        
        const divFeatures = obj.Features || "";
        const divUsage = obj.Description || "";
        const prodCategory = (prodData && prodData.sector) || obj.Category || 'Professional';
        
        const uiHtml = `... ${obj.Technical.pH} ... ${obj.Safety.Signal} ... ${obj.Cost.dilution_eco}`;
        
    } catch (e) {
        console.error("FAILED on", match.DiverseyShort, e);
    }
}
console.log("TEST COMPLETE FOR ALL 45 ITEMS.");
