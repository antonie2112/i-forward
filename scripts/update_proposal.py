import re

vn_html = """
<h2 class="prop-section-title">CHƯƠNG TRÌNH DÀNH CHO KHU VỰC ĐÓN KHÁCH (GUEST ROOM & FRONT OF THE HOUSE PROGRAM)</h2>
<div contenteditable="true" class="edit-area">
    <p><strong>Kinh Doanh, Thương hiệu quý công ty. Là mối quan tâm của chúng tôi!</strong></p>
    <p>Đem lại những trải nghiệm tuyệt vời cho khách hàng, nâng cao hiệu quả kinh doanh và nắm bắt những trải nghiệm phát triển bền vững đều là những thành tựu của việc kinh doanh ngày nay.</p>
    <p><strong>Ecolab đem lại những giải pháp tối ưu cho bạn</strong></p>
    <ul>
        <li><strong>Sản phẩm Hiệu quả và Đậm đặc cao:</strong> Ecolab cung cấp những sản phẩm có bằng sáng chế, an toàn với môi trường, đậm đặc. Mang lại kết quả tối ưu với chi phí tối thiểu mỗi lần làm sạch.</li>
        <li><strong>Dụng cụ vệ sinh:</strong> Tối ưu kết quả với những dụng cụ tiết kiệm nhân lực giúp nhân viên làm sạch mà không phải tốn quá nhiều sức lực.</li>
        <li><strong>Công nghệ Bơm Thông Minh:</strong> Hệ thống Bơm với công nghệ tân tiến nhất, thân thiện nhất trên thị trường. Giúp cho công việc tiết kiệm thời gian, nhân lực, liều lượng bơm chuẩn xác, an toàn.</li>
        <li><strong>Dịch vụ & Huấn luyện:</strong> Chương trình Tiếp cận (huấn luyện nhân viên của bạn quy trình CHUẨN và hiểu biết HÓA CHẤT, kiểm tra nống độ và hệ thống định kỳ), mang lại kết quả tốt nhất với chi phí tối thiểu.</li>
    </ul>
</div>

<h2 class="prop-section-title">Quy trình Dọn dẹp Vệ sinh Trạm Dừng Chân</h2>
<div contenteditable="true" class="edit-area">
    <ul>
        <li><strong>Cam kết dịch vụ:</strong> 24 Giờ / Ngày, 7 Ngày / Tuần</li>
        <li><strong>Kiểm tra Kết quả:</strong> Đại diện Ecolab sẽ kiểm tra kết quả các khu vực: sàn, lối ra vào, toilet nhân viên, toilet khách, và sảnh.</li>
        <li><strong>Kiểm tra hệ thống bơm:</strong> Đại diện Ecolab sẽ kiểm tra toàn bộ hoạt động hệ thống bơm đảm bảo hoạt động đúng chức năng và lượng bơm tiêu chuẩn.</li>
        <li><strong>Kiểm tra hệ thống Bảo vệ 360º:</strong> Đại diện Ecolab sẽ kiểm tra khu vực vận hành và khu vực xử lý an toàn.</li>
    </ul>
    <p>Tất cả các dịch vụ và vấn đề đều được ghi nhận trong Service Detail Report.</p>
</div>

<h2 class="prop-section-title">CHƯƠNG TRÌNH HUẤN LUYỆN THEO YÊU CẦU (CUSTOMIZED TRAINING)</h2>
<div contenteditable="true" class="edit-area">
    <p><strong>Việc kinh doanh, Nhân sự. Là mối quan tâm của chúng tôi!</strong></p>
    <p>Thật sự quan trọng khi nhân viên được đào tạo và huấn luyện. Một chương trình huấn luyện thành công có thể cung cấp cho đội ngũ của bạn với những thông tin mà họ cần để làm việc một cách hiệu quả. Khi hoàn thành, khóa huấn luyện sẽ tác động trực tiếp tới việc giữ chân khách hàng của bạn và lợi nhuận kinh doanh.</p>
    <p>Ecolab hiểu rằng tầm quan trọng của việc cung cấp những khóa huấn luyện. Chúng tôi cam kết sẽ cung cấp mọi nguồn lực mà chúng tôi có tới bạn và đội ngũ lãnh đạo của bạn vì mục tiêu trên.</p>
</div>

<h2 class="prop-section-title">CAM KẾT DỊCH VỤ VÀ HỖ TRỢ (SERVICE AND SUPPORT COMMITMENT)</h2>
<div contenteditable="true" class="edit-area">
    <p><strong>G 360 BÁO CÁO TRỰC TUYẾN</strong></p>
    <p>Ecolab hiểu rằng luôn cần thiết để vận hành chăm sóc khách hàng liên tục và dịch vụ cần được chủ động. Báo cáo Dịch vụ Ecolab sẽ được trình bày với ban quản lý và nhấn mạnh các yếu tố vận hành cần được tiến hành ngay như yêu cầu quản lý nhân lực, sử dụng hóa chất, lãng phí và đầu tư cho tương lai.</p>
    <p>Báo cáo Dịch vụ được thể hiện dưới dạng văn bản điện tử và được kí nhận bởi Trưởng bộ phận cùng với những hành động cần thiết. Một bản copy được gửi bằng email vào ngày hôm sau.</p>
</div>
"""

