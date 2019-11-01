#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：lc time:2019/11/1
import re 
import sys,getopt

repalce_str = str()
# # def change():
def sort(str_list,not_con,k,m,blank_str):

    if k == m:
        # 修饰生成目标字符串
        new_str_re = blank_str + '<pattern>^'
        for x in str_list:
            new_str_re += '(' + not_con + '.)*' + x

        new_str_re += '(' + not_con + '.)*$<pattern>'
        global repalce_str
        repalce_str += new_str_re + '\n'
    
    else:
        for i in range(k,m+1):
            str_list[i], str_list[k] = str_list[k], str_list[i]#交换
            sort(str_list, not_con, k+1, m,blank_str)
            str_list[i], str_list[k] = str_list[k], str_list[i]#还原
    

# 生成分割'需要'集合列表和'不需要'集合列表
def extract(match_str):
    # str='【打开】,【房间】,灯, (?!【关闭】)'

    str_list = match_str.replace(' ','').split(',') #逗号分割
    str_not_contain = re.search(r"\(\?!(.*)\)",match_str) #提取括号里的‘不需要’字符串
    # print(str_not_contain.group())
    not_con = str_not_contain.group() #字符串形式

    str_list.remove(not_con)#删除'不需要'的
    return  str_list,not_con





def open_file(file_path,goal_path):
    with open(file_path,'r',encoding='utf-8') as f:
        with open(goal_path,'w',encoding='utf-8') as p:
            i=0
            for line in f :
                if line.lstrip().startswith('<pattern>'):
                    i += 1
                    change_xml = re.search('<pattern>(.*)</pattern>',line)
                    str_list,not_con = extract(change_xml.group(1))
                    blank_str = re.search(r'\s*',line).group()
                    sort(str_list,not_con,0,len(str_list)-1,blank_str)
                    global repalce_str
                    p.write(repalce_str)
                    repalce_str = str()

                elif line.lstrip().startswith('<template '):
                    ext = re.search('ext="(.*?);',line)
                    blank_str = re.search(r'\s*',line).group()
                    p.write('{}<template ext="{}">\n'.format(blank_str,ext.group(1)))
                else:
                    p.write(line)
    print('成功生成~\n旧模板:{}\n新模板:{}'.format(file_path,goal_path))

def urls(argv):
    USAGE = r'''
		Usage:：python cmb.py -f file_path -g goal_path
			Optional:
			-g : File target path
			-f : file full path
		'''
    try:
        opts,args=getopt.getopt(argv,'f:hg',"help") #f是导入路径，g是导出路径

    except getopt.GetoptError:
        print(USAGE)
        sys.exit()
    if '-f' in argv and '-g'in argv:
        open_file(argv[1],argv[3])

    else:
        print(USAGE)
if __name__ == "__main__":
    urls(sys.argv[1:])
    # file_path = '槽模板.xml'
    # goal_path = '槽模板2.xml'
    # open_file(file_path,goal_path)

                





