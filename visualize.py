import os
import argparse
from tqdm import tqdm
from data import Data
import cv2

def config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root_dir", type=str, default="NDLTabNet_PascalVOCformat_ver1")
    parser.add_argument("--save_dir", type=str, default="output")
    parser.add_argument("--line_thickness", type=int, default=1)
    args = parser.parse_args()
    return args




def get_image_list(dir, filename):
    image_list = open(os.path.join(dir, filename)).readlines()
    return [image_name.strip() for image_name in image_list]


def process_image(image_data):
    if not os.path.exists(image_data.image_path):
        image_data.image_path = image_data.image_path.replace("jpg", "png")
    
    image = cv2.imread(image_data.image_path)

    for ann in image_data.annotations:
        box_color = (0, 255, 0)  # Green
        if ann.difficult or ann.truncated:
            box_color = (0, 0, 255)  # Red
        image = cv2.rectangle(
            image,
            (ann.xmin, ann.ymin),
            (ann.xmax, ann.ymax),
            box_color,
            1, 
        )
        image = cv2.putText(
            image,
            ann.logical_location,
            (ann.xmin, ann.ymin),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            1,
        )
    return image


def main():
    args = config()
    img_dir = os.path.join(args.root_dir, "JPEGImages")
    ann_dir = os.path.join(args.root_dir, "Annotations")
    set_dir = os.path.join(args.root_dir, "ImageSets", "Main")

    os.makedirs(args.save_dir, exist_ok=True)

    image_list = sorted(get_image_list(set_dir, 'default.txt'))

    for image_path in image_list:
        image_data = Data(args.root_dir, image_path)
        image_name = image_path.split('/')[-1]
        image = process_image(image_data)
        cv2.imwrite(os.path.join(args.save_dir, f'{image_name}.jpg'), image)

if __name__ == "__main__":
    main()
