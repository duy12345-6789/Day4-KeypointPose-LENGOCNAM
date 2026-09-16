# Kiểm artifact — bản nộp cá nhân Ngày 4

Người gán: LÊ NGỌC NAM. Ngày kiểm: 2026-09-16. Partner: không áp dụng.

| Artifact bắt buộc | Trạng thái | Bằng chứng |
| --- | --- | --- |
| `dataset/labels/train/*.txt` | Đủ 20 file, 29 skeleton | [Log kiểm cuối](pose_validation_after.log); mỗi dòng 56 số; hash khớp dữ liệu Colab. |
| `annotations/coco_keypoints/person_keypoints_default.json` | Có export CVAT thật | 20 ảnh, 29 người, mỗi người 51 số keypoint; tọa độ/cờ khớp YOLO sau chuẩn hóa. |
| `outputs/visibility_report.json` | Có, khớp nhãn hiện tại | 314 v2 / 146 v1 / 33 v0. |
| `reports/visibility_report.md` | Đã điền | [Bảng visibility](visibility_report.md), 20 ảnh/29 người; đối chiếu partner N/A. |
| `GUIDELINE_MINI.md` | Đã điền | Luật COCO17, visibility, ca mơ hồ và phân biệt confidence model với visibility annotation. |
| `outputs/eval_vs_gold.json` | Có kết quả sau rework | OKS 0.9539; ghép 29/29; thiếu/thừa 0; giữ JSON trước/sau để kiểm lại. |
| `outputs/eval_model.json` | Có kết quả thật từ Colab | Pose_mAP50–95 0.6853 → 0.6908; JSON nhập nguyên byte từ ZIP kết quả. |
| `reports/REPORT.md` | Đã điền các mục template | Nhãn, gold/rework, partner N/A, bảng model và đủ năm câu phân tích, rule evidence. |
| `reports/review_partner.md` | Đã điền cho bài cá nhân | Giữ biên bản khóa ban đầu; bổ sung kiểm sau rework/Colab; không tạo partner giả. |
| `reports/REVIEWER_CHECKLIST.md` | Đã điền kiểm cuối | 20 nhãn/29 skeleton, định dạng và visibility, đánh giá annotation/model, cảnh báo còn lại. |

[Manifest bản nộp](../outputs/submission_manifest.json) lưu hash và kết quả kiểm. [Manifest nhập Colab](model_evidence/import_manifest.json) lưu SHA-256 của ZIP và từng kết quả gốc; ảnh phủ nhãn bổ sung dùng để đọc lỗi. Nhãn/export không thay đổi khi nhập kết quả model.

## Lượt kiểm cuối

```bash
python3 tools/check_pose_labels.py --images dataset/images/train --labels dataset/labels/train
```

Kết quả: exit code 0, 0 lỗi cấu trúc, 8 cảnh báo đã giải thích trong [REPORT.md](REPORT.md). Log cũ 27 người/7 cảnh báo thuộc mốc khóa; [pose_validation_after.log](pose_validation_after.log) ghi bản nộp 29 người/8 cảnh báo.

Commit bản nộp: `Day 4: pose annotation and evaluation`, push lên nhánh `main`. Các file kết quả/báo cáo và ảnh dự đoán minh họa được commit; ZIP trao đổi, protected gold, model weights và cache không nằm trong commit.

## Nộp VLearn

URL fork cá nhân: **https://github.com/duy12345-6789/Day4-KeypointPose-LENGOCNAM**.

Chỉ dán URL này vào biểu mẫu nộp bài. Không tải ZIP, ảnh raw, test labels, gold labels hoặc model weights lên VLearn. Kiểm lại nhánh main và khả năng đọc URL không dùng đăng nhập sau khi push. Việc gửi biểu mẫu VLearn do người gán thực hiện.
