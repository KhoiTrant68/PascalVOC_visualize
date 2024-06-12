import os
from bs4 import BeautifulSoup


class Entity():
    def __init__(self, name, xmin, xmax, ymin, ymax, difficult, truncated, logical_location):
        self.name = name
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.difficult = difficult
        self.truncated = truncated
        self.logical_location = logical_location



class Data():
    def __init__(self, root_dir, image_name):
        self.image_name = image_name
        self.image_path = os.path.join(root_dir, "JPEGImages", image_name + ".jpg")
        self.annotation_path = os.path.join(root_dir, "Annotations", image_name + ".xml")
        self.annotations = self.load_gt()

    def load_gt(self):
        annotations = []
        xml_content = open(self.annotation_path).read()
        bs = BeautifulSoup(xml_content, 'xml')
        objs = bs.findAll('object')
        for obj in objs:
            obj_name = obj.findChildren('name')[0].text
            difficult = int(obj.findChildren('difficult')[0].contents[0])
            truncated = int(obj.findChildren('truncated')[0].contents[0])
            bbox = obj.findChildren('bndbox')[0]
            xmin = int(float(bbox.findChildren('xmin')[0].contents[0]))
            ymin = int(float(bbox.findChildren('ymin')[0].contents[0]))
            xmax = int(float(bbox.findChildren('xmax')[0].contents[0]))
            ymax = int(float(bbox.findChildren('ymax')[0].contents[0]))
            attribute = obj.findChildren('attribute')
            start_row = int(float(attribute[3].findChildren('value')[0].contents[0]))
            end_row = int(float(attribute[1].findChildren('value')[0].contents[0]))
            start_col = int(float(attribute[2].findChildren('value')[0].contents[0]))
            end_col = int(float(attribute[0].findChildren('value')[0].contents[0]))
            logical_location = f'{start_row}{end_row}, {start_col}{end_col}'
            annotations.append(Entity(obj_name, xmin, xmax, ymin, ymax, difficult, truncated, logical_location))
        return annotations