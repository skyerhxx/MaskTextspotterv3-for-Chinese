import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

root = 'test_output/inference/chinese_test/'
text_result = 'model_chinese_dataset_1000_results/'
pic_result = 'model_chinese_dataset_1000_visu/'
save_path = 'test_output_visu/'
if not os.path.exists(save_path):
    os.mkdir(save_path)
for i in os.listdir(root + pic_result):
    img = cv2.imread(root + pic_result + i)
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  
    with open(root+text_result+'res_'+i.split('.')[0]+'.txt') as f:
        for line in f:
            text = line.split(',')[13]
            # print(text)
            if text == None:
                continue
            # AddText = img.copy()
            # cv2.putText(img, text, (200, 100), cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
            # print(type(img))
            # print(img)
            draw = ImageDraw.Draw(img)
            # 参数依次为 字体、字体大小、编码
            fontStyle = ImageFont.truetype("simsun.ttc", 20, encoding="utf-8")
            # 参数依次为位置、文本、颜色、字体
            # print(line.split(',')[0])
            draw.text((int(line.split(',')[0]), int(line.split(',')[1])), text, 'red', font=fontStyle)
    # print(img)
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    cv2.imwrite(save_path+i, img)
# 将原图片和添加文字后的图片拼接起来


