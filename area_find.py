import cv2
import numpy as np

class ColorFinder:
    def __init__(self, image_path, crop_area, target_color):
        self.image_path = image_path
        self.crop_area = crop_area
        self.target_color = target_color
        self.cropped_image = self.load_and_crop_image()
        self.similar_color_regions = []

    def load_and_crop_image(self):
        # 打开图片
        image = cv2.imread(self.image_path)
        if image is None:
            print("Error: Image cannot be loaded.")
            return None

        # 裁剪图片
        x, y, w, h = self.crop_area
        return image[y:y + h, x:x + w]

    def find_similar_color(self):
        # 创建掩码，寻找与样本颜色相近的像素
        sample_color = target_color  # 取一个目标颜色点
        mask = np.where((np.abs(self.cropped_image - np.array(sample_color)) < [30, 30, 30]).all(axis=-1), 255,0).astype('uint8')

        # 膨胀掩码以连接邻近区域
        kernel = np.ones((5, 5), np.uint8)
        dilated_mask = cv2.dilate(mask, kernel, iterations=1)

        # 找到轮廓
        contours, _ = cv2.findContours(dilated_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 定位相似颜色区域
        self.similar_color_regions = []
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # 过滤小轮廓
                x, y, w, h = cv2.boundingRect(contour)
                self.similar_color_regions.append((x, y, w, h))

    def display_results(self):
        # 检查是否找到相似颜色区域
        if self.similar_color_regions:
            # 画出相似颜色区域并在图片上打印坐标
            for x, y, w, h in self.similar_color_regions:
                cv2.rectangle(self.cropped_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(self.cropped_image, f"({x}, {y})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
             # 输出相似颜色区域的坐标
            for x, y, w, h in self.similar_color_regions:
                print(f"着火区域坐标: ({x}, {y}), 宽: {w}, 高: {h}")
        else:
            # 如果没有找到相似颜色区域，输出消息
            cv2.putText(self.cropped_image, "没有找到着火区域", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),2)

        # 显示结果
        cv2.imshow('Cropped Image', self.cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # 使用示例


image_path = 'screenshots/latest_shoot.png'
crop_area = (0, 90, 1160, 860)  # x, y, width, height
target_color = [255, 255, 255]  # RGB颜色

color_finder = ColorFinder(image_path, crop_area, target_color)
color_finder.find_similar_color()
color_finder.display_results()
