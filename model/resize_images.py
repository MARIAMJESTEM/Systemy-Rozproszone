import cv2
import os


base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/satelites/main_base"))
for file_name in os.listdir(base_path):
    img_path = os.path.join(base_path, file_name)
    if os.path.isfile(img_path):
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

        scale_percent = 200  # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        cv2.imwrite(img_path, resized)
