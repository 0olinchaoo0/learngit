#用来存储名片
a=0
count=0#用来保存添加字典的数量
card_infors = []
#new_infor = {}
def print_menu():
	'''完成打印功能菜单 '''
	print("="*50)
	print("		名片管理系统 V0.01")
	print("		1.添加一个新的名片")
	print("		2.删除一个名片")
	print("		3.修改一个名片")
	print("		4.查询一个名片")
	print("		5.显示所有的名片")
	print("		6.退出系统")
	print("="*50)

def modify_card():
	'''完成修改名片的功能'''
#	print("姓名\tQQ\t微信\t住址")
#	print("%s\t%s\t%s\t%s\t"%(temp['name'],temp['qq'],temp['weixin'],temp['addr']))
	find_flag = 0   #0表示没有找到  1表示找到
	find_name = input("请输入要修改的名字:")
	for temp in card_infors:
		if find_name == temp['name']:
			modified_name = input("请输入要修改后的名字:")
			modified_qq = input("请输入要修改后的QQ:")
			modified_weixin = input("请输入要修改后的微信：")
			modified_addr = input("请输入要修改后的地址:")
			temp['name'] = modified_name
			temp['qq'] = modified_qq
			temp['weixin'] = modified_weixin
			temp['addr'] = modified_addr
			find_flag = 1
		if find_flag == 0:
			print("查无此人")

def delete_card():
	'''完成删除名片的功能'''
	find_flag = 0 # 0表示没有此人  1表示有此人
	find_name = input("请输入你要删除的名字：")
	for temp in card_infors:
		if find_name == temp['name']:
			b=temp['sum']
			global a,count
			a-=1
			
			del card_infors[b]
			find_flag = 1
			
			print('b= ',b)
			while True:
				
				print('b(+=1) = ',b)
				temp['sum'] = b	
				b+=1
				print("sum+1 = ",temp['sum']+1)
				if b == a:
					#temp['sum+1'] = b
					break
			
			print("count2 = ",count)
			#print('a= ',a)
			
	if find_flag == 0:
		print("查无次人")
def add_new_card_infor():
	''' 完成添加一个新的名片'''	
	new_name = input("请输入新的名字：")
	new_qq = input("请输入新的QQ:")
	new_weixin = input("请输入新的微信：")
	new_addr = input("请输入新的住址:")
	
	#定义一个字典
	new_infor = {}
	new_infor['name'] = new_name
	new_infor['qq'] = new_qq
	new_infor['weixin'] = new_weixin
	new_infor['addr'] = new_addr
	global a
	new_infor['sum']=a

	a=a+1

	global card_infors
	card_infors.append(new_infor)

def find_card_infor():
	'''用来查询一个名片'''
	find_name = input("请输入你要查询的名字：")
	find_flag = 0 #表示没有找到此人  1表示找到了
	for temp in card_infors:
		if find_name == temp['name']:
			print("姓名\tQQ\t微信\t住址")
			find_flag = 1
			print("%s\t%s\t%s\t%s\t%s"%(temp['name'],temp['qq'],temp['weixin'],temp['addr'],temp['sum']))	
			break
	#判断是否找到了
	if find_flag == 0:
		print("查无此人...")

def show_all_infor():
	global card_infors
	print("姓名\tQQ\t微信\t住址")
	for temp in card_infors:
		print("%s\t%s\t%s\t%s\t%s"%(temp['name'],temp['qq'],temp['weixin'],temp['addr'],temp['sum']))	

def main():
	'''完成对整个程序的控制'''
	print_menu()
	
	while True:
		num = int(input("请输入操作序号:"))
		
		if num == 1:
			add_new_card_infor()
		elif num == 2:
			delete_card()
		elif num == 3:
			modify_card()
		elif num == 4:
			find_card_infor()
		elif num == 5:
			show_all_infor()
		elif num ==  6:
			break
		else:
			print("您输入的序号有误，请重新输入")
main()







