# Báo cáo Ngày 4 — gán nhãn, rework và đánh giá pose

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

Đã nhận kết quả chạy Colab từ `Day4-Colab-results.zip` do người gán gửi. Model là `yolo26n-pose.pt`; fine-tune dùng 20 ảnh train và nhãn đã rework, đánh giá dùng 10 ảnh test phát sẵn theo `val` trong `data.yaml`. SHA-256 của đủ 20 file nhãn train trong kết quả Colab khớp bản hiện tại sau chuẩn hóa newline. Gold không nằm trong gói chạy Colab và không được dùng để train; chỉ kết quả đánh giá annotation đã có được dùng để đối chiếu trong báo cáo.

Số dưới đây chép nguyên từ [outputs/eval_model.json](../outputs/eval_model.json). “Chênh” là sau fine-tune trừ baseline; các giá trị mAP dùng thang 0–1.

| Chỉ số | yolo26n-pose gốc | Sau fine-tune | Chênh |
| --- | ---: | ---: | ---: |
| pose_mAP50 | 0.8450 | 0.8450 | 0.0000 |
| pose_mAP50-95 | 0.6853 | 0.6908 | +0.0055 |
| pose_precision | 0.9734 | 0.9792 | +0.0058 |
| pose_recall | 0.8462 | 0.8462 | 0.0000 |
| box_mAP50 | 0.9785 | 0.9600 | −0.0185 |
| box_mAP50-95 | 0.8119 | 0.8041 | −0.0078 |

### Trả lời năm câu hỏi ở cuối notebook

**1. pose_mAP50-95 thay đổi bao nhiêu?**

Tăng 0.0055, tương đương **0.55 điểm phần trăm**. Precision pose tăng 0.58 điểm phần trăm; pose_mAP50 và recall giữ nguyên. Bộ 20 ảnh có nhiều người quay lưng, khớp bị che và người nền nhỏ; ví dụ train_06 và train_13 cho thấy model vẫn khó phục hồi các khớp này sau fine-tune. Trên 10 ảnh test, kết quả là cải thiện nhỏ ở pose và giảm ở box; chưa có nhiều lần chạy hoặc khoảng tin cậy để kết luận mức tăng này ổn định.

**2. Box mAP và pose mAP chênh nhau bao nhiêu?**

Ở mAP50–95, baseline chênh `0.8119 − 0.6853 = 0.1266` (**12.66 điểm phần trăm**); sau fine-tune chênh `0.8041 − 0.6908 = 0.1133` (**11.33 điểm phần trăm**). Box vẫn đạt điểm cao hơn pose: tìm vùng người dễ hơn đặt đúng 17 khớp, đặc biệt ở người nhỏ hoặc các chi bị che. Trong train_13, model tìm đủ ba người nhưng pose người áo xanh chỉ đạt OKS 0.530; bbox được nhận ra không bảo đảm cổ tay và cổ chân đúng. Box_mAP50–95 giảm 0.78 điểm phần trăm sau fine-tune, nên không thể nói mọi mặt của model đều tốt hơn.

**3. Một ảnh test model đoán sai, gọi tên lỗi.**

Chọn **test_03.jpg, người 1 trong nhãn test, người áo số 14 gần camera**: điểm gối phía phải ảnh (`left_knee`) trong ảnh dự đoán lệch về vùng đùi sát yên xe so với khớp gối trên nhãn tham chiếu. Tôi xếp ca này vào **lệch nhẹ**, cần đặt lại đúng khớp; không có bằng chứng chắc về đảo trái/phải hoặc lẫn sang người áo số 3 ở ca này. [Ảnh dự đoán thật](model_evidence/test/test_03.jpg) và [ảnh phủ nhãn test](model_evidence/test/test_03_labels.jpg) cho phép kiểm trực tiếp. Nhãn tham chiếu đặt left_knee tại khoảng `(405, 292)` px; ZIP không có tọa độ dự đoán test dạng JSON nên không ghi sai số pixel của model như một phép đo đã tính.

Một lỗi detector bổ sung ở [test_02.jpg](model_evidence/test/test_02.jpg): model tạo thêm bbox `person 0.31` quanh con chim trên bờ tường phía trái. Đây là nhầm đối tượng/thừa người, được ghi để không bỏ qua lỗi số lượng chỉ vì pose của người thật phía phải tương đối đúng.

