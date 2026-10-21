"""Candidate sign detection + FINN classification. Image segmentation runs on ARM."""
import time
import cv2
import numpy as np


def extract_candidates(frame_bgr, min_area=180, max_candidates=3):
    """Return (x,y,w,h) for colored regions that could contain signs.

    Intentionally only a heuristic region proposal, not a trained detector.
    Candidates have no semantic label until an actual trained BNN is run.
    """
    hsv=cv2.cvtColor(frame_bgr,cv2.COLOR_BGR2HSV)
    red1=cv2.inRange(hsv,(0,90,55),(12,255,255))
    red2=cv2.inRange(hsv,(165,90,55),(179,255,255))
    blue=cv2.inRange(hsv,(92,90,55),(135,255,255))
    combined=cv2.bitwise_or(cv2.bitwise_or(red1,red2),blue)
    kernel=np.ones((5,5),dtype=np.uint8)
    combined=cv2.morphologyEx(combined,cv2.MORPH_CLOSE,kernel)
    contours,_=cv2.findContours(combined,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    choices=[]
    for contour in contours:
        area=cv2.contourArea(contour)
        if area < min_area:continue
        x,y,w,h=cv2.boundingRect(contour)
        ratio=w/max(1,h)
        if .55<=ratio<=1.65:
            pad=int(max(w,h)*.12)
            x1=max(0,x-pad);y1=max(0,y-pad)
            x2=min(frame_bgr.shape[1],x+w+pad)
            y2=min(frame_bgr.shape[0],y+h+pad)
            choices.append((area,(x1,y1,x2-x1,y2-y1)))
    choices.sort(key=lambda p:p[0],reverse=True)
    return [r for _,r in choices[:max_candidates]],combined


def decode_scores(output):
    """43-class output or 44-element padded logits; invalid class is -1."""
    arr=np.asarray(output).reshape(-1)
    if arr.size==1:
        cid=int(arr[0])
    elif arr.size in (43,44):
        cid=int(np.argmax(arr))
    else:
        raise ValueError('Unexpected FINN GTSRB output shape {}'.format(np.asarray(output).shape))
    return cid if 0<=cid<43 else -1


def classify_roi(accel, frame_bgr, box):
    x,y,w,h=box
    roi=frame_bgr[y:y+h,x:x+w]
    if not roi.size:raise ValueError('Empty cropped ROI')
    roi32=cv2.resize(roi,(32,32),interpolation=cv2.INTER_LINEAR)
    rgb32=cv2.cvtColor(roi32,cv2.COLOR_BGR2RGB)
    inp=np.expand_dims(np.ascontiguousarray(rgb32,dtype=np.uint8),0)
    started=time.perf_counter_ns()
    result=accel.execute(inp)
    latency_ms=(time.perf_counter_ns()-started)/1e6
    return decode_scores(result),latency_ms
