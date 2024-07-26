import numpy as np
import supervision as sv
import torch
import argparse

parser = argparse.ArgumentParser(
    prog='yolov5',
    description='This program helps to detect and count the persons in the polygon region',
    epilog='Text at the bottom of help'
)

parser.add_argument('-i', '--input', required=True)  # option that takes a value
parser.add_argument('-o', '--output', required=True)

args = parser.parse_args()
class CountObject:
    def __init__(self, input_video_path, output_video_path) -> None:
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5x6')
        self.colors = [sv.Color(r, g, b) for r, g, b in [(255, 0, 0), (0, 255, 0), (0, 0, 255)]]  # Convert to Color objects

        self.input_video_path = input_video_path
        self.output_video_path = output_video_path

        # Define the polygon
        self.polygons = [np.array([
                [343, 259], [383, 471], [195, 567], [195, 723],
              [143, 735], [7, 399], [7, 1039], [27, 1071],
             [907, 1075], [932, 1067], [953, 1043], [951, 27],[923, 3],
             [847, 7], [691, 63], [699, 87], [643, 115], [623, 91], [343, 259]])]

        self.video_info = sv.VideoInfo.from_video_path(input_video_path)
        self.zones = [
            sv.PolygonZone(
                polygon=polygon
            )
            for polygon
            in self.polygons
        ]

        self.zone_annotators = [
            sv.PolygonZoneAnnotator(
                zone=zone,
                color=self.colors[index],  # Use the Color object
                thickness=6,
                text_scale=4  # Removed text_thickness
            )
            for index, zone
            in enumerate(self.zones)
        ]

        self.box_annotators = [
            sv.BoxAnnotator(
                color=self.colors[index],  # Use the Color object
                thickness=4
            )
            for index
            in range(len(self.polygons))
        ]

    def process_frame(self, frame: np.ndarray, i) -> np.ndarray:
        # detect
        results = self.model(frame, size=1280)
        detections = sv.Detections.from_yolov5(results)
        detections = detections[(detections.class_id == 0) & (detections.confidence > 0.5)]

        for zone, zone_annotator, box_annotator in zip(self.zones, self.zone_annotators, self.box_annotators):
            mask = zone.trigger(detections=detections)
            detections_filtered = detections[mask]
            frame = box_annotator.annotate(scene=frame, detections=detections_filtered)
            frame = zone_annotator.annotate(scene=frame)

        return frame

    def process_video(self):
        sv.process_video(source_path=self.input_video_path, target_path=self.output_video_path,
                         callback=self.process_frame)

if __name__ == "__main__":
    obj = CountObject(args.input, args.output)
    obj.process_video()