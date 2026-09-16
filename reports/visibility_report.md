# Visibility report

- Thư mục nhãn: `dataset\labels\train`
- 20 ảnh, 29 skeleton, trung bình 15.86 khớp có v > 0 mỗi người
- Tổng: v=2 314 | v=1 146 | v=0 33

| # | Khớp | v=2 | v=1 | v=0 | %v=1 |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0 | nose | 22 | 7 | 0 | 24% |
| 1 | left_eye | 16 | 13 | 0 | 45% |
| 2 | right_eye | 18 | 11 | 0 | 38% |
| 3 | left_ear | 10 | 19 | 0 | 66% |
| 4 | right_ear | 13 | 16 | 0 | 55% |
| 5 | left_shoulder | 27 | 2 | 0 | 7% |
| 6 | right_shoulder | 27 | 2 | 0 | 7% |
| 7 | left_elbow | 23 | 6 | 0 | 21% |
| 8 | right_elbow | 26 | 3 | 0 | 10% |
| 9 | left_wrist | 19 | 10 | 0 | 34% |
| 10 | right_wrist | 19 | 9 | 1 | 31% |
| 11 | left_hip | 17 | 11 | 1 | 38% |
| 12 | right_hip | 21 | 7 | 1 | 24% |
| 13 | left_knee | 15 | 8 | 6 | 28% |
| 14 | right_knee | 13 | 10 | 6 | 34% |
| 15 | left_ankle | 15 | 5 | 9 | 17% |
| 16 | right_ankle | 13 | 7 | 9 | 24% |

## Đọc bảng này thế nào

1. Khớp nào có **%v=1 cao**: khớp hay bị che. Cổ tay và hông thường là hai vị trí cần xem lại guideline trước khi kết luận.
2. Khớp nào có **v=0 cao bất thường**: mọi người đang dùng Outside ở chỗ đáng lẽ là Occluded. Đó là lỗi số 3 của slide 46, và nó xoá thẳng khớp đó khỏi bảng điểm OKS.
3. Khi so hai người: **lệch lớn = bất đồng về guideline**, không phải về bức ảnh. Sửa guideline trước, sửa nhãn sau.
