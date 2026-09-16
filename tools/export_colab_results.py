"""Run after notebook sections 0–6 to download the evidence for REPORT.md."""
from __future__ import annotations

import hashlib
import json
import math
import zipfile
from pathlib import Path


def export_results(context: dict) -> Path:
    required = ('LAB_ROOT', 'OUTPUTS', 'RUNS', 'TRAIN_IMAGES', 'TRAIN_LABELS',
                'MODEL_NAME', 'DEVICE', 'best_model', 'rows_out', 'image_size')
    missing = [name for name in required if name not in context]
    if missing:
        raise RuntimeError('Chạy xong các mục 0–6 trước: thiếu ' + ', '.join(missing))
    root = Path(context['LAB_ROOT']).resolve()
    outputs = Path(context['OUTPUTS']).resolve()
    runs = Path(context['RUNS']).resolve()
    train_images = Path(context['TRAIN_IMAGES']).resolve()
    train_labels = Path(context['TRAIN_LABELS']).resolve()
    assert all(path.is_relative_to(root) for path in (outputs, runs, train_images, train_labels))
    evaluation = outputs / 'eval_model.json'
    if not evaluation.is_file():
        raise RuntimeError('Chưa có outputs/eval_model.json; chạy mục 4 trước.')
    metrics = json.loads(evaluation.read_text(encoding='utf-8'))
    baseline_key = 'baseline_' + context['MODEL_NAME'].replace('.pt', '')
    metric_names = ('pose_mAP50', 'pose_mAP50_95', 'pose_precision', 'pose_recall',
                    'box_mAP50', 'box_mAP50_95')
    for section in (baseline_key, 'finetuned', 'delta'):
        for name in metric_names:
            value = metrics[section][name]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f'Chỉ số không hợp lệ: {section}.{name}')
    test_predictions = sorted((runs / 'predictions/test').glob('*.jpg'))
    if len(test_predictions) != 10:
        raise RuntimeError('Cần đủ 10 ảnh dự đoán test; chạy mục 5 trước.')
    label_files = sorted(train_labels.glob('*.txt'))
    if len(label_files) != 20 or len(list(train_images.glob('*.jpg'))) != 20:
        raise RuntimeError('Bài phải có đủ 20 ảnh và nhãn train.')
    rows = list(context['rows_out'])
    if not rows:
        raise RuntimeError('Chưa có bảng OKS; chạy mục 6 trước.')
    scored = sorted((stem, score) for stem, score in rows if isinstance(score, (int, float)))
    scored.sort(key=lambda row: row[1])
    low_score_images = list(dict.fromkeys(stem for stem, _ in scored))
    count_mismatches = list(dict.fromkeys(stem.split(' (')[0] for stem, score in rows if isinstance(score, str)))
    selected = low_score_images[:2 if count_mismatches else 3]
    for stem in count_mismatches + low_score_images:
        if len(selected) == 3:
            break
        if stem not in selected:
            selected.append(stem)
    evidence = []
    predictions = []
    for stem in selected:
        image = train_images / f'{stem}.jpg'
        if not image.is_file():
            raise RuntimeError(f'Không tìm thấy ảnh train {image.name}.')
        result = context['best_model'].predict(
            source=str(image), conf=0.25, device=context['DEVICE'], save=True,
            project=str(runs / 'predictions'), name='report_train', exist_ok=True,
            verbose=False)[0]
        width, height = context['image_size'](image)
        predictions.append({'image': image.name, 'width': width, 'height': height,
                            'boxes_xywhn': result.boxes.xywhn.tolist(),
                            'keypoints_xy_conf': result.keypoints.data.tolist()})
        rendered = runs / 'predictions/report_train' / image.name
        if not rendered.is_file():
            raise RuntimeError(f'Không tìm thấy ảnh dự đoán {rendered}.')
        evidence.append(rendered)
    review = outputs / 'train_model_review.json'
    payload = {
        'model': context['MODEL_NAME'], 'prediction_confidence': 0.25,
        'oks_rows_from_notebook': [{'image': stem, 'value': score} for stem, score in rows],
        'lowest_scored_pair': {'image': scored[0][0], 'oks': scored[0][1]} if scored else None,
        'review_predictions': predictions,
        'train_label_sha256': {path.name: hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
                               for path in label_files},
        'eval_model_sha256': hashlib.sha256(evaluation.read_bytes()).hexdigest(),
    }
    review.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    members = [evaluation, review, *test_predictions, *evidence]
    results_csv = runs / 'pose_finetune/results.csv'
    if results_csv.is_file():
        members.append(results_csv)
    archive = root.parent / 'Day4-Colab-results.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in members:
            relative = path.resolve().relative_to(root)
            if 'gold' in relative.parts or relative.suffix.lower() not in ('.json', '.jpg', '.csv'):
                raise ValueError(f'File không thuộc gói kết quả: {relative}')
            bundle.write(path, relative.as_posix())
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.testzip() is None
    print(f'Đã đóng gói {len(members)} file kết quả: {archive.name}')
    print('Gửi gói này để điền REPORT.md; nộp URL fork trên VLearn.')
    return archive


if __name__ == '__main__':
    archive_path = export_results(globals())
    from google.colab import files
    files.download(str(archive_path))
