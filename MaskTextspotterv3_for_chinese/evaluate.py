import json
from rapidfuzz import string_metric
from collections import namedtuple

def get_textlines_Huawei(gt):
        layers = gt['layers']
        labels = layers[0]['labels']

        TextLine = namedtuple('TextLine', ['group_id', 'textline_type', 'rectangle', 'content', 'children'])
        # Char = namedtuple('Char', ['group_innerid', 'content', 'polygon'])
        Char = namedtuple('Char', ['group_innerid', 'content', 'rectangle'])
        

        #! 一个label是一个文本行
        textlines = []
        for label in labels:
            group_id = label['customInfo'][2]['value']
            textline_type = label['customInfo'][1]['value']
            rectangle = list(map(lambda item: [float(item['x']), float(item['y'])], label['rectangle']))
            textline_content = ''
            try:
                children = label['children']
            except:
                children = None
            else:
                chars = []
                for char in children:
                    assert char['customInfo'][-1]['name'] == 'GroupInnerId'
                    group_innerid = char['customInfo'][-1]['value']
                    assert char['customInfo'][-2]['name'] == 'content'
                    content = char['customInfo'][-2]['value']
                    # polygon = list(map(lambda item: [float(item['x']), float(item['y'])], char['polygon']))
                    rectangle = list(map(lambda item: [float(item['x']), float(item['y'])], label['rectangle']))
                    # char = Char(group_innerid=group_innerid, content=content, polygon=polygon)._asdict()
                    char = Char(group_innerid=group_innerid, content=content, rectangle=rectangle)._asdict()
                    
                    chars.append(char)
                    textline_content += content
                children = chars
            textline = TextLine(group_id=group_id, textline_type=textline_type, rectangle=rectangle, content=textline_content, children=children)._asdict()
            textlines.append(textline)

        return textlines  

test_gt_root = 'datasets/chinese/test_gts/'
test_output_root = 'test_output/inference/chinese_test/'
ans = 0.0
for num in range(1000):
    with open(test_gt_root + '_'+str(num)+'.json', 'r', encoding = 'utf-8') as f:
        a = json.load(f)    #此时a是一个字典对象
    #a是len为2的dict
    # print(type(a))
    x = get_textlines_Huawei(a)
    _list1 = []
    for i in x:
        _list1.append(i['content'])
    _list1 = [i for i in _list1 if(len(str(i))!=0)]
    _list1.sort(key = lambda i:len(i),reverse=True)  
    # print(myList)
    # print(_list1)

    with open(test_output_root + 'model_chinese_dataset_1000_results/res__'+str(num)+'.txt','r', encoding = 'utf-8') as f:
        _list2 = []
        for line in f:
            _list2.append(line.split(',')[13])
        _list2.sort(key = lambda i:len(i),reverse=True) 
        # print(_list2)
    


    l1 = []
    l2 = []
    if (len(_list1)>0 and len(_list2)>0):
        for i in range(len(_list1)):
            min_ = 100
            idx = -1
            for j in range(0,len(_list2)):
                d = string_metric.levenshtein(_list1[i],_list2[j])
                # print(d)
                # print(min_)
                if min_ > d:
                    min_ = d
                    idx = j
            # print(idx)
            l1.append(_list1[i])
            # print(l1)
            # print(l2)
            l2.append(_list2[idx])
            del _list2[idx]
            if(len(_list2) == 0):
                break
        # print(i)
        for k in range(i+1, len(_list1)):
            l1.append(_list1[k])
    
    print(l1)
    print(l2)

    edd = 0.0
    for i in range(min(len(l1),len(l2))):
        # if _list1[i] == '':
        #     edd += 1.0
        # else:
        d = string_metric.levenshtein(l1[i],l2[i])
        if d > len(l1[i]):
            d = len(l2[i])
        edd += d / len(l1[i])
    if len(l1) > 0:
        edd = edd / len(l1)
    print(edd)
    ans += edd
    print(num)

ans = ans / 1000
print('error rate: ', ans)
print('acc: ', 1-ans)