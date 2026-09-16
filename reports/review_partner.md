# Biên bản tự kiểm — bài cá nhân Ngày 4

Người gán: LÊ NGỌC NAM. Người kiểm: Codex hỗ trợ kiểm ảnh gốc và ảnh phủ. Ngày: 2026-09-16.

> Phần đến “Kết luận và khóa” ghi bản khóa `d9ded1f`, trước protected-release rework. Các trạng thái “chưa sửa” thuộc mốc đó; phần “Kiểm bản nộp sau rework và Colab” cuối file ghi trạng thái hiện tại.

**Partner: không áp dụng.** Người gán làm cá nhân theo yêu cầu; không có kiểm chéo độc lập, không chạy `--compare`, không tạo bảng giả hoặc chấm với partner/gold.

Phạm vi là bản export người gán đã hoàn thành. Không sửa annotation trong COCO hoặc CVAT. Đã chuyển nguyên cờ và tọa độ dùng được sang 20 file YOLO bằng `tools/coco_kp_to_yolo_pose.py`; công cụ đặt tọa độ các mục `v=0` về `(0,0)` đúng định dạng YOLO.

## Bằng chứng và kiểm tra

- Export: `annotations/coco_keypoints/person_keypoints_default.json`.
- 20/20 ảnh có file nhãn, 27 skeleton. Mỗi skeleton có 17 bộ ba/51 số COCO, mỗi dòng YOLO 56 số; `num_keypoints` đúng số điểm `v>0`.
- Tên/thứ tự COCO17 và kích thước ảnh khớp. [data.yaml](../data.yaml) có `kpt_shape: [17, 3]`.
- `check_pose_labels.py`: **0 lỗi cấu trúc, 7 cảnh báo**, exit code 0. [Log đầy đủ](pose_validation.log).
- [Visibility trước rework](visibility_report_before.md): `v=2: 334`, `v=1: 93`, `v=0: 32`; [JSON trước rework](../outputs/visibility_report_before.json) có `comparison: null`.
- [Ảnh phủ tổng quan 20 ảnh](review_evidence/train_overview.jpg), ảnh riêng ở `outputs/vis_train/`. Các cặp ảnh gốc/ảnh phủ trong `review_evidence/` là bằng chứng từ export, không phải screenshot giao diện CVAT.

## Các phát hiện

“Người thứ” là thứ tự dòng YOLO/annotation COCO trong ảnh; mô tả vị trí giúp tìm đúng người. Cách xử lý là đề nghị cho lúc được phép mở nhãn, **chưa được áp dụng**.

