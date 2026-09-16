# Báo cáo Ngày 4 — phản hồi OKS và rework

Họ tên: LÊ NGỌC NAM. Hình thức: cá nhân. Ngày: 2026-09-16.

## 1. Nhãn của tôi

Bản trước rework là nhãn đã khóa ở commit `d9ded1f`. Protected-release gold đã có đủ 20 file trong `gold/labels/train/` khi bắt đầu lượt này. Gold được dùng để đánh giá/chẩn đoán, không dùng để train model.

| Chỉ số | Trước rework | Sau rework |
| --- | ---: | ---: |
| Số ảnh | 20 | 20 |
| Số skeleton | 27 | 29 |
| v=2 / v=1 / v=0 | 334 / 93 / 32 | 314 / 146 / 33 |
| Thời gian trung bình/ảnh | Không có log thời gian thực tế | Không có log thời gian thực tế |

Mục tiêu khoảng 4 phút/ảnh là mục tiêu thao tác, không được ghi thành thời gian đã đo.

Ba khớp có tỷ lệ v=1 cao nhất sau rework:

1. `left_ear`: 19/29 = 65.52%.
2. `right_ear`: 16/29 = 55.17%.
3. `left_eye`: 13/29 = 44.83%.

Tai/mắt hay bị mũ, tóc và kính che; ảnh 04, 15, 20 minh họa rõ. Hông và các chi sau xe/bàn khó xác định vị trí giải phẫu dù tỷ lệ v1 không đứng đầu; tỷ lệ bị che không đồng nghĩa sai số tọa độ lớn nhất.

[Visibility trước](visibility_report_before.md) · [Visibility sau](visibility_report.md).

## 2. Chấm với gold

Chạy cùng evaluator và cùng gold cho cả hai lần; số dưới đây chép từ JSON, không sửa file kết quả để nâng điểm.

```bash
python3 tools/evaluate_pose_annotations.py --pred dataset/labels/train --gold gold/labels/train --images dataset/images/train --out outputs/eval_vs_gold.json
```

| Chỉ số | Trước rework | Sau rework |
| --- | ---: | ---: |
| OKS trung bình | 0.9484 | 0.9539 |
| OKS@0.50 | 0.931 | 1.0 |
| OKS@0.75 | 0.931 | 1.0 |
| Số người gold | 29 | 29 |
| Ghép được | 27 | 29 |
| Thiếu người | 2 | 0 |
| Thừa người | 0 | 0 |
| Lỗi `dao_trai_phai` | 0 | 0 |
| Lỗi `nham_nguoi` | 0 | 0 |
| Lỗi `xoa_khop_bi_che` | 0 | 0 |
| Lỗi `thieu_khop` | 0 | 0 |
| Lỗi `truot_han` | 0 | 0 |
| Lỗi `lech_nhe` | 3 | 0 |
| Chẩn đoán `co_khac_gold` | 38 | 53 |
| Chẩn đoán `gold_khong_gan_nhan` | 58 | 68 |

[JSON trước](../outputs/eval_vs_gold_before.json) · [JSON sau](../outputs/eval_vs_gold_after.json) · [JSON hiện tại](../outputs/eval_vs_gold.json).

OKS trung bình tăng 0.0055; OKS@0.75 tăng 6.9 điểm phần trăm. Mean OKS trước tính trên 27 cặp đã ghép, sau tính trên 29 cặp; phải đọc kèm số thiếu người và OKS@0.75 để hiểu thay đổi độ đầy đủ.

### Thứ tự xử lý finding

Đã đọc theo thứ tự đảo trái/phải → nhầm người → thiếu/thừa người → xóa khớp bị che → trượt hẳn → lệch nhẹ. Evaluator không báo đảo trái/phải, nhầm người, xóa khớp bị che hay trượt hẳn ở bản trước; vấn đề chính theo OKS là hai người thiếu và ba lệch nhẹ. Kiểm ảnh vẫn xác nhận cổ tay người trái ở ảnh 04 đi sang vùng găng người phải, dù evaluator chỉ phân loại lệch nhẹ. Do đó ưu tiên sửa danh tính chi theo hình trước, rồi thêm người và sửa tọa độ.

Không có lỗi đảo trái/phải được evaluator phân loại trong cả 20 ảnh trước/sau. Cảnh báo hướng mắt ở ảnh 02 không được dùng để đảo thân vì các mắt là điểm ước lượng khi người quay đầu.

### Tôi đã sửa gì trong CVAT

