#coding=utf-8
#2
import re
import os
import os.path
import xml.dom.minidom
import sys,getopt
from xml.sax.handler import ContentHandler
from xml.sax import make_parser

USAGE = r'''
		Usage:：python check.py [-t|-F|-g] -f file_path
			Optional:
			-t : check synset name repeat
			-F : check format of xml
			-g : check format of nlg
			-f : file full path
		'''

l=[]
filesum=0
b=True
start=0
start_up=0
#获得地址
def url(argv):
    path=''
    try:
        opts,args=getopt.getopt(argv,'t:F:g:hf',"help") #t是查文件数据重复，F是查文件格式问题

    except getopt.GetoptError:
        print(USAGE)
        sys.exit()
   
    # if '-t'in argv and '-F'in argv and '-f' in argv:     
    #     path=args[0]
    #     open(path,l)        
    #     check(l)
    #     com(l,filesum)
    if '-F'in argv and '-f' in argv:
        path=args[0]
        open(path,l)
        global b
        b=False         
        check(l)
        
    if '-t'in argv and '-f' in argv:
        if b :
            path=args[0]
            open(path,l) 
                 
        try:
            com(l,filesum)
        except:
            print("文件有错误！请使用-F查找错误")           
    if '-g' in argv and '-f' in argv:
        if b :
            path=args[0]
            open(path,l) 
                 
        try:
            nlg(l,filesum)
        except:
            print("文件有错误！请使用-F查找错误")  

    if path=='':
        print(USAGE)
    else:
        print("输入的地址为：",path)

    # return self.path

# path='C:\\Users\\YZS\\Desktop\\text'# path=input("输入绝对路径：").strip()
#-t查重，读取文件夹
def com(l,filesum):

    #循环读取文件夹内所有文件
    for i in range(filesum):
        #打开xml文档
        dom1 = xml.dom.minidom.parse(l[i])
        #得到文档元素对象
        synsets1=dom1.getElementsByTagName('synset')
        root1=dom1.documentElement
        start=0
        it=iter(synsets1)
        #生成一个集合储存synset name
        synset_set=set()
        #读取本身重复synsets对象
        while True:
            try:
                
                start+=1
                synsets_iter=next(it)
                #用列表把文件synset name 储存起来
                synset_set.add(synsets1[start-1].getAttribute('name'))
                
  
                for file_len in range(start,len(synsets1)):
                    if synsets1[file_len].getAttribute('name')==synsets_iter.getAttribute('name')and synsets1[file_len].getAttribute('name')!='import':
                            print('domainId:',root1.getAttribute('domainId'),'---->synset name:',synsets_iter.getAttribute('name'))
                            print('domainId:',root1.getAttribute('domainId'),'---->synset name:',synsets1[file_len].getAttribute('name'))
                            print('---------------------------')
            except StopIteration:
                break
        #提取pattern内的关键字
        #1、在集合中获取所有template
        templates = root1.getElementsByTagName('template')
        pattern_set=set()
        #2、循环
        for template in templates:
            #3、循环读取到多个pattern内元素
            pattern = template.getElementsByTagName('pattern')

            for pattern_value in pattern:
                #4、正则提取关键字
                pattern_list = re.findall('【(.*?)】',pattern_value.firstChild.data)
                #如果不在集合中则弹出提示
                #1、循环读取提取出的列表中的元素
                for pattern_key in pattern_list:
                    #1、把关键字组成一个集合
                    pattern_set.add(pattern_key)
        #2、减去synset集合看是否为空
        empty_set=pattern_set-synset_set
        
        #3、如果不为空着提示
        if empty_set:
            for empty_set_value in empty_set:
                print('{}文件中的synset name不包含{}'.format(root1.getAttribute('domainId'),empty_set_value))
        
                    
                #     if pattern_key not in synset_set:
                #         print('{}文件中的synset name不包含{}'.format(root1.getAttribute('domainId'),pattern_key))
        #循环文件synset name查询是否有import
        def whether_import(synsets):
            for file_i in range(len(synsets)):
                if synsets[file_i].getAttribute('name')=='import':
                    #如果有import则获取导入的Id名
                    import_Id=synsets[file_i].getAttribute('expr')
                    #循环读取文件夹内所有文件
                    for j in range(filesum):     
                        #打开xml文档
                        dom2= xml.dom.minidom.parse(l[j])
                        #得到文档元素对象
                        synsets2=dom2.getElementsByTagName('synset')
                        root2=dom2.documentElement
                        #判断是否是本身
                        if j !=i:
                            #判断其他文件是否与import_Id相等
                            if root2.getAttribute('domainId') == import_Id:
                                #如果相等则查询是否还含有其他导入import
                                whether_import(synsets2)
                                # 对比俩个文件
                                it=iter(synsets1)
                                while True:
                                    try:                             
                                        synsets_iter=next(it)
                                        for file_len in range(len(synsets2)):
                                            #判断相等且名字不等于import
                                            if synsets2[file_len].getAttribute('name')==synsets_iter.getAttribute('name') and synsets2[file_len].getAttribute('name')!='import':
                                                    print('domainId:',root1.getAttribute('domainId'),'---->synset name:',synsets_iter.getAttribute('name'))
                                                    print('domainId:',root2.getAttribute('domainId'),'---->synset name:',synsets2[file_len].getAttribute('name'))
                                                    print('---------------------------')
                                    except StopIteration:
                                        break
        whether_import(synsets1)                                
