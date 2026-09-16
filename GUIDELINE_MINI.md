# Mini guideline — bài cá nhân LÊ NGỌC NAM

Người gán: LÊ NGỌC NAM. Người kiểm: Codex hỗ trợ kiểm tra ảnh phủ. Ngày: 2026-09-16.

> Các số liệu và phát hiện ban đầu dưới đây thuộc mốc khóa `d9ded1f`. Protected release đã mở cho lượt rework tiếp theo; trạng thái sửa và chỉ số mới nằm trong [REPORT.md](reports/REPORT.md).

Phạm vi: kiểm tra bản nhãn người gán đã hoàn thành; không gán lại 18 ảnh. Các quy tắc dưới đây dùng để đánh giá nhãn hiện tại. Những điểm chưa tuân thủ được ghi trong [biên bản tự kiểm](reports/review_partner.md), chưa sửa trong bản khóa.

## 1. Luật bắt buộc

- Dùng đúng 17 tên và thứ tự COCO trong [schema chung](assets/schema/coco17-keypoints.json).
- Mỗi người phải có đủ 17 mục keypoint; không xóa mục bị che.
- Trái/phải theo cơ thể người, không theo trái/phải màn hình.
- Khớp thấy được: `v=2`. Khớp bị che nhưng còn trong khung: `v=1`, giữ tọa độ ước lượng.
- Khớp thật sự ngoài khung: `v=0`. Khi chuyển sang YOLO, tọa độ mục này là `(0, 0)`.
- Không dùng `Hidden` (`h`). Export không cho phép chứng minh người gán đã dùng hay không dùng phím này; chỉ kiểm được kết quả tọa độ và cờ.
- Ưu tiên đúng khớp và đúng người; không kéo điểm sang vật che chỉ để điểm nằm trên vùng nhìn thấy.

## 2. Quy tắc cho các tình huống khó

Ảnh minh họa là ảnh gốc cạnh ảnh phủ do `tools/visualize_pose.py` tạo từ export CVAT, không phải ảnh chụp giao diện CVAT. Ảnh phủ giữ nguyên nhãn hiện tại, kể cả lỗi được ghi bên dưới.

| Tình huống | Quy tắc dùng để kiểm | Vì sao / ví dụ |
| --- | --- | --- |
| Hông dưới quần áo dài | Nếu đường nét cho phép định vị khớp rõ, dùng `v=2`; nếu áo rộng/tạp dề che vị trí cụ thể, ước lượng theo thân và đùi, dùng `v=1`. | Không dùng mép áo làm khớp hông. [Người mặc tạp dề, train_01](reports/review_evidence/hip_apron.jpg). Bản hiện tại còn cần rà cờ hông. |
| Tai bị tóc hoặc mũ che | Tai thấy được dùng `v=2`; không nhìn thấy tai thì đặt vị trí giải phẫu ước lượng với `v=1`, không đặt lên vỏ mũ. | [Mũ bảo hiểm train_04](reports/review_evidence/helmet_ears.jpg). Có điểm tai hiện dùng `v=2` dù bị mũ che. |
| Người bị cắt ở mép ảnh | Xét từng khớp. Khớp ngoài ảnh dùng `v=0`; khớp trong ảnh bị che vẫn dùng `v=1`. Không đặt khớp ngoài ảnh lên mép ảnh. | [Phần chân bị cắt, train_07](reports/review_evidence/frame_crop.jpg). Phân biệt với đầu gối đặt gần mép dưới ở train_01. |
| Cổ tay sau tay lái hoặc thân người | Ước lượng ở cuối cẳng tay của đúng người và dùng `v=1`; không lấy tay lái/găng tay người khác làm mốc. | [Cổ tay bị che, train_03](reports/review_evidence/hidden_wrist.jpg). `left_wrist` người sau hiện là `v=0` dù trong khung. |
| Hai người chồng lên nhau | Lần theo vai → khuỷu → cổ tay và hông → gối → cổ chân của từng người; người sau vẫn giữ 17 mục, phần bị che dùng `v=1`. | [Hai người train_03](reports/review_evidence/overlapping_people.jpg); [vùng tay train_04](reports/review_evidence/wrist_person_mix.jpg). |
| Người nhỏ | Không tự đặt ngưỡng loại theo pixel cho 20 ảnh core. Người phân biệt được trong ảnh vẫn cần skeleton; ghi rõ nếu không xác định được chi tiết. | [Người nhỏ train_19](reports/review_evidence/smaller_person.jpg). Các người nền train_13 cần được ghi vào lượt kiểm độ đầy đủ. |