**4. Ảnh nào có OKS thấp nhất giữa nhãn của tôi và model? Ai đúng?**

Theo **điểm của từng cặp người–pose trong bảng notebook**, thấp nhất là **train_13.jpg, người 1 trong nhãn hiện tại, người áo xanh sát mép trái, ID CVAT 592**. Người này ghép với người 3 của model: notebook ghi **0.530**, tính lại từ tọa độ lưu trong ZIP được khoảng **0.5298**. Hai người còn lại trong ảnh đạt 0.965 và 0.821, nên OKS trung bình ảnh 13 là 0.772. [Ảnh model](model_evidence/train/train_13.jpg) · [ảnh phủ nhãn](model_evidence/train/train_13_labels.jpg).

`left_wrist` của người áo xanh có confidence model **0.0404**. Theo quy tắc notebook `score <= 0.05 → v=0`, điểm này bị loại khỏi pose đối chiếu; nhãn của tôi giữ điểm ước lượng `(34, 150)` px với **v=1**, vì cổ tay ở cuối cẳng tay vẫn trong khung nhưng bị thân che. Tôi giữ nhãn theo luật visibility của lớp. Hai cổ chân dự đoán cũng gần như đổi phía so với nhãn: left_ankle model `(38.56, 235.82)` so với nhãn `(21, 229)`; right_ankle model `(23.94, 235.09)` so với nhãn `(39, 235)`. Nhãn người này đạt OKS 1.0000 trên những khớp gold có gán, củng cố việc giữ danh tính trái/phải theo nhãn; ảnh người nền mờ nên không khẳng định từng pixel ước lượng bị che đều chính xác.

Cờ 0/1/2 suy từ **confidence model** trong notebook không phải visibility annotation do người gán quyết định. Thiếu dự đoán không phải căn cứ đổi khớp bị che trong khung về v=0, và gold không gán một khớp cũng không thay đổi luật lớp.

**5. Ảnh tôi gán tệ nhất có cũng là ảnh model đoán tệ nhất không?**

Nếu dùng **cặp người thấp nhất** như câu 4, **không trùng**: nhãn sau rework so với gold thấp nhất ở train_06 (0.8905), còn model so với nhãn thấp nhất ở người áo xanh train_13 (0.530). Nếu thống nhất dùng **OKS trung bình những người được ghép trong từng ảnh**, **có trùng ở train_06**: nhãn–gold 0.8905 và model–nhãn 0.630, đều đứng cuối bảng tương ứng. Không so điểm thấp nhất của một người với điểm trung bình của cả ảnh rồi kết luận ảnh khó nhất giống nhau.

| Ảnh | OKS nhãn–gold trung bình sau rework | OKS model–nhãn trung bình | Cặp model–nhãn thấp nhất |
| --- | ---: | ---: | ---: |
| train_06.jpg | 0.8905 | 0.6300 | 0.630 |
| train_13.jpg | 0.9875 | 0.7720 | 0.530 |
| train_18.jpg | 0.8934 | 0.8860 | 0.886 |

Train_06 là người quay lưng, mũ và thân/xe che các mốc mặt và tay phía xa. Model thiếu các điểm mặt và right_wrist theo ngưỡng confidence của notebook; right_elbow lệch khoảng 30 px so với điểm ước lượng trên nhãn. [Ảnh model](model_evidence/train/train_06.jpg) · [nhãn hiện tại](model_evidence/train/train_06_labels.jpg). Cùng khó ở ảnh này gợi ý che khuất làm việc đặt khớp khó cho cả người gán và model; OKS thấp tự nó không chứng minh nhãn sai, nhất là khi gold không gán một số điểm bị che.

### Các ca đối chiếu và kiểm lại kết quả

- **Train_13, người áo xanh:** thiếu dự đoán left_wrist và hai cổ chân gần như đổi phía so với nhãn; giữ quy tắc v1/COCO17, không sửa nhãn theo model.
- **Train_06, người lái xe:** mặt và right_wrist bị che có confidence thấp; vị trí right_elbow lệch. Khớp bị che trong khung vẫn được ước lượng với v1 trên nhãn.
- **Train_03:** model báo **4 người**, nhãn có **2 người**. Tính lại ghép được hai người thật, còn hai dự đoán thừa (model người 2/4); ảnh cho thấy dự đoán trùng người nền và bbox ở búp bê dưới xe. Cổ tay phải người sau (người 2 của nhãn/người 3 model) lệch khoảng **106 px**, đi vào vùng tay người trước: **nhầm người**. [Ảnh model](model_evidence/train/train_03.jpg) · [nhãn](model_evidence/train/train_03_labels.jpg).