Đã sửa task 7 qua API annotation của CVAT: PATCH update/create đều HTTP 200, giữ IDs của 27 skeleton và các điểm cũ; thêm hai skeleton IDs 592/593. Sau đó dùng exporter thật `COCO Keypoints 1.0` của CVAT, chuyển lại bằng `tools/coco_kp_to_yolo_pose.py` và chạy evaluator trên bản chuyển đổi này. Số đo sau không lấy từ bản đề xuất.

Số người sau là thứ tự dòng YOLO trong **export hiện tại**. Export có thể sắp xếp lại người, nên bảng giữ cả thứ tự trước và sau; ID CVAT ổn định giúp tìm đúng người.

| Ảnh | Người trước → sau / ID CVAT | Khớp hoặc thao tác | Lý do |
| --- | --- | --- | --- |
| train_01.jpg | 1 → 2 / 106 | `left_ear`, `right_ear`, `left_elbow`, `left_hip`, `right_hip`, `left_knee`, `right_knee` | Tai/tóc, khuỷu/pizza, hông/tạp dề bị che dùng v1; gối thật nằm dưới khung dùng v0. |
| train_01.jpg | 2 → 1 / 107 | `left_ear`, `right_ear`, `right_wrist`, `left_knee`, `right_knee` | Đưa tai về mức giải phẫu; cổ tay phải sau mép pizza; gối thật ngoài ảnh. |
| train_03.jpg | 1 → 2 / 178 | `left_wrist`, `left_knee`, `left_ankle` | Người sau bị người trước/xe che: giữ cổ tay, gối và cổ chân trái với v1. |
| train_04.jpg | 1 → 2 / 196 | `left_ear`, `right_ear` | Mũ che tai: v1, giữ chấm ước lượng. |
| train_04.jpg | 2 → 1 / 214 | `left_wrist`, `left_ear`, `right_ear` | Cổ tay thuộc cẳng tay người bên trái, không lấy vùng găng người bên phải; tai sau mũ dùng v1. |
| train_06.jpg | 1 → 1 / 250 | `right_shoulder` | Vai thật ở áo người lái sau tựa lưng, không nằm trên mép tựa xe; v1 ước lượng. |
| train_08.jpg | 1 → 1 / 286 | `right_ankle` | Cổ chân ở gấu quần/giày, không ở giữa cẳng chân. |
| train_09.jpg | 1 → 1 / 304 | `nose`, `left_eye`, `right_eye`, `left_ear`, `right_ear`, `right_shoulder`, `right_elbow`, `right_wrist` | Mốc mặt phía dưới mũ theo đầu quay trái; phục hồi mặt/tay bị che trong khung bằng v1, giữ tai gần thấy được v2. |
| train_11.jpg | 1 → 1 / 340 | `left_eye`, `right_eye`, `left_knee`, `right_knee` | Kính che mắt và bàn che gối tư thế ngồi: v1; cổ chân thật ngoài ảnh giữ v0. |
| train_12.jpg | 1 → 1 / 341 | `left_hip`, `right_hip`, `right_knee`, `right_ankle` | Áo/hộp che hông và gối: v1; cổ chân thấy được ở gấu quần/giày. |
| train_13.jpg | 1 → 2 / 376 | `left_hip`, `right_hip`, `left_knee`, `right_knee` | Áo vest che hông: v1; gối thật dưới mép ảnh, không đặt lên túi/đùi. |
| train_14.jpg | 1 → 1 / 394 | `right_hip`, `right_knee` | Hông/gối người ngồi bị áo và ô che: v1. |
| train_14.jpg | 2 → 2 / 412 | `left_ear`, `right_ear` | Mũ/tóc che tai người đứng: v1, giữ tọa độ ước lượng. |
| train_15.jpg | 1 → 2 / 430 | `left_ear` | Ước lượng tai ở mức đầu, không đặt lên phần cao mũ. |
| train_15.jpg | 2 → 1 / 431 | `left_eye`, `left_ear`, `right_ear`, `right_elbow` | Ước lượng khuỷu phía xa sau thân; tai dưới mũ và mắt sau kính dùng v1. |
| train_16.jpg | 2 → 1 / 467 | `right_eye`, `right_ear` | Đầu quay khỏi camera: mắt/tai phía xa sau tóc dùng v1. |
| train_20.jpg | 1 → 1 / 574 | `left_eye`, `right_eye`, `left_ear`, `right_ear` | Kính/mũ che mắt và tai: v1, không xóa điểm trong khung. |
| train_13.jpg | Chưa có → 1 / 592 | Thêm đủ 17 điểm cho người áo xanh sát mép trái | Gold chỉ ra người thiếu; ảnh phóng lớn xác nhận người riêng. Khớp bị che vẫn v1; cổ chân ngoài ảnh của người áo beige v0. |
| train_13.jpg | Chưa có → 3 / 593 | Thêm đủ 17 điểm cho người áo beige sau/trái người chính | Gold chỉ ra người thiếu; ảnh phóng lớn xác nhận người riêng. Khớp bị che vẫn v1; cổ chân ngoài ảnh của người áo beige v0. |

