import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the proposal section
start_marker = '      <!-- SECTION 4: PROPOSAL -->'
end_marker = '    </main>'

new_proposal = """      <!-- SECTION 4: PROPOSAL -->
      <section id="proposal" class="tab-content">
        <!-- Control Bar -->
        <div class="prop-controls no-print" style="background: var(--color-surface); padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; gap: 15px; align-items: center;">
                <div>
                    <strong style="margin-right: 10px; color: var(--color-secondary);">Ngôn ngữ Template:</strong>
                    <button class="btn btn-outline btn-sm" id="propLangToggle" onclick="toggleProposalLang()">Tiếng Việt</button>
                </div>
                <div>
                    <strong style="margin-right: 10px; color: var(--color-secondary);">Logo Khách hàng:</strong>
                    <input type="file" id="propLogoUpload" accept="image/*" style="font-size: 0.85em;" onchange="handlePropLogoUpload(event)">
                </div>
            </div>
            <button class="btn btn-primary" onclick="window.exportProposalPdf()">📄 Xuất PDF Đề Xuất</button>
        </div>
        
        <div id="proposalDoc" class="proposal-doc">
          <!-- Header (Bi-Logo) -->
          <div class="prop-header" style="display: flex; justify-content: space-between; align-items: start; border-bottom: 2px solid var(--color-primary); padding-bottom: 15px; margin-bottom: 25px;">
            <img src="ecolab-logo-tagline svg.svg" alt="Ecolab Logo" class="prop-logo" style="height: 60px;">
            <div style="text-align: right;">
                <img id="propCustomerLogo" src="" alt="Customer Logo" style="max-height: 60px; display: none;">
            </div>
          </div>
          <h1 class="prop-title" style="text-align: center; margin-bottom: 30px;" id="propDocTitle">BẢNG ĐỀ XUẤT HỢP TÁC - BUSINESS PROPOSAL</h1>
          
          <!-- Vendor & Customer Info -->
          <table class="prop-info-table">
            <tr>
              <td width="15%"><strong id="propLblTo">Kính gửi:</strong></td>
              <td width="35%"><div contenteditable="true" class="edit-field" style="min-width: 200px;" id="propValTo">[Nhập tên Khách hàng]</div></td>
              <td width="15%" style="text-align: right;"><strong id="propLblDate">Ngày báo:</strong></td>
              <td width="35%"><div contenteditable="true" class="edit-field" style="text-align: right;" id="propValDate">[Nhập ngày]</div></td>
            </tr>
            <tr>
              <td><strong id="propLblContact">Người liên hệ:</strong></td>
              <td><div contenteditable="true" class="edit-field" id="propValContact">[Nhập người liên hệ]</div></td>
              <td style="text-align: right;"><strong id="propLblFrom">Người gửi:</strong></td>
              <td><div contenteditable="true" class="edit-field" style="text-align: right;" id="propValFrom">[Tên Sale Ecolab]</div></td>
            </tr>
          </table>

          <!-- Content Body (Dynamic) -->
          <div class="prop-body" id="propDynamicBody">
            <!-- Injected via JS -->
          </div>
          
          <!-- Appendix / Khuyến Mãi & Chiết Khấu -->
          <div class="prop-appendix" style="margin-top: 40px; page-break-inside: avoid;">
            <h2 class="prop-section-title" id="propLblAppendixTitle">Phụ lục: Thỏa thuận với Khách hàng (Program Terms)</h2>
            <div contenteditable="true" class="edit-area" style="border: 1px dashed #eee; padding: 15px;">
                <table style="width: 100%; border-collapse: collapse; font-size: 13px;" border="1">
                    <thead>
                        <tr style="background: var(--color-table-row-even);">
                            <th style="padding: 8px; text-align: left;">Hạng mục / Item</th>
                            <th style="padding: 8px; text-align: center;">Hình thức / Type</th>
                            <th style="padding: 8px; text-align: right;">Ghi chú / Note</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="padding: 8px;">Máy pha hóa chất (Dispenser)</td>
                            <td style="padding: 8px; text-align: center;">Cho mượn (FOL)</td>
                            <td style="padding: 8px; text-align: right;">Bảo trì miễn phí 1 lần/tháng</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px;">Chiết khấu thương mại</td>
                            <td style="padding: 8px; text-align: center;">... %</td>
                            <td style="padding: 8px; text-align: right;">Áp dụng từ đơn hàng ...</td>
                        </tr>
                    </tbody>
                </table>
                <p style="font-size: 11px; font-style: italic; margin-top: 10px;">* Tất cả hóa chất có tỉ lệ pha loãng đều được trang bị bằng bơm định lượng: đảm bảo bơm đúng, đủ, an toàn.<br>** Tất cả máy bơm được Ecolab trang bị miễn phí với hình thức cho mượn (FOL) với điều kiện khách hàng sử dụng hóa chất Ecolab.</p>
            </div>
          </div>

          <!-- Signatures -->
          <div class="prop-signatures">
            <div class="sig-box">
              <p><strong id="propSigClient">Xác nhận của Khách Hàng</strong></p>
              <p class="sig-title">Customer Confirmation</p>
              <div class="sig-space"></div>
            </div>
            <div class="sig-box">
              <p><strong id="propSigEcolab">Đại diện CTY TNHH Ecolab VN</strong></p>
              <p class="sig-title">Ecolab Representative</p>
              <div class="sig-space"></div>
            </div>
          </div>
        </div>
      </section>
"""

new_html = html[:html.find(start_marker)] + new_proposal + html[html.find(end_marker):]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)
