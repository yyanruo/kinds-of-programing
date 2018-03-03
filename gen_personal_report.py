# -*- coding: utf-8 -*- 
import xlrd
from xlrd import open_workbook
import re,sys,os

import smtplib  
from email.mime.text import MIMEText 


#计算所有人总分以及7项指标分数所打败的人数百分比，输出到1.txt
def percentcal():
	data=xlrd.open_workbook('point.xlsx') 
	table=data.sheets()[0]
	data_list=[]
	data_list.extend(table.col_values(5))
	s = data_list
	s2 = s
	s2 = sorted(s2)

	fo = open("1.txt", "w")

	for i in range(len(s)):
		index = s2.index(s[i])
		while (index+1<len(s))and(s2[index+1]==s2[index]):
			index+=1
		s[i] = 100*index/len(s)
		fo.write('%.f'%(s[i])+'\n')
    	#print('%.f'%(s[i]))
	fo.close()

#计算每道问题不为0的人的百分比，输出到2.txt
def danxiang():
	#打开excel文件
	data=xlrd.open_workbook('11.xlsx') 
	#获取第一张工作表（通过索引的方式）
	table=data.sheets()[0]
	n = table.ncols
	m = table.nrows
	fo = open("2.txt","w")
	for i in range(9,n):
		s = []
		s.extend(table.col_values(i))
		h = 100*sum(s)/m
		fo.write('%.f'%(h)+'\n')
		print('%.f'%(h))
	fo.close()

#计算每道问题不为0的人的百分比，输出到3.txt和4.txt
def diyu():
	data=xlrd.open_workbook('point.xlsx') 
	table=data.sheets()[0]
	s1 =[]
	s2 =[]
	s3 =[]
	n = table.ncols
	m = table.nrows
	s33=[]
	for i in range(m):
		s1.append((i+1,table.cell(i,3).value))
		s2.append((i+1,table.cell(i,4).value))
		s3.append((i+1,table.cell(i,5).value))
		s33.append(table.cell(i,5).value)

	s34 = s33
	s1.sort(key=lambda x:x[1])
	s2.sort(key=lambda x:x[1])	
	#计算每人在中西东部地区所击败人数百分百
	print(s1)
	print('\n')
	print(s33)

	ct = 1
	while (ct<len(s1)):
		tmp = []
		while (s1[ct-1][1]==s1[ct][1])and(ct<len(s1)-1):
			tmp.append((s1[ct-1][0],s3[s1[ct-1][0]-1][1]))
			print(ct,s1[ct-1][1])
			ct+=1
		tmp.sort(key=lambda x:x[1])
		tag = s1[ct-1][1]
		for i in range(len(tmp)):
			s33[tmp[i][0]-1] = 100*(i+1)/len(tmp)
			#s33.insert(tmp[i-1][0], 100*i/len(tmp)
		ct+=1

	print(s33)
	fo = open('3.txt','w')
	for i in range(len(s33)):
		fo.write('%.f'%(s33[i])+'\n')	
	fo.close()	
	#计算每人所在省份所击败人数百分比	
	ct = 1
	while (ct<len(s1)):
		tmp = []
		while (s2[ct-1][1]==s2[ct][1])and(ct<len(s2)-1):
			tmp.append((s2[ct-1][0],s3[s2[ct-1][0]-1][1]))
			ct+=1
		tmp.sort(key=lambda x:x[1])
		tag = s2[ct-1][1]
		print(tag,tmp)
		for i in range(len(tmp)):
			s34[tmp[i][0]-1] = 100*(i+1)/len(tmp)
			#s33.insert(tmp[i-1][0], 100*i/len(tmp)
		ct+=1

	fo = open('4.txt','w')
	for i in range(len(s34)):
		fo.write('%.f'%(s34[i])+'\n')
	fo.close()	
	s1 = sorted(s1)

