#!/usr/bin/env python3
"""Evaluate genuine FINN QONNX GTSRB model (NO random/artificial predictions).

Requires qonnx on an x86 FINN host environment, not on Zybo armv7l.
"""
from pathlib import Path
import argparse
import csv
import time
import numpy as np

from gtsrb import find_test_records, stratified_sample, load_rgb_32, confusion_matrix, LABELS


def get_model_executor(model_file):
    try:
        from qonnx.core.modelwrapper import ModelWrapper
        from qonnx.core.onnx_exec import execute_onnx
    except ImportError as exc:
        raise RuntimeError('QONNX is not installed. Run in the FINN Docker x86 environment, or install qonnx on a supported host. This is NOT a Zybo notebook.') from exc
    model = ModelWrapper(str(model_file))
    name = model.graph.input[0].name
    shape = model.get_tensor_shape(name)
    if shape in ([1,3,32,32], (1,3,32,32)):
        layout='NCHW'
    elif shape in ([1,32,32,3], (1,32,32,3)):
        layout='NHWC'
    else:
        raise ValueError('Unexpected model input shape {}. Inspect preprocessing and model version.'.format(shape))
    output_name = model.graph.output[0].name
    print('Model input:',name,shape,'layout:',layout)
    print('Model output:',output_name,model.get_tensor_shape(output_name))

    def predict(image_rgb_uint8):
        # FINN GTSRB pretrained QONNX model expects float-normalized [0..1] RGB.
        image = image_rgb_uint8.astype(np.float32) / 255.0
        if layout=='NCHW': image = np.transpose(image, (2,0,1))
        image = np.expand_dims(image,0).copy()
        data = execute_onnx(model,{name: image})[output_name]
        values = np.asarray(data).reshape(-1)
        if values.size == 1:
            return int(values[0])
        if values.size in (43,44):
            # Some FINN models pad the 43 classes to 44 output values.
            # Padded class #43 is an invalid classification: count it as an error.
            return int(np.argmax(values))
        raise ValueError('Unexpected model output: shape {} ({} values)'.format(data.shape,values.size))
    return predict


def evaluate(dataset, model_file, limit, output, progress=10):
    records = find_test_records(dataset)
    sample = stratified_sample(records,limit)
    print('GTSRB test set:',len(records),'labeled images; evaluating:',len(sample))
    classifier=get_model_executor(model_file)
    output=Path(output);output.mkdir(parents=True, exist_ok=True)
    rows=[]
    started=time.perf_counter()
    for i,(path,y) in enumerate(sample):
        image = load_rgb_32(path)
        t0=time.perf_counter_ns()
        predicted = classifier(image)
        latency=(time.perf_counter_ns()-t0)/1e6
        rows.append(dict(filename=str(path), truth=y, prediction=predicted,
                         correct=int(y==predicted), latency_ms=round(latency,3)))
        if (i+1)%progress==0 or i+1==len(sample):
            print('Processed {:5d}/{:5d} | accuracy {:.1f}% | avg {:.0f} ms/image'.format(
                i+1,len(sample),100*sum(z['correct'] for z in rows)/len(rows),
                sum(z['latency_ms'] for z in rows)/len(rows)),flush=True)
    with (output/'predictions.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
    cm=confusion_matrix([r['truth'] for r in rows],[r['prediction'] for r in rows])
    np.save(output/'confusion.npy', cm)
    accuracy=sum(r['correct'] for r in rows)/len(rows)
    times=np.array([r['latency_ms'] for r in rows])
    print('Samples:',len(rows),'accuracy: {:.2f}%'.format(100*accuracy))
    print('Median inference: {:.1f} ms | P95: {:.1f} ms'.format(np.median(times),np.percentile(times,95)))
    print('Elapsed total: {:.1f} s'.format(time.perf_counter()-started))
    print('Invalid class IDs:',sum(r['prediction']<0 or r['prediction']>=43 for r in rows))
    print('Saved',output/'predictions.csv')


def main():
    p=argparse.ArgumentParser()
    root=Path(__file__).resolve().parents[1]
    p.add_argument('--data',default=str(root/'data'/'gtsrb'))
    p.add_argument('--model',default=str(root/'models'/'cnv_1w1a_gtsrb.onnx'))
    p.add_argument('--limit',type=int,default=215,help='215 (5/class), 430, 1000 or 0=all test images')
    p.add_argument('--out',default=str(root/'results'/'qonnx_cpu'))
    args=p.parse_args()
    if not Path(args.model).is_file():raise FileNotFoundError('Pretrained model is missing: '+args.model+'; run download_assets.py')
    evaluate(args.data,args.model,args.limit,args.out)
if __name__=='__main__':main()