| Ảnh | Người thứ / COCO id | Khớp | Hiện trạng / loại lỗi | Cách xử lý đề nghị và trạng thái |
| --- | --- | --- | --- | --- |
| train_01.jpg | 1/id 1, nữ bên trái; 2/id 2, nam bên phải | left_knee, right_knee | Các điểm `v=2` ở y≈417–420 sát mép dưới, trong khi ảnh cắt ở đùi; nghi điểm trôi khỏi khớp và nhầm outside. | Khi mở nhãn, xác nhận vị trí giải phẫu của gối; gối dưới ảnh phải là `v=0`, không đặt lên mép. Chưa sửa. |
| train_01.jpg | 1/id 1, nữ bên trái | left_ear, right_ear; left_hip, right_hip | Tai sau tóc và hông dưới tạp dề đang dùng `v=2`; cờ chưa nhất quán với quy tắc bị che. | Kiểm khả năng thấy đúng landmark; nếu bị che thì giữ vị trí ước lượng và dùng `v=1`. Chưa sửa. |
| train_02.jpg | 1/id 3 | left/right_shoulder, left/right_hip; các điểm mặt | Hai cảnh báo hướng vai/hông so với mắt. Cả hai mắt `v=1`, người quay đầu; chưa xác nhận đảo thân. Mốc mặt ước lượng cần xem kỹ. | Không tự đảo trái/phải theo heuristic. Kiểm theo thân và chi, rồi kiểm mốc dưới mũ. Đây là cảnh báo, chưa kết luận lỗi đảo thân. |
| train_03.jpg | 1/id 4, người sau bên trái | left_wrist | **Xác nhận lỗi visibility:** tọa độ export `(272.93,214.39)` nằm trong ảnh nhưng cờ `v=0`; cổ tay bị người trước che. | Giữ tọa độ ước lượng thuộc đúng cẳng tay với `v=1`, không xóa. Chưa sửa. [Ảnh](review_evidence/hidden_wrist.jpg). |
| train_04.jpg | 2/id 7, người bên trái | left_wrist | **Lẫn người:** điểm `(366.09,353.31)` đi sang vùng găng/tay người bên phải; tay người bên trái đi ra sau cơ thể người kia. | Lần theo cẳng tay người bên trái, đặt cổ tay riêng bị che với `v=1`. Chưa sửa. [Ảnh](review_evidence/wrist_person_mix.jpg). |
| train_04.jpg | 1/id 6 bên phải; 2/id 7 bên trái | left_ear, right_ear | Tai được đặt `v=2` tại vùng mũ, trong khi tai bị mũ che. | Phân biệt mốc tai với vỏ mũ; ước lượng tai và dùng `v=1` nếu không thấy. Chưa sửa. [Ảnh](review_evidence/helmet_ears.jpg). |
| train_04.jpg | Hai người | Các mục `v=0` | Hai cảnh báo “người nằm giữa ảnh” của checker. Ảnh cắt phần dưới người; không đủ kết luận mọi `v=0` là sai. | Xét từng khớp thật sự ngoài ảnh; không đổi hàng loạt `v=0` sang `v=1` chỉ để xóa cảnh báo. |
| train_05.jpg | 1/id 8 | left_ankle | Cổ chân trái bị che đang đặt gần cẳng chân phải, cần kiểm vị trí giày chân phía sau. | Giữ `v=1`, lần theo chân trái trước khi chỉnh. Đây là điểm cần xem thêm, chưa sửa. |
| train_06.jpg | 1/id 9 | right_shoulder | **Điểm trôi sang vật:** `(408.59,202.97,2)` nằm trên mép tựa lưng xe máy thay vì vai áo người lái. | Kiểm vai phía xa thuộc áo xanh; nếu tựa lưng che thì dùng vị trí ước lượng và `v=1`. Chưa sửa. |
| train_07.jpg | 1/id 10 | left_hip, right_hip | Hông dưới áo khoác đỏ rộng đang `v=2`, cần áp dụng nhất quán quy tắc hông bị che. | Rà `v=1`/`v=2` theo khả năng định vị khớp; cổ chân ngoài mép dưới có thể giữ `v=0`. Chưa sửa. |
| train_08.jpg | 1/id 11 | right_ankle | **Điểm trôi khỏi khớp:** `(135.88,420.57,2)` nằm trên cẳng chân; gấu quần/cổ chân thấy được thấp hơn, khoảng y450–460. | Khi được mở nhãn, chuyển điểm về khớp cổ chân thực, không lấy cẳng chân làm mốc. Chưa sửa. |
| train_09.jpg | 1/id 12 | nose, right_eye | **Xác nhận lỗi visibility:** đầu nằm trong khung, người quay lưng; hai điểm không nhìn thấy hiện là `v=0`. | Ước lượng mốc mặt trong đầu và dùng `v=1`. Chưa sửa. [Ảnh](review_evidence/rear_head_v0.jpg). |
| train_09.jpg | 1/id 12 | right_elbow, right_wrist | Cánh tay phía xa bị thân/túi/xe che đang dùng `v=0`; cổ tay còn có tọa độ mặc định xa khỏi cẳng tay trong export. | Kiểm vị trí ước lượng đúng tay và dùng `v=1` nếu còn trong khung. Chưa sửa. |
| train_10.jpg | 1/id 13 | left/right_knee, left/right_ankle | Checker cảnh báo 4 mục `v=0`; người cúi về camera, khung cắt phía dưới. Chưa có bằng chứng các khớp này còn trong ảnh. | Có thể là outside hợp lệ; không xem cảnh báo là lỗi đã xác nhận. Giữ nguyên. |
| train_11.jpg | 1/id 14 | left_knee, right_knee | Người ngồi phía sau bàn; gối có thể nằm trong khung nhưng bị bàn che, hiện `v=0`. Cổ chân có thể thật sự dưới khung. | Kiểm tư thế ngồi và mép ảnh từng khớp; không đổi cả gối/cổ chân cùng nhau. Chưa sửa. |
| train_12.jpg | 1/id 15 | right_ankle; right_knee | **Cổ chân trôi lên cẳng chân:** `(168.07,440.07,2)` ở trên vị trí giày/gấu quần khoảng y485–505. Gối phải nằm chỉ khoảng 14 px dưới hông, cần rà tư thế ngồi và vật che. | Định vị lại khớp thực khi được mở nhãn; dùng `v=1` nếu hộp/xe che. Chưa sửa. |
| train_13.jpg | Người nền chưa có dòng/id | Toàn bộ skeleton | **Xác nhận thiếu người:** một người áo beige phía sau/trái người chính, khoảng xyxy `[84,16,162,281]`, và một người áo xanh sát trái, khoảng `[13,95,78,251]`. Export chỉ có người chính. | Theo quy tắc mọi người, cần skeleton riêng khi được mở nhãn. Không tự thêm vào bản khóa. |
| train_13.jpg | 1/id 16 | Hông và gối người chính | Hông dưới áo vest dài đang `v=2`; gối gần mép dưới có thể trùng túi/đùi. | Kiểm lại giải phẫu, cắt khung và visibility từng khớp. Cần xem thêm, chưa sửa. |
| train_14.jpg | 1/id 17 ngồi; 2/id 18 đứng | Hông/gối người ngồi; tai người đứng | Khớp sau áo rộng, ô và vùng mũ/tóc có cờ `v=2`; một số khớp khuỷu/cổ tay cần soi kỹ. | Rà khả năng thấy landmark và liên kết chi của từng người. Chưa xác nhận đảo trái/phải hoặc lẫn người ở ảnh này; chưa sửa. |
| train_15.jpg | 1/id 19 bên trái; 2/id 20 bên phải | left_ear người trái; right_ear người phải | **Tai đặt lên phần cao mũ:** điểm tai nằm cao hơn mức giải phẫu tai. | Ước lượng tai ở mức đầu thích hợp với `v=1` nếu mũ/tóc che. Chưa sửa. |
| train_15.jpg | 2/id 20 | left_eye, left_ear | `v=2` ở vùng mắt/tai bị kính/mũ che, cần nhất quán quy tắc visibility. | Rà landmark thấy được hay chỉ là vật che; khớp không thấy dùng `v=1`. Chưa sửa. |
| train_16.jpg | 2/id 22, người bên phải | right_eye, right_ear; left_wrist | Điểm mắt/tai `v=2` ở vùng bị che; cổ tay trái có lệch nhẹ cần soi lại. | Kiểm mốc mặt thuộc người và cờ; lệch cổ tay chưa đủ chắc để kết luận sửa cụ thể. Chưa sửa. |
| train_17.jpg | 1/id 23 | left_elbow | Lệch nhẹ quanh khuỷu cần xem thêm; chưa thấy lỗi lẫn người, đảo thân hoặc xóa điểm bị che. | Khi được mở nhãn, kiểm tâm khớp khuỷu theo cánh tay. Chưa xác nhận lỗi lớn, chưa sửa. |
| train_18.jpg | 1/id 24 | 17 điểm | Không phát hiện bốn loại lỗi mục tiêu trong lượt xem ảnh gốc/ảnh phủ này. | Giữ nguyên; nhận xét này không phải chấm chất lượng với gold. |
| train_19.jpg | 2/id 26, người nhỏ bên trái | left_wrist, right_wrist | Hai cổ tay có lệch nhẹ cần xem thêm; không thấy người bị bỏ sót hoặc lẫn người. | Kiểm khớp cổ tay, tránh đặt lên bàn tay. Chưa xác nhận lệch lớn, chưa sửa. |
| train_20.jpg | 1/id 27 | left_eye, right_eye, left_ear, right_ear | Các điểm `v=2` tại vùng bị kính/mũ/tóc che; visibility cần nhất quán với quy tắc khớp không nhìn thấy. | Ước lượng mốc giải phẫu với `v=1` nếu không thấy; không dùng cạnh mũ/kính thay khớp. Chưa sửa. |