#输出到html
def html(infos,questions):

	# info[0] = emal
	# info[1] = name
	# info[2] = organization
	# info[3] = 区域
	# info[4] = 省份
	# info[5-11] = 7指标 击败人数百分比 
	# info[12]   = 东西中部地区内总分击败人生百分比
	# info[13]   = 省份总分击败人生百分比
	# info[14]   = 总分 击败人数百分比
	# info[15-54]= 单项得分
	nrows=infos.nrows
	for i in range(1,nrows):
		info = []
		info.extend(infos.row_values(i))
		printhtml(info)
		printrec(info,questions)

#打印首段和条形图
def printhtml(info):
	p11 = '<div style="width:600px;background:#fff;padding:25px 20px;border-radius:10px;box-shadow:2px 2px 5px rgba(100,100,100,0.8);color:#121212;font-family:sans-serif;font-size:14px;margin:15px auto 30px">'
	p12 = '，您好，<br><br>您的组织“'
	p13 = '”在NGO2.0发起的<a href="http://ngo20.sxl.cn/6" style="color: #f47373;">中国公益组织互联网使用与传播能力第五次调研</a>中“击败”了全国' 
	p14 = '%参与调研的公益组织，下面是您的组织在各方面上的表现 （%数字为超越了百分之多少的公益组织）。所有的排序和数据仅基于调研收集到的数据。这份邮件仅针对您的组织，希望对您有用。'
	p20 = '<table style="font-size:14px;color:#333;margin:20px auto"><tbody>'
	
	p21 = '<tr><td style="text-align:right;padding-right:10px;padding-bottom:3px;">'
	#中间是7大指标内容
	p22 = '</td><td style="font-size: 12px;font-weight: bold;"><div style="background:'
	#中间是rgb(200,124,100)
	p23 = ';width:'
	#中间是长度
	p24 = 'px;height:12px;display:inline-block;margin-right:5px;"></div>'
	#中间是百分比
	p25 = '%</td></tr>'
	p26 = '</tbody></table>'
	
	filename ='%.f'%(info[55]-1)+info[1]+'.txt'
	fo = open(filename,'w')
	#打印首段
	fo.write(p11+info[1]+p12+info[2]+p13+'%.f'%(info[14])+p14+p20)
	
	#打印条形图
	for i in range(1,11):
		fo.write(p21+part1(i,info)+p22+rgb(info[i+4])+p23+'%.f'%(width(info[i+4]))+p24+'%.f'%(info[i+4])+p25)
	fo.write(p26)
	fo.close()
def rgb(cent):
	if (cent>0)and(cent<=10):
		return 'rgb(203,67,53)'
	elif(cent>10)and(cent<=20):
		return 'rgb(231,76,60)'
	elif(cent>20)and(cent<=30):
		return 'rgb(236,112,99)'
	elif(cent>30)and(cent<=40):
		return 'rgb(220,118,51)'
	elif(cent>40)and(cent<=50):
		return 'rgb(235,152,78)'
	elif(cent>50)and(cent<=60):
		return 'rgb(245,176,65)'
	elif(cent>60)and(cent<=70):
		return 'rgb(39,174,96)'
	elif(cent>70)and(cent<=80):
		return 'rgb(82,190,128)'
	elif(cent>80)and(cent<=90):
		return 'rgb(46,204,113)'
	elif(cent>90)and(cent<=100):
		return 'rgb(88,230,141)'
	else:
		return 'rgb(23,32,42)'
def width(cent):
	return cent*2
def part1(zb,info):
	zb1 = '了解行业信息' 
	zb2 = '宣传组织.倡导公益理念'
	zb3 = '透过互联网获得资源'
	zb4 = '知识管理和信息管理'
	zb5 = '利用互联网协作'
	zb6 = '通过数据和分析提升自己'
	zb7 = '通过互联网提高透明度公信力'
	zb8 = '总成绩:'+info[3]
	zb9 = '总成绩:'+info[4]
	zb10= '总成绩:全部参与组织'
	if zb == 1:
		return zb1
	elif zb == 2:
		return zb2
	elif zb == 3:
		return zb3
	elif zb == 4:
		return zb4
	elif zb == 5:
		return zb5
	elif zb == 6:
		return zb6
	elif zb == 7:
		return zb7
	elif zb == 8:
		return zb8
	elif zb == 9:
		return zb9
	elif zb == 10:
		return zb10
	else:
		return -1

