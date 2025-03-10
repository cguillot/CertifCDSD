import time
from ultralytics import YOLO
from PIL import Image
import cv2

model = None
classNames = ['Green Light', 'Red Light', 'Speed Limit 10', 'Speed Limit 100', 'Speed Limit 110', 'Speed Limit 120', 'Speed Limit 20', 'Speed Limit 30', 'Speed Limit 40', 'Speed Limit 50', 'Speed Limit 60', 'Speed Limit 70', 'Speed Limit 80', 'Speed Limit 90', 'Stop']

import os

def predict(image):
    global model

    print('predicting model_5...')
    if model is None:
        # Default to docker deployed path (WORKDIR /app/)
        yolo_base_dir = os.getenv('DSFS_FT_31_MODELS_BASE_DIR', '/app/src/model-tester/models').strip('"')
        model = YOLO(f'{yolo_base_dir}/yolov11n/best.pt', task='detect')

    infer_start_time = time.perf_counter()

    results = model(image)

    res_plotted = results[0].plot()

    img_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)

    infer_end_time = time.perf_counter()

    elapsed_time_ms = (infer_end_time - infer_start_time) * 1000

    print(f"model_5 inferred in: {elapsed_time_ms:.3f} ms")

    detected = []
    for bbox in results[0].boxes:
        detected.append({'confidence': float(bbox.conf), 'label_name': classNames[int(bbox.cls)]})

    print('model_5 detected: ', detected)
    description = str(results[0].speed) + " " + str(detected)
    
    stats = {
        'time_to_predict_ms': elapsed_time_ms
    }

    return { "image": img_rgb, "description": description, "detections": detected, "stats": stats }