## Phủ đủ lượt kiểm 20 ảnh

Đã xem ảnh gốc và ảnh phủ cho train_01–20, kiểm cả bốn nhóm: trái/phải, nhầm người, điểm trôi khỏi khớp và mất điểm bị che. 27 là số skeleton **trong bản nộp**, không phải xác nhận rằng toàn bộ người trong ảnh đều được gán.

Không xác nhận đảo trái/phải toàn thân trong lượt kiểm; lẫn người rõ ở train_04; điểm trôi rõ ở train_06/08/12/15; outside sai cho điểm bị che rõ ở train_03/09. train_13 thiếu hai người nền. Các nhận xét chưa chắc chắn được ghi riêng, không tự sửa theo cảnh báo.

Các audit chi tiết theo nhóm ảnh được lưu trong `review_evidence/audit_train_*.json`; đây là kiểm tra hỗ trợ bằng AI cho bài cá nhân, không phải kiểm chéo với một bạn cùng nhóm.

## Kết luận và khóa

Bản nhãn **đạt định dạng**, nhưng kiểm hình dáng và độ đầy đủ còn các mục chưa đạt. Lỗi rõ là dùng outside cho khớp bị che, một cổ tay lẫn người và người nền bỏ sót. Chưa có bằng chứng đủ chắc để kết luận đảo trái/phải toàn thân ở train_02.

