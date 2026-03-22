const XLSX = require('xlsx');

try {
  const workbook = XLSX.readFile('templates_and_data/TVD Prospecting Tool - Jan-2026 - PW Protected.xlsx', { cellFormula: true });
  const sheet = workbook.Sheets['Tool - Jan 2026'];
  const data = XLSX.utils.sheet_to_json(sheet, { header: 1 });
  
  data.forEach((row, rowIndex) => {
      const rowStr = row.map(cell => String(cell).toLowerCase()).join(' | ');
      if (rowStr.includes('water') || rowStr.includes('lít') || rowStr.includes('lit') || rowStr.includes('kg') || rowStr.includes('20')) {
         console.log(`[R${rowIndex+1}]`, row.filter(cell => cell !== undefined && cell !== null && cell !== '').join(' | '));
      }
  });
} catch (error) {
  console.error(error);
}
