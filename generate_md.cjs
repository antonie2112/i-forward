const fs = require('fs');
const report = JSON.parse(fs.readFileSync('./missing_images_report.json'));

let md = `# 📸 GuideX Catsheet: Báo cáo Rà soát Hình ảnh Sản phẩm (Cập nhật Mới)

**Thời gian rà soát:** Tháng 08/2026
**Hệ thống:** CSDL GuideX (Ecolab Intelligence)

> [!IMPORTANT]
> **Tóm tắt kết quả (Sau khi chạy Auto-Downloader):**
> - **Tổng số Sản phẩm (Catsheet):** 223 sản phẩm
> - **Đã có Hình ảnh:** ${report.hasImage.length} sản phẩm
> - **Chưa có Hình ảnh (Missing):** ${report.missingImage.length} sản phẩm (Không tìm thấy trên Ecolab Wallchart)

Dưới đây là danh sách chi tiết các sản phẩm đã được liên kết hình ảnh thành công trong hệ thống.

---

## ✅ Danh sách ${report.hasImage.length} Sản phẩm ĐÃ CÓ hình ảnh

| STT | Tên Sản Phẩm | Trạng thái hiển thị |
| :--- | :--- | :--- |
`;

report.hasImage.forEach((p, i) => {
    md += `| ${i+1} | **${p}** | 🟢 Tốt |\n`;
});

md += `\n---

> [!WARNING]
> **${report.missingImage.length} Sản phẩm còn lại (Thiếu hình ảnh)**
> 
> Các sản phẩm này không có sẵn trên thư viện trực tuyến Ecolab Wallchart do mã vùng hoặc không được liệt kê (Ví dụ: Wash 'N Walk, Foodservice Foam Hand Sanitizer, AC30...). 
> Hệ thống GuideX sẽ tiếp tục dùng giao diện mờ (Smart Fallback) cho các sản phẩm này.
`;

fs.writeFileSync('/Users/nguyenphong/.gemini/antigravity/brain/61c53e6d-bf27-4faf-86c7-3be2b631482b/guidex_images_audit.md', md);
console.log("Updated guidex_images_audit.md");
