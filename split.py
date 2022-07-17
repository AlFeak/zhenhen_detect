import os
import random
import argparse
import xml.etree.ElementTree as ET

dir_name = '29h'

parser = argparse.ArgumentParser()
parser.add_argument('--xml_path', default=r'data\{}\xml'.format(dir_name), type=str, help='input xml label path')
parser.add_argument('--txt_path', default=r'data\{}\labels'.format(dir_name), type=str, help='output txt label path')
opt = parser.parse_args()

trainval_percent = 1.0
train_percent = 0.9
xmlfilepath = opt.xml_path
txtsavepath = opt.txt_path
total_xml = os.listdir(xmlfilepath)
if not os.path.exists(txtsavepath):
    os.makedirs(txtsavepath)

num = len(total_xml)
list_index = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list_index, tv)
train = random.sample(trainval, tr)

file_trainval = open(os.path.join(txtsavepath, 'trainval.txt') , 'w')
file_test = open(os.path.join(txtsavepath, 'test.txt'), 'w')
file_train = open(os.path.join(txtsavepath,'train.txt'), 'w')
file_val = open(os.path.join(txtsavepath, 'val.txt'), 'w')
a=0
for i in list_index:
    file = open(r'data\{}\xml\%s.xml'.format(dir_name) % (total_xml[i][:-4]), encoding='utf-8')
    tree = ET.parse(file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    name = total_xml[i][:-4] + '\n'
    if w!=0 and h!=0:
        if i in trainval:
            file_trainval.write(name)
            if i in train:
                file_train.write(name)
            else:
                file_val.write(name)
        else:
            file_test.write(name)
    else:
        a=a+1
print(a)
file_trainval.close()
file_train.close()
file_val.close()
file_test.close()