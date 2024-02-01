import cv2
import torch
import random
from modules.autobackend import AutoBackend
import modules.utils as utils


class InferDet:
    def __init__(self):
        self.model = AutoBackend('yolov8n.engine', device=torch.device('cuda:0'), fp16=True)
        self.model.warmup()
        self.label_map = self.model.names
        self.COLORS = [[random.randint(0, 255) for _ in range(3)] for _ in self.label_map]

    def tensorrt_detection(self, model, image):
        # Preprocess
        im = utils.preprocess(image)

        # Inference
        preds = model(im)

        # Post Process
        results = utils.postprocess(preds, im, image, model.names)
        d = results[0].boxes

        # Get information from result
        tensor_size = d.cls.size()[0]
        if tensor_size > 1:
            cls, conf, box = d.cls.squeeze(), d.conf.squeeze(), d.xyxy.squeeze()
        else:
            cls, conf, box = d.cls, d.conf, d.xyxy

        return cls, conf, box

    def update(self, frame):

        cls, conf, box = self.tensorrt_detection(self.model, frame)
        # Pack together for easy use
        detection_output = list(zip(cls, conf, box))
        image_output = utils.draw_box(frame, detection_output, self.label_map, self.COLORS)
        return image_output
