const elecPrice = 2014;
const waterPrice = 11500;
const gasPrice = 22500;
const laborRate = 45000;

let totalFacilityTVD = 0;

const ldLoads = 400;
const ldKg = 60;
const chemStd = 800;
const chemLT = 1100;
const waterSavL = 7;
const energySavPct = 26;
const timeSavMin = 20;

if (ldLoads > 0 && ldKg > 0) {
    const totalKg = ldLoads * ldKg;
    const stdChemCost = totalKg * chemStd * 12;
    const stdWaterCost = totalKg * 20 * (waterPrice / 1000) * 12;
    const stdEnergyCost = totalKg * (1.0 * elecPrice + 0.3 * gasPrice) * 12;
    const stdLaborCost = ldLoads * (90 / 60) * laborRate * 12;
    const stdTotal = stdChemCost + stdWaterCost + stdEnergyCost + stdLaborCost;

    const ltChemCost = totalKg * chemLT * 12;
    const ltWaterCost = totalKg * (20 - waterSavL) * (waterPrice / 1000) * 12;
    const ltEnergyCost = stdEnergyCost * (1 - energySavPct / 100);
    const ltLaborCost = ldLoads * ((90 - timeSavMin) / 60) * laborRate * 12;
    const ltTotal = ltChemCost + ltWaterCost + ltEnergyCost + ltLaborCost;

    const reclaimSav = ldLoads * 0.02 * 150000 * 12;
    const ldAnnualNet = (stdTotal - ltTotal) + reclaimSav;
    const ldPct = (ldAnnualNet / stdTotal) * 100;

    console.log("stdTotal:", stdTotal);
    console.log("ltTotal:", ltTotal);
    console.log("reclaimSav:", reclaimSav);
    console.log("ldAnnualNet:", ldAnnualNet);
}
