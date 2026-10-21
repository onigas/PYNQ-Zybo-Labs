"""Local utility test; synthetic files are used ONLY to test loader correctness."""
import tempfile
from pathlib import Path
import csv
import numpy as np
import cv2
from gtsrb import find_test_records,stratified_sample,load_rgb_32,confusion_matrix

with tempfile.TemporaryDirectory() as d:
    base=Path(d)
    (base/'GTSRB/Final_Test/Images').mkdir(parents=True)
    with (base/'GT-final_test.csv').open('w',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(['Filename','Width','Height','ROI.x1','ROI.y1','ROI.x2','ROI.y2','ClassId'])
        for i in range(90):
            name=f'{i:05d}.ppm'; y=i%43
            cv2.imwrite(str(base/'GTSRB/Final_Test/Images'/name),np.zeros((10,10,3),np.uint8)+y)
            w.writerow([name,10,10,0,0,9,9,y])
    records=find_test_records(base)
    assert len(records)==90
    subset=stratified_sample(records,65)
    assert len(subset)==65
    assert {v for _,v in subset}==set(range(43))
    assert load_rgb_32(records[0][0]).shape==(32,32,3)
    cm=confusion_matrix([0,1,2],[0,43,2]);assert cm.sum()==2
    print('PASS: GTSRB CSV loader, stratified selection, RGB preprocessing, class labels')
