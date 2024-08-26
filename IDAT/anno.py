# -*- coding: utf-8 -*-
# @Author  : LG

from typing import List
from xml.etree import ElementTree as ET
import os


class Annotation(object):
    def __init__(self, category, xmin, ymin, xmax, ymax, is_difficult=False):
        self.category = category
        self.xmin = int(xmin) if isinstance(xmin, str) else xmin
        self.ymin = int(ymin) if isinstance(ymin, str) else ymin
        self.xmax = int(xmax) if isinstance(xmax, str) else xmax
        self.ymax = int(ymax) if isinstance(ymax, str) else ymax

        if is_difficult is not None:
            if isinstance(is_difficult, str):
                is_difficult = False if is_difficult == '0' else True
            if isinstance(is_difficult, int):
                is_difficult = False if is_difficult == 0 else True

        self.is_difficult = is_difficult


class Annotations(object):
    def __init__(self):
        self.annotations: List[Annotation] = []
        self.width:int = None
        self.height:int = None
        self.depth:int = None
        self.image_path:str = None

    def load_annotation_from_xml(self, xml_path):
        tree = ET.parse(xml_path)
        root= tree.getroot()

        size = root.find('size')
        width = size.find('width')
        height = size.find('height')
        depth = size.find('depth')
        self.width = width
        self.height = height
        self.depth = depth

        objs = root.findall('object')
        for obj in objs:
            name = obj.find('name').text
            difficult = obj.find('difficult').text
            bndbox = obj.find('bndbox')
            xmin = bndbox.find('xmin').text
            ymin = bndbox.find('ymin').text
            xmax = bndbox.find('xmax').text
            ymax = bndbox.find('ymax').text
            annotation = Annotation(name, xmin, ymin, xmax, ymax, difficult)
            self.annotations.append(annotation)

    def save_annotation_to_xml(self, xml_path):
        image_root, image_name = os.path.split(self.image_path)
        annotation = ET.Element('annotation')
        tree = ET.ElementTree(annotation)
        folder = ET.Element('folder')
        folder.text = '{}'.format(image_root)
        annotation.append(folder)

        filename = ET.Element('filename')
        filename.text = '{}'.format(image_name)
        annotation.append(filename)

        explain = ET.Element('explain')
        explain.text = '{}'.format('Build by IDAT v1.0')
        annotation.append(explain)

        size = ET.Element('size')
        width = ET.Element('width')
        width.text = '{}'.format(self.width)
        size.append(width)

        height = ET.Element('height')
        height.text = '{}'.format(self.height)
        size.append(height)

        depth = ET.Element('depth')
        depth.text = '{}'.format(self.depth)
        size.append(depth)
        annotation.append(size)

        for anno in self.annotations:

            object = ET.Element('object')
            name = ET.Element('name')
            name.text = anno.category
            object.append(name)

            pose = ET.Element('pose')
            pose.text = 'Unspecified'
            object.append(pose)

            truncated = ET.Element('truncated')
            truncated.text = '0'
            object.append(truncated)

            difficult = ET.Element('difficult')
            difficult.text = '1' if anno.is_difficult else '0'
            object.append(difficult)

            bndbox = ET.Element('bndbox')
            xmin = ET.Element('xmin')
            xmin.text = '{}'.format(int(anno.xmin))
            bndbox.append(xmin)

            ymin = ET.Element('ymin')
            ymin.text = '{}'.format(int(anno.ymin))
            bndbox.append(ymin)

            xmax = ET.Element('xmax')
            xmax.text = '{}'.format(int(anno.xmax))
            bndbox.append(xmax)

            ymax = ET.Element('ymax')
            ymax.text = '{}'.format(int(anno.ymax))
            bndbox.append(ymax)
            object.append(bndbox)
            annotation.append(object)

        # tree.write(xml_path, encoding='utf-8', xml_declaration=True)
        xml_string = ET.tostring(annotation, encoding='utf-8', method='xml')
        print(xml_string)
        from xml.dom import minidom
        xml_pretty = minidom.parseString(xml_string).toprettyxml(indent='    ')
        # print(xml_pretty)
        with open(xml_path, 'w') as f:
            f.write(xml_pretty)
        return True
