import argparse
import numpy as np
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
import supervision as sv

class DetectronProcessor:
    def __init__(self, input_video_path, output_video_path):
        self.input_video_path = input_video_path
        self.output_video_path = output_video_path

        # Initialize Detectron2 configuration and predictor
        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        self.predictor = DefaultPredictor(self.cfg)

        # Define the polygon zone
        self.polygon = np.array([
            [342, 251], [374, 399], [194, 523], [186, 735], [154, 739], [70, 507], [6, 515], [6, 1043], [20, 1067],
            [911, 1071], [934, 1059], [954, 1027], [954, 23], [922, 3], [802, 7], [344, 246]
        ])
        self.zone = sv.PolygonZone(polygon=self.polygon)

        # Initialize annotators
        self.box_annotator = sv.BoxAnnotator(thickness=4)
        self.zone_annotator = sv.PolygonZoneAnnotator(zone=self.zone, color=sv.Color.WHITE, thickness=6, text_thickness=6, text_scale=4)

    def process_frame(self, frame: np.ndarray, i: int) -> np.ndarray:
        # Detect
        outputs = self.predictor(frame)
        detections = sv.Detections(
            xyxy=outputs["instances"].pred_boxes.tensor.cpu().numpy(),
            confidence=outputs["instances"].scores.cpu().numpy(),
            class_id=outputs["instances"].pred_classes.cpu().numpy().astype(int)
        )
        detections = detections[detections.class_id == 0]
        self.zone.trigger(detections=detections)

        # Annotate
        frame = self.box_annotator.annotate(scene=frame, detections=detections)
        frame = self.zone_annotator.annotate(scene=frame)

        return frame

    def process_video(self):
        sv.process_video(source_path=self.input_video_path, target_path=self.output_video_path, callback=self.process_frame)

def main():
    parser = argparse.ArgumentParser(description="Detectron2 Video Processing")
    parser.add_argument('--input', type=str, required=True, help='Path to the input video file')
    parser.add_argument('--output', type=str, required=True, help='Path to the output video file')
    args = parser.parse_args()

    processor = DetectronProcessor(input_video_path=args.input, output_video_path=args.output)
    processor.process_video()

if __name__ == "__main__":
    main()