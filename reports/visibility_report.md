# Visibility report

- Thư mục nhãn: `dataset\labels\train`
- 20 ảnh, 27 skeleton, trung bình 15.81 khớp có v > 0 mỗi người
- Tổng: v=2 334 | v=1 93 | v=0 32

| # | Khớp | v=2 | v=1 | v=0 | %v=1 |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0 | nose | 21 | 5 | 1 | 19% |
| 1 | left_eye | 19 | 8 | 0 | 30% |
| 2 | right_eye | 20 | 6 | 1 | 22% |
| 3 | left_ear | 16 | 11 | 0 | 41% |
| 4 | right_ear | 18 | 9 | 0 | 33% |
| 5 | left_shoulder | 26 | 1 | 0 | 4% |
| 6 | right_shoulder | 27 | 0 | 0 | 0% |
| 7 | left_elbow | 24 | 3 | 0 | 11% |
| 8 | right_elbow | 24 | 2 | 1 | 7% |
| 9 | left_wrist | 19 | 7 | 1 | 26% |
| 10 | right_wrist | 17 | 8 | 2 | 30% |
| 11 | left_hip | 19 | 7 | 1 | 26% |
| 12 | right_hip | 23 | 3 | 1 | 11% |
| 13 | left_knee | 18 | 5 | 4 | 19% |
| 14 | right_knee | 16 | 7 | 4 | 26% |
| 15 | left_ankle | 15 | 4 | 8 | 15% |
| 16 | right_ankle | 12 | 7 | 8 | 26% |

## Đọc bảng này thế nào

1. Khớp nào có **%v=1 cao**: khớp hay bị che. Cổ tay và hông thường là hai vị trí cần xem lại guideline trước khi kết luận.
2. Khớp nào có **v=0 cao bất thường**: mọi người đang dùng Outside ở chỗ đáng lẽ là Occluded. Đó là lỗi số 3 của slide 46, và nó xoá thẳng khớp đó khỏi bảng điểm OKS.
3. Khi so hai người: **lệch lớn = bất đồng về guideline**, không phải về bức ảnh. Sửa guideline trước, sửa nhãn sau.
