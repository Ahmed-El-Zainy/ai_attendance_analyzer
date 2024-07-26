import numpy as np
import torch
import cvzone
from super_gradients.training import models
import cv2
import math
from sort import *

class PeopleCounter:
    def __init__(self, input_video_path, output_video_path, classnames_path):
        self.input_video_path = input_video_path
        self.output_video_path = output_video_path
        self.classnames_path = classnames_path

        self.cap = cv2.VideoCapture(self.input_video_path)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.out = cv2.VideoWriter(self.output_video_path, self.fourcc, self.fps, (self.width, self.height))

        if not self.out.isOpened():
            print("Error: Could not open output video file for writing.")
            exit()

        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        print(self.device)

        self.model = models.get('yolo_nas_s', pretrained_weights='coco').to(self.device)

        self.zone = np.array([
            [343, 259], [383, 471], [195, 567], [195, 723],
            [143, 735], [7, 399], [7, 1039], [27, 1071],
            [907, 1075], [932, 1067], [953, 1043], [951, 27], [923, 3],
            [847, 7], [691, 63], [699, 87], [643, 115], [623, 91], [343, 259]
        ])

        self.tracker = Sort()
        with open(self.classnames_path, 'r') as f:
            self.classnames = f.read().splitlines()

    def process_frame(self, video):
        detections = np.empty((0, 5))
        people_count = 0
        total_people_in_frame = []

        video = cv2.resize(video, (1280, 1152))

        result = self.model.predict(video, conf=0.50)
        bboxs = result.prediction.bboxes_xyxy
        confidence = result.prediction.confidence
        labels = result.prediction.labels

        for (bbox, conf, label) in zip(bboxs, confidence, labels):
            x1, y1, x2, y2 = np.array(bbox)
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            conf = math.ceil(conf * 100)
            label = int(label)
            classdetect = self.classnames[label]
            w, h = x2 - x1, y2 - y1

            if classdetect == 'person':
                new_detections = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, new_detections))

        track_result = self.tracker.update(detections)
        for results in track_result:
            x1, y1, x2, y2, id = results
            x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)
            w, h = x2 - x1, y2 - y1
            cx, cy = x1 + w // 2, y1 + h // 2

            total_people_in_frame.append(id)

            cv2.circle(video, (cx, cy), 6, (0, 255, 255), -1)
            cv2.rectangle(video, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cvzone.putTextRect(video, f'{id}', [x1 + 8, y1 - 12], thickness=2, scale=1.5)

            cv2.polylines(video, [self.zone], True, (0, 0, 255), 4)
            counts = cv2.pointPolygonTest(self.zone, pt=(cx, cy), measureDist=False)
            if counts == 1:  # Inside the defined region
                people_count += 1

        # Display the count of people in the region on the frame
        cvzone.putTextRect(video, f'People in Region: {people_count}', (0, 32), scale=2)
        cvzone.putTextRect(video, f'Total People Detected: {len(total_people_in_frame)}', (600, 32), scale=2)

        return video

    def process_video(self):
        frame_count = 0
        while self.cap.isOpened():
            rt, video = self.cap.read()
            if not rt:
                print("End of video file reached or cannot read the frame.")
                break

            video = self.process_frame(video)

            # Write the frame to the output file
            self.out.write(video)
            frame_count += 1

            # Display the frame
            cv2.imshow('frame', video)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print(f"Processed {frame_count} frames.")
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    input_video_path = r'AI_Intern_Video_Tech_Task.mp4'
    output_video_path = r'output_yolo_nas.mp4'
    classnames_path = 'classes.txt'
    people_counter = PeopleCounter(input_video_path, output_video_path, classnames_path)
    people_counter.process_video()