#打印个性化推送部分
def printrec(info,questions):
	# '了解行业信息' : question[0,1,2,3,4,29,30]
	# '宣传组织.倡导公益理念': question[5,6,7,31]
	# '透过互联网获得资源': question[8,18,19,20,21,22]
	# '知识管理和信息管理':quetion[9,10,11,12;16,17;32,33,34,35;]
	# '利用互联网协作': question[26,27,36,37]
	# '通过数据和分析提升自己' :question[23,24,25]
	# '通过互联网提高透明度公信力':question[13,14,15;28;38,39]
	q =[]
	qc = []
	q.extend(questions.col_values(0))
	qc.extend(questions.col_values(1))
	s = []
	for i in range(15,55):
		if info[i]==0:
			s.append(i-15)
	p31 = '<h2 style="margin:25px 0 0;font-size:16px"><b>'
	#中间是大文字
	p32 = '</b>，您可以尝试：</h2>'
	p33 = '<p style="margin:5px 0 0 15px;color:#354704">'
	#中间是小文字
	p34 = ' <span style="color:#0ba7ce;">('
	#中间是分数
	p35 = '%的组织正这样做)</span></p>'
	pf  = '<p style="width:400px;margin:50px auto 10px;text-align:center;font-size:13px;">看完这份报告有什么感想？欢迎您联系我们</a><br><br>您可以在<a href="http://www.ngo20.org/post/2882.html" style="color: #f47373;">NGO2.0的网站</a>查看到完整版的调研报告<br>欢迎您来<a href="http://www.ngo20map.com/" style="color: #f47373;">公益地图</a>补充信息并结识更多的公益组织<br>您可以在<a href="http://tools.ngo20map.com/" style="color: #f47373;">公益工具箱</a>上了解更多的工具<br>再次感谢您参与本次调研<br><br></p></div>'
	
	filename ='%.f'%(info[55]-1)+info[1]+'.txt'
	fo = open(filename,'a+')
	for i in range(1,8):
		a = check(i,s)
		if a:
			fo.write(p31+part1(i,info)+p32)
			for j in range(len(a)):
			 	fo.write(p33+site(a[j],q[a[j]])+p34+qc[a[j]]+p35) 
	fo.write(pf)
	fo.close 			
def site(num, s):
	s1 = '使用<a href="http://tools.ngo20.org/index.php/post/145" style="color: #f47373;">灵析</a>、<a href="http://tools.ngo20.org/index.php/post/97" style="color: #f47373;">麦客CRM</a>、<a href="http://tools.ngo20.org/index.php/post/47" style="color: #f47373;">今目标</a>等<a href="http://tools.ngo20.org/index.php/tool/7" style="color: #f47373;">在线志愿者管理系统</a>'
	s2 = '在互联网上建立一个存储公共资料的地方(如<a href="http://tools.ngo20.org/index.php/post/60" style="color: #f47373;">百度云盘</a>等）'
	s3 = '使用项目管理工具进行项目管理（如<a href="http://tools.ngo20.org/index.php/post/48" style="color: #f47373;">Tower</a>、<a href="http://tools.ngo20.org/index.php/post/153" style="color: #f47373;">Teambition</a>等）'
	s4 = '通过行业门户网站（<a href="http://www.ngo20map.com" style="color: #f47373;">NGO2.0地图</a>等）找企业、基金会或者NGO的项目'
	s5 = '使用行业门户网站（<a href="http://www.ngo20map.com" style="color: #f47373;">NGO2.0地图</a>等）发现新的合作机会'
	s6 = '使用<a href="http://tools.ngo20.org/index.php/tool/15" style="color: #f47373;">谷歌日历、QQ日历等在线日历</a>安排日程'
	s7 = '使用<a href="http://tools.ngo20.org/index.php/tool/16" style="color: #f47373;">YY语音.腾讯QT或skype等工具</a>进行多人在线会议'
	s8 = '使用<a href="http://tools.ngo20.org/index.php/tool/21" style="color: #f47373;">在线文档工具.如百会.OneNote.印象笔记</a>共同编辑文档'
	s9 = '使用在线分析工具（如<a href="http://tools.ngo20.org/index.php/post/229" style="color: #f47373;">百度统计</a>等）对官方网站访问量进行分析'
	s10 ='使用微博分析工具（如<a href="http://tools.ngo20.org/index.php/post/130" style="color: #f47373;">知微</a>等）对官方微博访问量进行分析'
	if num == 10:
		return s1
	elif num == 16:
		return s2
	elif num == 17:
		return s3
	elif num == 21:
		return s4
	elif num == 22:
		return s5
	elif num == 27:
		return s6
	elif num == 36:
		return s7
	elif num == 37:
		return s8
	elif num == 23:
		return s10
	elif num == 24:
		return s9
	else:
		return s