Khóa nguyên export người gán và bản YOLO chuyển đổi bằng commit cuối lượt kiểm, theo phạm vi người dùng đã làm xong annotation và yêu cầu thực hiện các phần còn lại. Hash nguồn và từng nhãn nằm trong [label_lock_manifest.json](label_lock_manifest.json). Sau mốc commit không sửa nhãn cho tới protected release. Commit này bảo toàn bài nộp và các phát hiện, không chứng nhận chất lượng đã đạt hết checklist.

## Kiểm bản nộp sau rework và Colab

Ngày 2026-09-16. **Partner vẫn không áp dụng** vì bài làm cá nhân. Phần này là tự kiểm với hỗ trợ phân tích của Codex, không phải kiểm chéo hoặc chấm của một bạn cùng nhóm.

- Sau protected release đã sửa 57 điểm trên 17 skeleton hiện có và thêm hai người nền train_13 qua CVAT; export COCO thật và convert lại được 20 nhãn/29 skeleton. [Chi tiết](rework_changes.json).
- Những ca visibility train_03/09, cổ tay lẫn người train_04, vai train_06, cổ chân train_08/12, tai/khuỷu train_15 và các ca khác có bằng chứng đã được xử lý. JSON sau rework ghép 29/29 với gold, không thiếu/thừa người và không còn finding lỗi vị trí; chẩn đoán cờ khác gold giữ riêng.
- Lượt kiểm cuối có 0 lỗi cấu trúc và 8 cảnh báo. [Log sau rework](pose_validation_after.log) ghi đúng bản hiện tại; cảnh báo bbox cắt chân và người quay đầu không tự chứng minh nhãn sai.
- Kết quả Colab dùng đúng hash 20 nhãn rework. Pose_mAP50–95 0.6853 → 0.6908; box_mAP50–95 0.8119 → 0.8041. [JSON model gốc](../outputs/eval_model.json).
- Đã xem 10 ảnh dự đoán test và ba ảnh train 13/06/03. Train_13 có cặp model–nhãn thấp nhất; train_06 thấp nhất theo trung bình ảnh; train_03 có dự đoán trùng người/ở vật hình em bé và cổ tay người sau đi sang tay người trước. Nhãn không bị sửa theo model.
- [REPORT.md](REPORT.md) đã có bảng model và năm câu phân tích, chỉ rõ cách tính OKS và giới hạn ảnh mờ/CSV. [Reviewer checklist](REVIEWER_CHECKLIST.md) và [bảng artifact](SUBMISSION_CHECKLIST.md) ghi bản nộp cuối.

Các ảnh ước lượng bị che và các lệch nhỏ chưa có bằng chứng đủ chắc vẫn có giới hạn đã nêu; không biến việc hết finding evaluator thành khẳng định mọi pixel đều đúng. Giữ luật lớp: khớp bị che còn trong khung có chấm ước lượng v1, kể cả khi gold COCO không gán hoặc model confidence thấp.