## 3. Ba ca mơ hồ đã gặp

### Ca 1 — train_02.jpg, người 1, các điểm mặt

- Mơ hồ: người đạp xe quay đầu khỏi camera, mũ và tóc che các mốc mặt; hai mắt trong export là tọa độ ước lượng.
- Cách kiểm: giữ danh tính trái/phải theo thân và đường đi các chi; không đảo vai/hông chỉ vì cảnh báo dựa trên hai mắt.
- Vì sao: cảnh báo hướng mắt không đủ kết luận đảo trái/phải khi các điểm mắt đều `v=1`.
- Hậu quả nếu quyết ngược: có thể đảo cả phía cơ thể vốn đúng hoặc dạy model nhận mốc trên mũ như mốc mặt.
- Kết quả bản hiện tại: chưa xác nhận lỗi đảo thân; vị trí đầu là vùng cần kiểm thêm nếu được phép mở nhãn.

### Ca 2 — train_03.jpg, người sau bên trái (dòng YOLO 1, COCO id 4), left_wrist

- Mơ hồ: cổ tay bị người trước che; khó định vị chính xác trên ảnh.
- Cách kiểm: đây là khớp trong khung bị che, phải có tọa độ ước lượng với `v=1`.
- Vì sao: sự che khuất không có nghĩa là cổ tay ra ngoài khung; export hiện có tọa độ `(272.93, 214.39)` nhưng cờ `v=0`.
- Hậu quả nếu quyết ngược: điểm bị loại khỏi học keypoint thay vì học tư thế có che khuất.
- Kết quả bản hiện tại: ghi nhận lỗi cờ, chưa sửa tọa độ hoặc visibility.

### Ca 3 — train_09.jpg, người 1, nose và right_eye

- Mơ hồ: người quay lưng; các mốc mặt không nhìn thấy.
- Cách kiểm: ước lượng vị trí thuộc đầu người và dùng `v=1` nếu còn trong khung.
- Vì sao: đầu nằm giữa ảnh; `v=0` của nose/right_eye không thể được giải thích bằng cắt mép ảnh. [Ảnh đối chiếu](reports/review_evidence/rear_head_v0.jpg).
- Hậu quả nếu quyết ngược: model mất các điểm mặt ở tư thế quay lưng; báo cáo visibility đánh đồng bị che với ngoài ảnh.
- Kết quả bản hiện tại: lỗi được ghi trong biên bản; nhãn được giữ nguyên theo phạm vi tự kiểm.

## 4. Visibility tại mốc khóa và bài cá nhân

- Đã tạo [bảng visibility trước rework](reports/visibility_report_before.md) và [JSON trước rework](outputs/visibility_report_before.json).
- Tổng 20 ảnh, 27 skeleton: `v=2: 334`, `v=1: 93`, `v=0: 32`.
- Tai trái có tỷ lệ `v=1` cao nhất: 11/27, khoảng 41%. Hông trái 7/27 so với hông phải 3/27 là tín hiệu cần soi ảnh, không tự chứng minh sai.
- So sánh với partner: **không áp dụng**, theo yêu cầu làm cá nhân. Không có bảng đối chiếu hay điểm chấm của partner.
- Quy tắc cần làm rõ: mặt quay lưng vẫn ở trong khung; điểm bị che dùng `v=1`, không dùng `v=0`.

## 5. Mốc khóa nhãn ban đầu

Commit cuối lượt kiểm khóa nguyên export người gán và 20 file YOLO chuyển đổi. Hash từng file nằm trong [manifest](reports/label_lock_manifest.json). Sau commit không chỉnh nhãn cho tới protected release. Mốc này bảo toàn bài nộp; không phải xác nhận rằng toàn bộ kiểm hình dáng đã đạt. Các phát hiện còn mở được giữ trong biên bản tự kiểm.

## 6. Rework sau protected release

Đã đánh giá gold, sửa trong CVAT, export thật và convert lại sau khi người dùng yêu cầu lượt rework. Bản hiện tại có 20 ảnh, 29 skeleton; chỉ số trước–sau và từng lỗi đã sửa nằm trong [REPORT.md](reports/REPORT.md), hash hiện tại trong [rework manifest](reports/rework_manifest.json). Manifest khóa cũ giữ nguyên để truy lại nhãn tại commit `d9ded1f`, không mô tả hash nhãn mới. Khớp bị che nhưng trong ảnh vẫn giữ `v=1` và chấm ước lượng dù gold COCO không gán; không dùng gold để train.
