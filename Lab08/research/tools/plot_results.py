"""Aggregate labeled GTSRB classification results without scikit-learn."""
from pathlib import Path
import csv
import numpy as np
import cv2
import matplotlib.pyplot as plt
from gtsrb import LABELS, confusion_matrix


def load_predictions(csv_path):
    with open(csv_path,newline='') as f:
        rows=list(csv.DictReader(f))
    if not rows:raise ValueError('Prediction CSV is empty')
    for r in rows:
        r['truth']=int(r['truth']);r['prediction']=int(r['prediction'])
        r['latency_ms']=float(r['latency_ms'])
        r['correct']=int(r['truth']==r['prediction'])
    return rows


def plot_report(csv_path,max_errors=12):
    rows=load_predictions(csv_path)
    accuracy=np.mean([r['correct'] for r in rows])
    times=np.array([r['latency_ms'] for r in rows])
    print('Evaluated real images:',len(rows))
    print('Accuracy: {:.2f}%'.format(100*accuracy))
    print('Median model inference: {:.2f} ms; P95: {:.2f} ms'.format(np.median(times),np.percentile(times,95)))
    print('Invalid class predictions:',sum(not(0<=r['prediction']<43) for r in rows))
    cm=confusion_matrix([r['truth'] for r in rows],[r['prediction'] for r in rows])
    fig,ax=plt.subplots(figsize=(9,8))
    img=ax.imshow(cm,cmap='Blues')
    ax.set_xlabel('Predicted class ID');ax.set_ylabel('True class ID')
    ax.set_title('GTSRB BNN confusion matrix — {} real test images'.format(len(rows)))
    fig.colorbar(img,ax=ax,label='Images')
    plt.tight_layout();plt.show()
    errors=[r for r in rows if r['correct']==0][:max_errors]
    if errors:
        ncols=4;nrows=(len(errors)+3)//4
        fig,axes=plt.subplots(nrows,ncols,figsize=(13,3.4*nrows))
        for ax in np.asarray(axes).reshape(-1): ax.axis('off')
        for r,ax in zip(errors,np.asarray(axes).reshape(-1)):
            bgr=cv2.imread(r['filename']);
            if bgr is None: continue
            ax.imshow(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB));ax.set_title('True {} → predicted {}'.format(r['truth'],r['prediction']),fontsize=9);ax.axis('off')
        plt.suptitle('Real GTSRB images classified incorrectly')
        plt.tight_layout();plt.show()
    else: print('No misclassifications in the selected subset.')
    return rows
