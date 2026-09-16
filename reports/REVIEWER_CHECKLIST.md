# Reviewer checklist — tự kiểm bài cá nhân

Người gán: LÊ NGỌC NAM. Người kiểm: Codex hỗ trợ đọc ảnh gốc và ảnh phủ. Ngày: 2026-09-16.

Đây là tự kiểm, không có partner độc lập hay chấm điểm với gold. Bản COCO/CVAT không bị chỉnh; YOLO là bản chuyển đổi bằng công cụ có sẵn.

## Kết quả

| # | Mục kiểm | Kết quả | Bằng chứng / giới hạn |
| ---: | --- | --- | --- |
| 1 | Mỗi người có 17 mục, không thiếu người | Đạt cấu trúc; chưa đạt độ đầy đủ | 27 skeleton đều có 51 số COCO. train_13 có người nền chưa có skeleton trong export. |
| 2 | Vai/hông đúng trái/phải, không nối sai thân | Chưa xác nhận lỗi đảo thân | Cảnh báo train_02 dựa trên mắt `v=1`; người quay đầu nên không tự đảo vai/hông. |
| 3 | Không kéo chi sang người khác | Chưa đạt | train_04 người bên trái, `left_wrist`, đặt sang găng tay/vùng tay người bên phải; xem biên bản. |
| 4 | Khớp bị che dùng `v=1` và có tọa độ | Chưa đạt | train_03 người sau `left_wrist`; train_09 `nose/right_eye` đang dùng `v=0` trong khung. |
| 5 | `v=0` chỉ cho khớp ngoài mép ảnh | Chưa đạt | Các ca trên là khớp bị che, không ngoài ảnh. Cảnh báo train_04/10 không đủ để kết luận mọi điểm `v=0` ở các ảnh đó sai. |
| 6 | Không có `v=2` tại điểm vô lý / dấu hiệu Hidden | Cần rà lại | Tai sau mũ ở train_04, gối sát mép dưới ở train_01. Không suy ra lịch sử dùng phím Hidden từ export. |
| 7 | COCO Keypoints: 51 số mỗi người | Đạt | Đủ 27/27; đúng tên/thứ tự COCO17, `num_keypoints` bằng số điểm `v>0`. |
| 8 | YOLO: 56 số/dòng, `kpt_shape: [17, 3]` | Đạt | 20 file, 27 dòng; [data.yaml](../data.yaml) có cấu hình đúng. Converter đặt `(0,0)` cho điểm `v=0`. |
| 9 | Visibility report đã nộp; đối chiếu hai bảng | Đạt báo cáo; đối chiếu N/A | [Bảng](visibility_report.md), [JSON](../outputs/visibility_report.json); bài cá nhân nên không chạy `--compare`. |
| 10 | Ca mơ hồ được ghi vào mini guideline | Đạt | [GUIDELINE_MINI.md](../GUIDELINE_MINI.md) ghi ba ca train_02/03/09 và sáu tình huống kèm ảnh. |
| 11 | check_pose_labels.py chạy 0 lỗi | Đạt cấu trúc, 7 cảnh báo | Đã đọc 20/20 file, 27 skeleton, exit code 0. [Log](pose_validation.log) giữ đầy đủ cảnh báo. |

Ảnh phủ đủ 20 ảnh ở `outputs/vis_train/`; [tổng quan](review_evidence/train_overview.jpg) và các cặp ảnh gốc/ảnh phủ đã lưu cùng báo cáo. Những dòng “chưa đạt” chưa được sửa trong bản khóa.

## Lỗi và kết luận

Danh sách ảnh, người, khớp, hiện trạng và cách xử lý nằm trong [reports/review_partner.md](review_partner.md). Người thứ trong biên bản là thứ tự dòng YOLO/annotation COCO của ảnh, không nhất thiết thứ tự từ trái sang phải.

- Lỗi rõ và lặp lại: dùng `v=0` cho khớp còn trong khung nhưng bị che; ngoài ra có cổ tay lẫn người và điểm gối đặt gần mép ảnh.
- Nguyên nhân chưa thể quy cho thao tác hay phím cụ thể. Quy tắc “bị che khác ngoài khung” và cách ước lượng tai/hông cần được áp dụng nhất quán. Định dạng hợp lệ không đồng nghĩa chất lượng hình dáng đã đạt.

## Khóa nhãn

Khóa nguyên nhãn người gán theo yêu cầu; không sửa sau commit cho tới protected release. [Manifest SHA-256](label_lock_manifest.json) ghi hash export và từng file YOLO. Không chấm với gold hoặc partner.
