"""Tạo file Word (.docx) chuẩn biểu mẫu khảo sát Lab Coach khoá AI20K.
Tác giả: Hoàng Thế Phong (2A202603832) — Cặp 2.
"""

import os
import zipfile
import html

def escape(text):
    return html.escape(text)

def create_docx(filename):
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
    
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="word/styles.xml"/>
</Relationships>"""

    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>
        <w:sz w:val="22"/>
        <w:szCs w:val="22"/>
        <w:lang w:val="vi-VN"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
</w:styles>"""

    survey_data = [
        ("title", "KHẢO SÁT: TRẢI NGHIỆM CHUẨN BỊ DẪN NHẬP & ĐIỂM NGHẼN HỌC VIÊN TRƯỚC BUỔI LAB (AI20K)"),
        ("desc", "Chào các anh/chị Lab Coach và Giảng viên! Nhóm nghiên cứu nội bộ lớp L3B đang khảo sát thực tế về việc chuẩn bị dẫn nhập và nắm bắt điểm nghẽn của học viên trước giờ lên lớp. Khảo sát chỉ gồm 9 câu hỏi ngắn (khoảng 2 phút), hoàn toàn bảo mật thông tin. Rất mong nhận được chia sẻ thực tế từ anh/chị để cải thiện trải nghiệm vận hành đào tạo khoá học!"),
        ("sep", ""),
        ("q", "Câu 1: Vai trò chính của anh/chị tại khoá học AI20K là gì? [Trắc nghiệm - Chọn 1]"),
        ("opt", "a) Lab Coach phụ trách phòng thực hành"),
        ("opt", "b) Key Coach / Day Lead"),
        ("opt", "c) Giảng viên đứng lớp chính"),
        ("opt", "d) Trợ giảng (TA)"),
        ("sep", ""),
        ("q", "Câu 2: Trung bình một tuần, anh/chị phụ trách hỗ trợ / giảng dạy bao nhiêu ca học/lab? [Trắc nghiệm - Chọn 1]"),
        ("opt", "a) 1 buổi / tuần"),
        ("opt", "b) 2 – 3 buổi / tuần"),
        ("opt", "c) Trên 3 buổi / tuần"),
        ("sep", ""),
        ("q", "Câu 3: Trước khi vào ca lab/buổi dạy, anh/chị thường mất khoảng bao lâu để chuẩn bị nội dung dẫn nhập hoặc rà soát xem học viên đã học pre-class thế nào? [Trắc nghiệm - Chọn 1]"),
        ("opt", "a) Dưới 10 phút"),
        ("opt", "b) 10 – 20 phút"),
        ("opt", "c) 20 – 35 phút"),
        ("opt", "d) Trên 35 phút"),
        ("opt", "e) Thường vào lớp dạy luôn, không có thời gian chuẩn bị trước"),
        ("sep", ""),
        ("q", "Câu 4: Trước giờ học, anh/chị thường nắm tình hình học viên làm pre-class bằng cách nào? [Hộp kiểm - Chọn nhiều]"),
        ("opt", "a) Lướt xem tin nhắn học viên hỏi trên nhóm Zalo / Discord"),
        ("opt", "b) Vào hệ thống LMS mở xem điểm số / bài nộp"),
        ("opt", "c) Vào lớp hỏi miệng nhanh vài bạn đầu giờ"),
        ("opt", "d) Trao đổi nhanh với các Coach khác trước giờ mở cửa phòng"),
        ("opt", "e) Không có cách nào tra cứu nhanh bức tranh chung của cả lớp"),
        ("opt", "f) Khác"),
        ("sep", ""),
        ("q", "Câu 5: Trong 1 tháng qua, anh/chị có từng gặp tình huống vào ca lab rồi mới phát hiện phần lớn học viên cùng kẹt một khái niệm hoặc lỗi kỹ thuật từ bài pre-class tối qua không? [Trắc nghiệm - Chọn 1]"),
        ("opt", "a) Chưa từng gặp"),
        ("opt", "b) Hiếm khi (1 – 2 lần)"),
        ("opt", "c) Thường xuyên (3 – 5 lần)"),
        ("opt", "d) Rất thường xuyên (hầu như tuần nào cũng gặp)"),
        ("sep", ""),
        ("q", "Câu 6: Ở lần gần nhất gặp tình huống đó, sự việc diễn ra thế nào và ảnh hưởng gì đến ca lab? [Hộp kiểm - Chọn nhiều]"),
        ("opt", "a) Giảng viên / Coach phải dừng lớp 15–30 phút để giảng lại từ đầu kiến thức nền"),
        ("opt", "b) Bị cháy giáo án, học viên không kịp hoàn thành bài lab chính trên lớp"),
        ("opt", "c) Coach bị quá tải vì phải đi giải thích lặp đi lặp lại cùng một lỗi cho từng bàn"),
        ("opt", "d) Học viên hoang mang, nản lòng vì không theo kịp tiến độ"),
        ("opt", "e) Khác"),
        ("sep", ""),
        ("q", "Câu 7: Nếu trước buổi lab 30 phút có một bản tóm tắt nhanh điểm nghẽn của lớp (gọn trong 1 trang), 3 thông tin nào sau đây hữu ích nhất với anh/chị? [Hộp kiểm - Tối đa 3 lựa chọn]"),
        ("opt", "a) Top các câu hỏi trắc nghiệm (Knowledge Check) cả lớp làm sai nhiều nhất"),
        ("opt", "b) Tỷ lệ và danh sách các Mini Lab học viên bấm bỏ qua (Skip) hoặc bỏ dở"),
        ("opt", "c) Đoạn video bài giảng nào học viên hay tua đi tua lại hoặc hỏi trợ giảng nhiều nhất"),
        ("opt", "d) Gợi ý 1 hoạt động / câu hỏi dẫn nhập 5–10 phút đầu giờ để gỡ đúng chỗ nghẽn"),
        ("opt", "e) Cảnh báo độ tin cậy nếu số lượng học viên nộp bài trước giờ quá ít"),
        ("sep", ""),
        ("q", "Câu 8: Điều gì sẽ khiến anh/chị KHÔNG TIN hoặc KHÔNG DÙNG một bản tóm tắt như vậy? [Đoạn văn ngắn]"),
        ("opt", "(Câu trả lời dạng văn bản ngắn / ý kiến đóng góp)"),
        ("sep", ""),
        ("q", "Câu 9: [Khóa điểm Bonus] Sáng/trưa mai (Thứ Bảy 28/11), tụi em có bản chạy thử phân tích log pre-class. Anh/chị có sẵn sàng dành 3–5 phút trải nghiệm và cho nhận xét nhanh không ạ? [Trắc nghiệm - Chọn 1]"),
        ("opt", "a) Sẵn sàng! (Vui lòng để lại SĐT / Zalo / Telegram)"),
        ("opt", "b) Tiếc quá, mai mình có lịch bận mất rồi")
    ]

    body_xml = []
    for item_type, text in survey_data:
        escaped_text = escape(text)
        if item_type == "title":
            p = f"""<w:p>
              <w:pPr>
                <w:jc w:val="center"/>
                <w:spacing w:before="240" w:after="240"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:b/>
                  <w:sz w:val="32"/>
                  <w:szCs w:val="32"/>
                  <w:color w:val="1F497D"/>
                </w:rPr>
                <w:t>{escaped_text}</w:t>
              </w:r>
            </w:p>"""
        elif item_type == "desc":
            p = f"""<w:p>
              <w:pPr>
                <w:spacing w:after="200"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:i/>
                  <w:color w:val="595959"/>
                </w:rPr>
                <w:t>{escaped_text}</w:t>
              </w:r>
            </w:p>"""
        elif item_type == "q":
            p = f"""<w:p>
              <w:pPr>
                <w:spacing w:before="160" w:after="80"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:b/>
                  <w:color w:val="0D233A"/>
                </w:rPr>
                <w:t>{escaped_text}</w:t>
              </w:r>
            </w:p>"""
        elif item_type == "opt":
            p = f"""<w:p>
              <w:pPr>
                <w:ind w:left="400"/>
                <w:spacing w:after="40"/>
              </w:pPr>
              <w:r>
                <w:t>{escaped_text}</w:t>
              </w:r>
            </w:p>"""
        elif item_type == "sep":
            p = """<w:p><w:pPr><w:spacing w:after="100"/></w:pPr></w:p>"""
        body_xml.append(p)

    doc_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {"".join(body_xml)}
  </w:body>
</w:document>"""

    with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/_rels/document.xml.rels", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>""")
        z.writestr("word/styles.xml", styles)
        z.writestr("word/document.xml", doc_xml)

    print(f"File created successfully: {filename}")

if __name__ == "__main__":
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "evidence", "survey", "Khao_sat_Lab_Coach_AI20K.docx")
    create_docx(out_path)
