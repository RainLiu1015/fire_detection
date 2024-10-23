from PIL import Image
import matplotlib.pyplot as plt
import torch
import torchvision.transforms as T
import torchvision
import numpy as np
import cv2


class ObjectDetector:
    def __init__(self, model_path=None, pretrained=True):
        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=pretrained)
        self.model.eval()
        self.COCO_INSTANCE_CATEGORY_NAMES = ['__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
        ]
        if model_path:
            self.model.load_state_dict(torch.load(model_path))

    def get_prediction(self, img_path, threshold):
        img = Image.open(img_path).convert('RGB')
        transform = T.Compose([T.ToTensor()])
        img = transform(img)
        pred = self.model([img])
        pred_class = [self.COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].numpy())]
        pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().numpy())]
        pred_score = list(pred[0]['scores'].detach().numpy())
        pred_t = [pred_score.index(x) for x in pred_score if x > threshold][-1]
        pred_boxes = pred_boxes[:pred_t + 1]
        pred_class = pred_class[:pred_t + 1]
        print("pred_class:", pred_class)
        print("pred_boxes:", pred_boxes)
        return pred_boxes, pred_class

    def object_detection_api(self, img_path, threshold=0.5, rect_th=3, text_size=3, text_th=2):
        boxes, pred_cls = self.get_prediction(img_path, threshold)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        for i in range(len(boxes)):
            boxes1 = tuple(map(int, boxes[i][0]))
            boxes2 = tuple(map(int, boxes[i][1]))
            list1=list(boxes1)
            list1[0]=list1[0]+30
            list1[1]=list1[1]+30
            boxes3=tuple(list1)
            cv2.rectangle(img, boxes1, boxes2, color=(0, 255, 0), thickness=rect_th)
            cv2.putText(img, pred_cls[i], boxes3, cv2.FONT_HERSHEY_PLAIN, text_size, (0, 255, 0), thickness=text_th)
        plt.imshow(img)
        plt.show()


if __name__ == '__main__':
    detector = ObjectDetector()
    detector.object_detection_api(img_path="C://Users/11598/Desktop/13.png")