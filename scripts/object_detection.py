import os
import pandas as pd
import torch
from pathlib import Path
from yolov5 import detect
from PIL import Image
import logging

# Set up logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/object_detection.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class YOLOObjectDetection:
    def __init__(self, image_dir="data/raw/photos", output_dir="data/preprocessed/detections", model_name="yolov5s"):
        self.image_dir = Path(image_dir)
        self.output_dir = Path(output_dir)
        self.model = torch.hub.load("ultralytics/yolov5", "custom", path=model_name, force_reload=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def run_detection(self):
        results = []
        for image_path in self.image_dir.glob("*.jpg"):
            try:
                logging.info(f"Processing {image_path}")
                detections = self.model(str(image_path))
                detections.save(save_dir=self.output_dir)

                for *box, conf, cls in detections.xyxy[0].tolist():
                    results.append({
                        "image": image_path.name,
                        "xmin": box[0],
                        "ymin": box[1],
                        "xmax": box[2],
                        "ymax": box[3],
                        "confidence": conf,
                        "class": self.model.names[int(cls)]
                    })

            except Exception as e:
                logging.error(f"Error processing {image_path}: {e}")
        return results

    def save_results(self, results, output_csv="data/preprocessed/detection_results.csv"):
        df = pd.DataFrame(results)
        df.to_csv(output_csv, index=False)
        logging.info(f"Detection results saved to {output_csv}")


if __name__ == "__main__":
    detector = YOLOObjectDetection()
    results = detector.run_detection()
    detector.save_results(results)
