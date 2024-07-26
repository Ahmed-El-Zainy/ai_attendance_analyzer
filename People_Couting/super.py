import numpy as np
import supervision as sv
from ultralytics import YOLO

MALL_VIDEO_PATH = "AI_Intern_Video_Tech_Task.mp4"

# initialize polygon zone
polygon = np.array([[362, 274],
                    [498, 1074],
                    [586, 1070],
                    [586, 1070],
                    [950, 694],
                    [950, 94],
                    [874, 26],
                    [362, 266],
                    [362, 274]])

video_info = sv.VideoInfo.from_video_path(MALL_VIDEO_PATH)
zone = sv.PolygonZone(polygon=polygon)

box_annotator = sv.BoxAnnotator(color=sv.Color.WHITE, thickness=4, text_scale=2)  # Adjusted the parameters
zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.WHITE, thickness=6, text_thickness=6, text_scale=4)

model = YOLO("yolov8s.pt")

def process_frame(frame: np.ndarray, _) -> np.ndarray:
    results = model(frame, imgsz=1280)[0]
    detections = sv.Detections.from_ultralytics(results)
    detections = detections[detections.class_id == 0]
    zone.trigger(detections=detections)

    labels = [f"{model.names[class_id]} {confidence:0.2f}" for _, _, confidence, class_id, _, _ in detections]
    frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
    frame = zone_annotator.annotate(scene=frame)

    return frame

sv.process_video(source_path=MALL_VIDEO_PATH, target_path="mall-result.mp4", callback=process_frame)
print(model.model.names)