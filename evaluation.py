# -*- coding:utf-8 -*-
import Levenshtein 

import re
from xpinyin import Pinyin
surplus = ['是','吗','啊','呀','呢','吧','嘛','这','那']
def pinyin(target, answer):
    p = Pinyin()

    dict_num2str = {'1': '一', '2': '俩', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'}

    answer_new = ''
    #数字转换成中文
    for a_i in answer:
        if a_i in dict_num2str.keys():
            answer_new = answer_new + dict_num2str[a_i]
        else:
            answer_new = answer_new + a_i
    #中文转换成拼音
    answer_new = p.get_pinyin(target, '')
    target_new = p.get_pinyin(answer_new, '')

    if target_new == answer_new:
        print(True)
    else:
        print(False)
def split_sents(content): #标点符号删除
    return [sentence for sentence in re.split(r'[“”\"‘’\',，！!.。；;：:\n\r]', content) if sentence]
def start(target, answer):
    # data_dict = read_picture_book()
    # data_id = random.randint(1,3)
    # answer_list = data_dict[data_id]

    #把小数点删除
    num_target = ''.join(target.split('.'))
    num_answer = ''.join(answer.split('.'))

    #把多余的修饰词删除
    for s in surplus:
        if s in answer:
            answer = answer.replace(s,'')
    #数字判断和字符判断不一样
    if num_target.isdigit() and num_answer.isdigit(): #判断是否数字转化为浮点型

        target = float(eval(target))
        answer = float(eval(answer))
        if target == answer :
            print(target)
            print(answer)
            print(True)
        else:
            print(False)
    else:
        target = ''.join(split_sents(target))
        answer = ''.join(split_sents(answer))
        if target in answer :
            # answer_out = random.sample(true_answer_out, 1)[0]
            print(True)
        else:
            text_judge(target, answer)

def text_judge(target, answer):

        assess_num1 = Levenshtein.jaro(answer, target)*20
        assess_num2 = Levenshtein.ratio(answer, target)*40
        assess_num3 = (1 - Levenshtein.distance(target, answer)/len(target))*30
        assess_num = assess_num1 + assess_num2 + assess_num3
        print(assess_num1)
        print(assess_num2)
        print(assess_num3)
        print(Levenshtein.distance(target, answer))
        print('答案评分为：',assess_num)

        if assess_num >= 57 :

            print(True)
        else:
            pinyin(target, answer)
if __name__ == "__main__":
    start('小熊','是熊啊')