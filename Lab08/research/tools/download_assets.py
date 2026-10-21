#!/usr/bin/env python3
"""Fetch OFFICIAL GTSRB TEST set and Xilinx FINN pretrained QONNX model.

Run on a computer with internet; files need not be downloaded on the Zybo.
Use --dataset-only or --model-only as needed. Safe extraction checks zip-slip.
"""
from pathlib import Path
import urllib.request
import zipfile
import argparse

DATA_URL = 'https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/'
MODEL_URL = 'https://github.com/Xilinx/finn-examples/releases/download/v0.0.7a/onnx-models-gtsrb.zip'


def download(url, target):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_file() and target.stat().st_size > 1000:
        print('Already downloaded:', target)
        return
    print('Downloading', url)
    target_part = target.with_suffix(target.suffix+'.part')
    urllib.request.urlretrieve(url, str(target_part))
    target_part.replace(target)
    print('Saved', target, target.stat().st_size, 'bytes')


def safe_extract(zip_path, destination, just_onnx=False):
    base = Path(destination).resolve()
    base.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        for item in z.infolist():
            if item.is_dir(): continue
            if just_onnx and not item.filename.lower().endswith('.onnx'): continue
            output = (base / (Path(item.filename).name if just_onnx else item.filename)).resolve()
            if not output.is_relative_to(base): raise ValueError('ZIP path traversal attempted')
            output.parent.mkdir(parents=True,exist_ok=True)
            with z.open(item) as src, output.open('wb') as dst:
                import shutil
                shutil.copyfileobj(src,dst)
            print('Extracted:', output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-only', action='store_true')
    parser.add_argument('--model-only', action='store_true')
    parser.add_argument('--root', default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    root = Path(args.root)
    if not args.model_only:
        for filename in ['GTSRB_Final_Test_Images.zip', 'GTSRB_Final_Test_GT.zip']:
            dest = root/'data'/'archives'/filename
            download(DATA_URL+filename,dest)
            safe_extract(dest,root/'data'/'gtsrb')
    if not args.dataset_only:
        dest=root/'models'/'onnx-models-gtsrb.zip'
        download(MODEL_URL,dest)
        safe_extract(dest,root/'models',just_onnx=True)
    print('Ready. Open notebooks/ in order.')

if __name__=='__main__': main()