Bảng notebook cũng báo train_10 có `model 2 / bạn 1`; ghi nhận thừa một dự đoán, không tự thêm người vào annotation để khớp model. OKS trung bình theo ảnh ở trên chỉ tính những người đã ghép; phải đọc cùng số người thừa/thiếu. Điểm bảng notebook đã làm tròn ba chữ số; [train_model_comparison.json](../outputs/train_model_comparison.json) lưu bảng xếp hạng và phép ghép tính lại từ tọa độ thật cho ba ảnh minh họa.

CSV huấn luyện có **39 epoch được ghi**, trong khi notebook đặt giới hạn 80 epoch và patience 30. Cột pose_mAP50–95 trong CSV cao nhất **0.70230 ở epoch 9/10**, nhưng cuối epoch 39 chỉ còn **0.09008** (box 0.14466), cho thấy quá trình fine-tune về sau kém ổn định. Đây là số ở các lượt validation trong quá trình train; bảng báo cáo dùng **0.6908 từ eval_model.json**, được notebook đánh giá lại với best checkpoint. Gói không có weights, args.yaml hoặc log đầy đủ để xác định chính xác epoch của best checkpoint hay nguyên nhân khác biệt CSV/JSON; không lấy 0.70230 thay cho kết quả đánh giá thực tế và không gán nguyên nhân chắc chắn chỉ từ CSV.

[CSV gốc](model_evidence/results.csv) · [JSON đối chiếu gốc từ Colab](../outputs/train_model_review.json) · [manifest nhập file, SHA-256 và ánh xạ đường dẫn](model_evidence/import_manifest.json). File JSON/ảnh/CSV nhận từ Colab được giữ nguyên byte; ảnh phủ nhãn bổ sung được vẽ từ nhãn hiện tại. Model weights và protected gold không commit.

## 5. Rule evidence về v1/v0

Ở train_09, người ngồi xe quay đầu sang trái: mũ che mắt và phía xa của mặt, nhưng toàn bộ đầu vẫn nằm trong ảnh. Nose/right_eye từng có v0 được phục hồi thành điểm ước lượng dưới mũ với v1; vị trí gần mặt được kiểm bằng crop phóng lớn. Tai gần có đường nét thấy được giữ v2, tai xa bị che dùng v1. COCO gold không gán một số mốc này là thông tin chẩn đoán, không phải căn cứ xóa điểm. [Ảnh gốc cạnh ảnh phủ sau](rework_evidence/train_09_after.jpg).

## 6. Mốc và khả năng kiểm lại

Manifest khóa cũ giữ nguyên trong `reports/label_lock_manifest.json`, tham chiếu commit d9ded1f; hash cũ không mô tả nhãn đã rework. [Manifest sau rework](rework_manifest.json) ghi hash bản export thật, nhãn hiện tại, kết quả trước/sau và gold dùng để đánh giá. Gold vẫn thuộc .gitignore và không commit. Các biên bản checklist/review_partner giữ phần lịch sử tại mốc khóa và bổ sung trạng thái bản nộp cuối sau rework/Colab; những lỗi trong phần lịch sử không phải lỗi còn mở của bản hiện tại.

## 7. Artifact và bản nộp cuối

Đã kiểm đủ 20 file nhãn train, export COCO, visibility JSON/Markdown, mini guideline, eval_vs_gold.json, eval_model.json, báo cáo, biên bản cá nhân và reviewer checklist. [Bảng kiểm artifact](SUBMISSION_CHECKLIST.md) và [log cấu trúc bản hiện tại](pose_validation_after.log) ghi lượt kiểm cuối. Nhãn/export không bị chỉnh khi nhập kết quả model; đủ 20 hash nhãn khớp dữ liệu Colab.

URL nộp VLearn: **https://github.com/duy12345-6789/Day4-KeypointPose-LENGOCNAM**. Chỉ nộp URL fork repository vào biểu mẫu; không tải ZIP, ảnh raw, test labels, gold labels hoặc model weights lên VLearn. Việc truy cập URL không dùng thông tin đăng nhập được kiểm tra ở bản nộp cuối; protected gold và weights không nằm trong commit.