#-F检测xml格式错误
def check(l):
    global filesum

    global start
    filesum2=filesum
    for i in range(start,filesum2):
        try:
            parser = make_parser()
            parser.setContentHandler(ContentHandler())
            parser.parse(l[i])
            print('\n\t %s 是没问题的\n' % l[i])
            start+=1
        except Exception as e:
            print('\n\t 发现错误:%s\n' % e)           
            del l[i]
            filesum-=1
            return check(l)
        # finally:
        #     print(i,l,filesum)

#-g检测nlg格式
def nlg(l,filesum):
    # 使用minidom解析器打开 XML 文档
    for i in range(filesum):
        dom = xml.dom.minidom.parse(l[i])
        domain = dom.documentElement
        domain_value = domain.getAttribute('value')  #获取value属性   
        # print(domain_value)
        #  测试value = 'cn.yunzhisheng.s'
        #  d. domain的value属性值应为cn.yunzhisheng.xxx格式 √
        boolean_value = re.search(r'cn\.yunzhisheng\.\w+',domain_value)
        if not boolean_value:
            print('domain的value属性值应为cn.yunzhisheng.xxx格式！')
        values = domain.getElementsByTagName('values')  #   读取values里的元素
        if values:
            if values[0].getElementsByTagName('propertyTemplate'):
                print('values里包含propertyTemplate！')
            if values[0].getElementsByTagName('vauleTemplate'):
                print('values里包含vauleTemplate！')
            value =  values[0].getElementsByTagName('value')    #  读取value里的值
            if not value :
                print('没有value值')
            else :
                for i in range(len(value)): # 循环读取value的数量
                    name = value[i].getAttribute('name')
                    expr = value[i].getAttribute('expr')
                    
                    if not name:
                        print('第{}个value中缺少name属性'.format(i+1))
                        
                    if not expr:
                        print('第{}个value中缺少expr属性'.format(i+1))
        else :
            print('没有values值')





        propertyTemplate = domain.getElementsByTagName('propertyTemplate')  #   读取propertyTemplate里面的元素
        if propertyTemplate :
            if propertyTemplate[0].getElementsByTagName('vauleTemplate') :
                print('propertyTemplate里包含vauleTemplate！')
            if propertyTemplate[0].getElementsByTagName('vaules') :
                print('propertyTemplate里包含vaules！')
            p_template = propertyTemplate[0].getElementsByTagName('template') #   读取template的值
            
            if p_template :
                for t in range(len(p_template)):
                    boolean = True
                    # e. 未来将会在template添加templateId这个属性值，可加判断，但需兼容当前未加的情况 √
                    if p_template[t].hasAttribute('templateId'):
                        pass# print(p_template.getAttribute('templateId'))
                    #   propertyTemplate是否全部只有key值   √
                    try :
                        intent = p_template[t].getElementsByTagName('intent')[0].firstChild.data    #循环读取intent值
                    except Exception:
                        print ('在propertyTemplate中第{}个template没有intent元素'.format(t+1))
                        boolean=False
                    if boolean:
                        
                        # print(re.findall(r'\[\w+:\]',intent))
                        if len(re.findall(r'\[',intent))==len(re.findall(r'\]',intent)):
                            if len(re.findall(r'\[\w+:\]',intent)) != len(re.findall(r'\[',intent)):
                                print('propertyTemplate里第{}个template中intent格式错误！'.format(t+1))
                        else :
                            print('propertyTemplate里第{}个template中方括号数量不一致！'.format(t+1))
                        
                        if p_template[t].getElementsByTagName('context_status'):    #判断是否有context_status属性
                                
                            context_status=p_template[t].getElementsByTagName('context_status')[0].firstChild.data  #读取contest_status值
                        # if re.findall(r'\[\w+:\]',context_status):

                    #   vauleTemplate中至少需要有一个方括号中有value值与key值配对，达到较为精确的匹配效果    
                    
                    # if boolean_key:
                    #     print('propertyTemplate的第{}个template中有精确匹配'.format(t+1))

                    try:
                        expr = p_template[t].getElementsByTagName('expr')[0].firstChild.data    #循环读取expr值
                    except Exception:
                        print('在propertyTemplate中第{}个没有expr元素'.format(t+1))
                    
            else : print('propertyTemplate中没有template值')
        else :
            print('没有propertyTemplate值')    
        
        


        vauleTemplate = domain.getElementsByTagName('vauleTemplate') # 读取valueTemplate里面的元素
        if not vauleTemplate :
            print('没有vauleTemplate值')
        else :
            a=0
            for v in range(len(vauleTemplate)): 
                if vauleTemplate[v].getElementsByTagName('values'):
                    print('vauleTemplate里包含values!')
                if vauleTemplate[v].getElementsByTagName('propertyTemplate'):
                    print('vauleTemplate里包含propertyTemplate!')
                index = vauleTemplate[v].getAttribute('index')  #获取index值
                #<!-- index初始值默认为1，依次增加 --> √
                if not index :
                    print('第{}个vauleTemplate没有index值'.format(v+1)) 
                else :
                    if not int(index)-a == 1:
                        print('第{}个index值有误！index值为{}'.format((v+1),index))
                    a=int(index)
                v_template = vauleTemplate[v].getElementsByTagName('template')  #   读取template的值
                if not v_template:
                    print('第{}个vauleTemplate里没有template值'.format(v+1))
                else :
                    for t in range(len(v_template)):
                        boolean = True
                        # e. 未来将会在template添加templateId这个属性值，可加判断，但需兼容当前未加的情况 √
                        if v_template[t].hasAttribute('templateId'):
                            pass# print(vauleTemplate[v].getAttribute('templateId'))
                        boolean_key = True #判断是否有精准匹配，有value值就变False
                        try:
                            intent = v_template[t].getElementsByTagName('intent')[0].firstChild.data    #读取intent值
                        except Exception:
                            print('第{}个vauleTemplate里第{}个template中没有intent值'.format(v+1,t+1))
                            boolean = False
                        if boolean :
                        # print(re.search(r'\[\w+:\w+\]',intent),intent)
                            if re.search(r'\[\w+:\w+\]',intent):
                                boolean_key = False
                        if v_template[t].getElementsByTagName('context_status'):    #判断是否有context_status属性
                            
                            context_status=v_template[t].getElementsByTagName('context_status')[0].firstChild.data  #读取contest_status值
                            if re.search(r'\[\w+:\w+\]',context_status):
                                boolean_key = False
                        #   vauleTemplate中至少需要有一个方括号中有value值与key值配对，达到较为精确的匹配效果   √ 
                            
                        if boolean_key:
                            print('第{}个vauleTemplate里第{}个template中没有达到精确匹配'.format(v+1,t+1))
                        try:
                            expr = v_template[t].getElementsByTagName('expr')[0].firstChild.data    #读取expr值
                        except Exception:
                            print('第{}个vauleTemplate里第{}个template中没有expr值'.format(v+1,t+1))
                            boolean = False
                        #   c. expr中的对应关系值应由花括号圈起来 √
                        if boolean :
                            if '{'in expr or '}' in expr:
                                if len(re.findall(r'\{',expr))==len(re.findall(r'\}',expr)):    #   验证左右花括号是否相等
                                    # for i in range(len(re.findall(r'{',expr))):
                                    #     print(i)
                                    if len(re.findall(r'{.*?=.*?}',expr)) != len(re.findall(r'\{',expr)):    #如果判断出来的和花括号数量不相等则报错
                                        # print(re.findall(r'{.*?=.*?}',expr),len(re.findall('{',expr)))
                                        print('第{}个vauleTemplate里第{}个template中expr对应关系错误！'.format(v+1,t+1)) 
                        
                                else :
                                    print('第{}个vauleTemplate里第{}个template中expr花括号不相等！'.format(v+1,t+1))



            
#打开文件夹获取里面文件名称
def open(path,l):
    global filesum
    if os.path.isdir(path):  #查看是不是目录
        fileList = os.listdir(path)   #获取path目录下所有文件
        
        for filename in fileList:    #获取文件名字
            pathTmp = os.path.join(path,filename)   #获取path与filename组合后的路径 
            if os.path.isdir(pathTmp):   #如果是目录
                open(pathTmp,l)        #则递归查找
            elif filename[-4:].upper()=='.XML':   #不是目录,则比较后缀名
                l.append(pathTmp)
        filesum=len(l)
    else:# elif filename[-4:].upper()=='.XML':   #不是目录,则比较后缀名
        l.append(path)
        filesum+=1
if __name__ == "__main__":
    url(sys.argv[1:])




