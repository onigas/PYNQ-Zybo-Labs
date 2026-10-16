# Original Lab08.4 20-image GTSRB FPGA benchmark, retained without
# changing the inference algorithm. Renumbered as Lab08.3 for publication.
# Requirements: infer_fpga() defined by the preceding notebook cell and
# gtsrb_batch20_inputs.npz in this same notebooks/ directory.
from pathlib import Path
import time
import numpy as np

batch_file = Path('gtsrb_batch20_inputs.npz')
if not batch_file.is_file():
    raise FileNotFoundError('Upload gtsrb_batch20_inputs.npz into Lab08/notebooks first.')
with np.load(batch_file, allow_pickle=False) as data:
    for field in ('rgb32', 'true_classes', 'csv_indices', 'filenames'):
        if field not in data:
            raise ValueError('Missing field {} in {}'.format(field, batch_file))
    test_images = np.array(data['rgb32'], copy=True)
    test_labels = np.array(data['true_classes'], copy=True)
    test_indices = np.array(data['csv_indices'], copy=True)
    test_filenames = np.array(data['filenames'], copy=True)

if test_images.dtype != np.uint8 or test_images.shape != (20, 32, 32, 3):
    raise ValueError('Expected uint8 images with shape (20,32,32,3).')
if test_labels.shape != (20,) or not np.all((test_labels >= 0) & (test_labels < 43)):
    raise ValueError('Expected 20 valid GTSRB labels (0..42).')
if len(set(int(x) for x in test_labels)) != 20:
    raise ValueError('20 samples must come from distinct GTSRB classes.')

all_scores = np.empty((20, 44), dtype=np.int16)
all_times_ms = np.empty((20,), dtype=np.float64)
all_predictions = np.empty((20,), dtype=np.int16)

print('Starting 20 FPGA inferences. No camera is used.', flush=True)
for i, image in enumerate(test_images):
    try:
        output = infer_fpga(image, timeout_s=8.0)
    except Exception as exc:
        print('STOP at sample {} (class {}, CSV index {}): {}'.format(
            i, int(test_labels[i]), int(test_indices[i]), exc), flush=True)
        raise
    all_scores[i, :] = output['scores']
    all_times_ms[i] = output['elapsed_ms']
    all_predictions[i] = output['raw_argmax']
    pred = int(all_predictions[i])
    print('{}/20 | CSV {:5d} | actual {:2d} | FPGA {:2d} | {} | {:.1f} ms'.format(
        i + 1, int(test_indices[i]), int(test_labels[i]), pred,
        'OK' if pred == int(test_labels[i]) else 'ERROR',
        float(all_times_ms[i])), flush=True)

batch_output = Path('gtsrb_batch20_fpga.npz')
np.savez_compressed(
    batch_output,
    rgb32=test_images,
    true_classes=test_labels,
    csv_indices=test_indices,
    filenames=test_filenames,
    fpga_scores=all_scores,
    fpga_elapsed_ms=all_times_ms,
)
print('FPGA accuracy: {}/20'.format(int(np.sum(all_predictions == test_labels))), flush=True)
print('Mean DMA + inference: {:.2f} ms'.format(float(np.mean(all_times_ms))), flush=True)
print('SAVED:', batch_output.resolve(), flush=True)