en_html = """
<h2 class="prop-section-title">GUEST ROOM & FRONT OF THE HOUSE PROGRAM</h2>
<div contenteditable="true" class="edit-area">
    <p><strong>Your Business, Your Brand. Are Important to us!</strong></p>
    <p>Delivering an exception experience for your guests, enhancing business performance, and embracing sustainable practices are all key to today’s business success.</p>
    <p><strong>Ecolab delivers solutions for your Peace of Mind and meet your goals</strong></p>
    <ul>
        <li><strong>High Performance Concentrated Solutions:</strong> Ecolab provides patented, environmentally responsible concentrated products delivering excellent results with lowest costs per cleaning over ready-to-use products.</li>
        <li><strong>Cleaning Tools:</strong> Optimize results with the right labor-saving tools to help staff clean with less effort.</li>
        <li><strong>Smart Dispensing Technology:</strong> The most comprehensive, user-friendly dispensing system on the market. Helps make the job safe, easy and economical.</li>
        <li><strong>Service & Training:</strong> Ecolab consultative approach (train your staff to the RIGHT Process and Product Levels, balancing, chemistry and regular service calls), delivers sparkling clean results at the best possible lower overall operating cost.</li>
    </ul>
</div>

<h2 class="prop-section-title">Housekeeping Service Procedures</h2>
<div contenteditable="true" class="edit-area">
    <ul>
        <li><strong>Service Commitment:</strong> On call 24 Hours a Day, 7 Days a Week.</li>
        <li><strong>Results Inspected:</strong> The Ecolab Representative will inspect housekeeping results which may include: floors, entry area, employee restrooms, guest restrooms, and hallways.</li>
        <li><strong>Dispensing Equipment Inspected:</strong> Ecolab Representative will inspect all dispensing equipment to ensure proper function and concentrations.</li>
        <li><strong>360º of Protection:</strong> Ecolab Representative will inspect operational areas and potential safety areas.</li>
    </ul>
    <p>All issues identified and services provided will be detailed on a Service Detail Report. Service reports will be reviewed electronically and signed by the Manager with all action needed agreed upon.</p>
</div>

<h2 class="prop-section-title">CUSTOMIZED TRAINING</h2>
<div contenteditable="true" class="edit-area">
    <p><strong>Your Business, Your People. Are Important to us!</strong></p>
    <p>It is critical to have knowledgeable and informed employees. A successful training program can provide your employees with the information they need to work efficiently. When this is accomplished, it will have a direct impact on your customer retention and profit margins.</p>
    <p>Ecolab understands the importance of providing effective training programs. We will commit to providing every resource we have available to you and your management teams for this purpose.</p>
</div>

<h2 class="prop-section-title">SERVICE AND SUPPORT COMMITMENT</h2>
<div contenteditable="true" class="edit-area">
    <p><strong>G 360 E - SERVICE REPORTS</strong></p>
    <p>Ecolab understands the need for smooth running of customers operations and provide proactive services. Ecolab Service Reports will be presented to your Management and highlight operational factors requiring action such as manpower requirements, product usage, waste and justification for future capital investments.</p>
    <p>All issues identified and services provided will be detailed on the Service Report. Service reports will be reviewed electronically and signed by the Manager with all action needed agreed upon. A copy of the report will be faxed or e-mailed the following day.</p>
    
    <p><strong>EMERGENCY SERVICE COVERAGE</strong></p>
    <ul>
        <li>Telephone follow-up on emergency service requests</li>
        <li>Escalation process to help insure timely issue resolution</li>
        <li>Technical support provided by world-class chemists, microbiologists and engineers</li>
    </ul>
    
    <p><strong>BUSINESS REVIEWS</strong></p>
    <p>Ecolab will conduct regular Business Review with your management, with the objective to evaluate and continually improve upon the services we provide to your property.</p>
    
    <p><strong>IMPLEMENTATION PLAN</strong></p>
    <p>Ecolab will work with you and your team to develop an implementation plan that incorporates reviewing and confirming product selection, KPI’s, training plan, meeting with all relevant parties, preparing MSDS, managing installations, conducting training, and implementing schedule service regime.</p>
</div>
"""

with open("main.js", "r", encoding="utf-8") as f:
    js_content = f.read()

replacement = f"""const proposalTemplates = {{
    vn: {{
        title: "BẢNG ĐỀ XUẤT HỢP TÁC - BUSINESS PROPOSAL",
        lblTo: "Kính gửi:",
        lblDate: "Ngày báo:",
        lblContact: "Người liên hệ:",
        lblFrom: "Người gửi:",
        lblAppendixTitle: "Phụ lục: THỎA THUẬN VỚI KHÁCH HÀNG (Program Terms)",
        sigClient: "Xác nhận của Khách Hàng",
        sigEcolab: "Đại diện CTY TNHH Ecolab VN",
        bodyHtml: `{vn_html}`
    }},
    en: {{
        title: "CLEANING, SANITIZATION AND FOOD SAFETY PROPOSAL",
        lblTo: "To:",
        lblDate: "Date:",
        lblContact: "Contact Person:",
        lblFrom: "Prepared by:",
        lblAppendixTitle: "Appendix: PROGRAM TERMS",
        sigClient: "Customer Confirmation",
        sigEcolab: "Ecolab Representative",
        bodyHtml: `{en_html}`
    }}
}};"""

new_js = re.sub(r'const proposalTemplates = {.*?};', replacement, js_content, flags=re.DOTALL)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(new_js)

print("Proposal updated.")
