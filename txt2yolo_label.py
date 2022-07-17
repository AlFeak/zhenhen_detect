# txt2yolo_label.py
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from tqdm import tqdm
import os
from os import getcwd

sets = ['train', 'val', 'test']
classes = ['ZhenHen_Highlights']


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(image_id):
    # try:
        in_file = open(r'data\{}\xml\%s.xml'.format(dir_name) % (image_id), encoding='utf-8')
        out_file = open(r'data\{}\labels\%s.txt'.format(dir_name) % (image_id), 'w', encoding='utf-8')
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            # difficult = obj.find('difficult').text
            cls = obj.find('name').text
            # if cls not in classes or int(difficult) == 1:
            if cls not in classes:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            b1, b2, b3, b4 = b
            # 标注越界修正
            if b2 > w:
                b2 = w
            if b4 > h:
                b4 = h
            b = (b1, b2, b3, b4)
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " +
                           " ".join([str(a) for a in bb]) + '\n')


if __name__ == '__main__':
    wd = getcwd()
    dir_name = '29h'
    for image_set in sets:
        if not os.path.exists(r'data\{}\labels'.format(dir_name)):
            os.makedirs(r'data\{}\labels'.format(dir_name))
        image_ids = open(r'data\{}\labels\%s.txt'.format(dir_name) %
                         (image_set)).readlines()

        list_file = open(r'data\{}/%s.txt'.format(dir_name) % (image_set), 'w')
        for image_id in tqdm(image_ids):
            if image_id !='-':
                image_id = image_id.strip()
                print(image_id)
                list_file.write(r'data\{}\images\%s.bmp'.format(dir_name) % (image_id) +'\n')
            # print("image_id=", image_id)
                convert_annotation(image_id)
        list_file.close()