[Chi tiết từng tọa độ/cờ trước–sau và IDs](rework_changes.json). Tổng 57 cập nhật điểm trên 17 người hiện có và thêm hai người với đủ 17 điểm.

Ba lệch nhẹ ban đầu đã xử lý: train_01 người nam `right_wrist` sau pizza; train_04 người bên trái `left_wrist` sau người phía trước; train_15 người bên phải `right_elbow` sau thân. Các lệch nhẹ trước là 26, 44 và 34 px theo finding của evaluator.

### Kiểm lại và giới hạn

Ảnh phủ sau rework đã tạo cho đủ 20 ảnh tại `outputs/vis_train/`; các cặp ảnh gốc/ảnh phủ thật sau export nằm trong [rework_evidence](rework_evidence/train_13_after.jpg). Đã kiểm chuyển đổi: 20/20 file, 29 skeleton, COCO17/51 số và YOLO56 số, visibility/tọa độ khớp dữ liệu CVAT sau làm tròn. Giữ nguyên những lệch nhỏ chưa có bằng chứng đủ chắc ở ảnh 05, 17, 19.

`check_pose_labels.py` có 0 lỗi cấu trúc và 8 cảnh báo. Các cảnh báo v0 do bbox skeleton không chạm mép trong ảnh cắt ở đùi/chân (01/04/10/13), không tự chứng minh khớp còn trong ảnh. Hai cảnh báo hướng mắt ở 02 đã đối chiếu người quay đầu; không đảo vai/hông để xóa cảnh báo.

Sau rework mọi cặp đạt OKS ≥0.75 và không còn finding lỗi vị trí/thiếu người của evaluator. Còn 53 chẩn đoán cờ khác gold và 68 chẩn đoán gold không gán; không phải lỗi bị trừ OKS. Không đổi khớp trong ảnh về v0 chỉ để khớp với COCO gold.

## 3. Kiểm chéo

Không áp dụng: bài cá nhân, không có partner hay bảng so sánh độc lập. Các agent hỗ trợ kiểm ảnh thuộc cùng lượt làm việc bằng AI; không được ghi thành một bạn cùng nhóm.

Quy tắc evidence đã dùng: nếu vai–cẳng tay cho thấy cổ tay còn trong ảnh nhưng bị thân/xe/người che, giữ chấm ước lượng và v1; chỉ v0 khi khớp thật sự nằm ngoài mép ảnh.

## 4. Model

Không chạy train, fine-tune hoặc đánh giá model trong phạm vi rework này; không có số liệu mAP để điền. Gold chỉ là đầu vào evaluator annotation, không được đưa vào dataset train hay huấn luyện model. Những câu hỏi so model trước/sau trong template nằm ngoài yêu cầu hiện tại và chưa có dữ liệu.

## 5. Rule evidence về v1/v0

Ở train_09, người ngồi xe quay đầu sang trái: mũ che mắt và phía xa của mặt, nhưng toàn bộ đầu vẫn nằm trong ảnh. Nose/right_eye từng có v0 được phục hồi thành điểm ước lượng dưới mũ với v1; vị trí gần mặt được kiểm bằng crop phóng lớn. Tai gần có đường nét thấy được giữ v2, tai xa bị che dùng v1. COCO gold không gán một số mốc này là thông tin chẩn đoán, không phải căn cứ xóa điểm. [Ảnh gốc cạnh ảnh phủ sau](rework_evidence/train_09_after.jpg).

## 6. Mốc và khả năng kiểm lại

Manifest khóa cũ giữ nguyên trong `reports/label_lock_manifest.json`, tham chiếu commit d9ded1f; hash cũ không mô tả nhãn đã rework. [Manifest sau rework](rework_manifest.json) ghi hash bản export thật, nhãn hiện tại, kết quả trước/sau và gold dùng để đánh giá. Gold vẫn thuộc .gitignore và không commit. Các biên bản checklist/review_partner trước đó là lịch sử tại mốc khóa, không phải trạng thái lỗi còn mở sau lượt này.
