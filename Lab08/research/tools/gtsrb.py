"""GTSRB labeled test-set utilities: no download, no fabricated predictions."""
from pathlib import Path
import csv
import numpy as np
import cv2

LABELS = [
    'Speed limit 20', 'Speed limit 30', 'Speed limit 50', 'Speed limit 60',
    'Speed limit 70', 'Speed limit 80', 'End speed limit 80', 'Speed limit 100',
    'Speed limit 120', 'No passing', 'No passing (trucks)', 'Priority at next intersection',
    'Priority road', 'Yield', 'Stop', 'No vehicles', 'Trucks prohibited', 'No entry',
    'General caution', 'Dangerous curve left', 'Dangerous curve right', 'Double curve',
    'Bumpy road', 'Slippery road', 'Road narrows on right', 'Road work', 'Traffic signals',
    'Pedestrians', 'Children crossing', 'Bicycles crossing', 'Beware of ice/snow',
    'Wild animals crossing', 'End speed and passing limits', 'Turn right ahead',
    'Turn left ahead', 'Ahead only', 'Ahead or right', 'Ahead or left',
    'Keep right', 'Keep left', 'Roundabout mandatory', 'End no passing',
    'End no passing (trucks)'
]


def find_test_records(root):
    """Find the *official labeled* GTSRB test images and CSV in a tree.

    Supports torchvision layout and directly extracted GTSRB archives.
    Returns a list of (path, class_id), deterministic in CSV order.
    """
    root = Path(root)
    candidates = sorted(root.rglob('GT-final_test.csv'))
    if not candidates:
        raise FileNotFoundError('GT-final_test.csv not found under {}. Download BOTH GTSRB test images and ground truth.'.format(root))
    csv_path = candidates[0]
    # The official CSV is ; separated; optional BOM tolerated.
    with csv_path.open('r', encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f, delimiter=';', skipinitialspace=True))
    if not rows or 'Filename' not in rows[0] or 'ClassId' not in rows[0]:
        raise ValueError('Unexpected GTSRB CSV columns: {}'.format(list(rows[0]) if rows else '<empty>'))
    image_folders = [csv_path.parent, csv_path.parent/'GTSRB'/'Final_Test'/'Images',
                     root/'GTSRB'/'Final_Test'/'Images', root/'gtsrb'/'GTSRB'/'Final_Test'/'Images']
    # In torchvision extracted layout the csv is at root/gtsrb/ and images at root/gtsrb/GTSRB/Final_Test/Images.
    seen = set()
    image_folders = [p for p in image_folders if not (str(p) in seen or seen.add(str(p)))]
    for image_dir in image_folders:
        records = [(image_dir / row['Filename'], int(row['ClassId'])) for row in rows]
        if all(p.is_file() for p,_ in records[:min(12,len(records))]):
            if any(not p.is_file() for p,_ in records):
                raise FileNotFoundError('The test images are incomplete in {} ({} annotation rows).'.format(image_dir, len(rows)))
            if any(not 0 <= y < 43 for _,y in records):
                raise ValueError('GTSRB ClassId outside 0..42')
            return records
    raise FileNotFoundError('Ground-truth CSV found at {}, but its referenced images were not found. Keep the test images in GTSRB/Final_Test/Images/'.format(csv_path))


def stratified_sample(records, limit, seed=2026):
    """Representative subset with samples from every class, if limit>=43.

    Full set is selected when limit=None or limit<=0.
    """
    if limit is None or limit <= 0 or limit >= len(records):
        return list(records)
    rng = np.random.default_rng(seed)
    if limit < 43:
        return [records[int(i)] for i in sorted(rng.choice(len(records), size=limit, replace=False))]
    selected = []
    all_by_class = {k: [] for k in range(43)}
    for i, (_, y) in enumerate(records): all_by_class[y].append(i)
    # Assign equal quotas, distribute extra randomly, never exceed available samples.
    per_class = limit // 43
    chosen_ids = set()
    for label in range(43):
        cls = all_by_class[label]
        take = min(per_class, len(cls))
        for i in rng.choice(cls, size=take, replace=False): chosen_ids.add(int(i))
    available = list(set(range(len(records))) - chosen_ids)
    remaining = min(limit-len(chosen_ids), len(available))
    for i in rng.choice(available, size=remaining, replace=False): chosen_ids.add(int(i))
    return [records[i] for i in sorted(chosen_ids)]


def load_rgb_32(path):
    """Return uint8 32x32 RGB image for the pretrained FINN GTSRB classifier."""
    frame = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if frame is None: raise ValueError('Unable to read image: {}'.format(path))
    frame = cv2.resize(frame, (32,32), interpolation=cv2.INTER_LINEAR)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def confusion_matrix(y_true, y_pred, classes=43):
    """Count correct/incorrect labels; invalid network output contributes to error but no CM column."""
    cm = np.zeros((classes, classes), dtype=np.int64)
    for truth,pred in zip(y_true, y_pred):
        if 0 <= int(pred) < classes: cm[int(truth), int(pred)] += 1
    return cm