def check(num,s):
	q1 = [0,1,2,3,4,29,30]
	q2 = [5,6,7,31]
	q3 = [8,18,19,20,21,22]
	q4 = [9,10,11,12,16,17,32,33,34,35]
	q5 = [26,27,36,37]
	q6 = [23,24,25]
	q7 = [13,14,15,28,38,39]
	
	a = []
	if num==1:
		for i in range(len(s)):
			for j in q1:
				if s[i]==j:
					a.append(j)
		return a 
	elif num==2:
		for i in range(len(s)):
			for j in q2:
				if s[i]==j:
					a.append(j)
		return a 
	elif num==3:
		for i in range(len(s)):
			for j in q3:
				if s[i]==j:
					a.append(j)
		return a 
	elif num==4:
		for i in range(len(s)):
			for j in q4:
				if s[i]==j:
					a.append(j)
		return a 
	elif num==5:
		for i in range(len(s)):
			for j in q5:
				if s[i]==j:
					a.append(j)
		return a 
	elif num==6:
		for i in range(len(s)):
			for j in q6:
				if s[i]==j:
					a.append(j)
		return a 
	elif num==7:
		for i in range(len(s)):
			for j in q7:
				if s[i]==j:
					a.append(j)
		return a 
	else:
		return a

'''
发送html文本邮件
小五义：http://www.cnblogs.com/xiaowuyi
'''

mail_host="smtp.exmail.qq.com"  #设置服务器
mail_sender="xxxx@xxxxx"    #邮箱
mail_pass="xxxxxx"   #密码 

  
def send_mail(to_list,sub,content):  #to_list：收件人；sub：主题；content：邮件内容
    me=mail_sender   #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content,_subtype='html',_charset='utf-8')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me  
    msg['To'] = to_list  
    try:  
        s = smtplib.SMTP(mail_host,25)  #port file
        #s.set_debuglevel(1) #infomation of mail
        s.login(mail_sender,mail_pass)  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()  
        return True  
    except smtplib.SMTPException:  
        print('error:fail to sent mail ') 
        return False  


if __name__ == '__main__':  
    
    data=xlrd.open_workbook('final.xlsx')
    infos    =data.sheets()[0]
    questions=data.sheets()[1]
    html(infos,questions)
    #diyu()
    ##test 用的邮箱
    mailto_lists = []
    #mailto_lists=['12','qaz5223998@163.com','yangyanruo@gmail.com']  
    #改为下面即可全部发送
    mailto_lists.extend(infos.col_values(0)) 
    filenames = []
    filenames.extend(infos.col_values(1))
    

    for i in range(1,533):
    	filename = '%.f'%(i)+filenames[i]+'.txt'
    	print(mailto_lists[i])
    	fo = open(filename,'r')
    	sub ='NGO2.0发起的中国公益组织互联网使用与传播能力第五次调研个性化报告（仅针对您的组织）'
    	content = fo.read()
    	if send_mail(mailto_lists[i],sub,content):  
        	print(filename+"发送成功")
    	else:  
        	print(filename+"发送失败") 




















