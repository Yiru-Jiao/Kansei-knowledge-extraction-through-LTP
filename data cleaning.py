#导入正则库(从页面代码中提取信息)
import re
#导入数值计算库(常规计算)
import numpy as np
#导入科学计算库(拼表及各种分析汇总)
import pandas as pd
#设置文件名列表
filename=['罗技（Logitech）G502',
'苹果（Apple）无线2代',
'罗技（Logitech）G102',
'罗技（Logitech）M330',
'雷蛇（Razer）蝰蛇2000',
'小米（MI）小米便携鼠标',
'罗技（Logitech）G903',
'罗技（Logitech）M545',
'雷柏（Rapoo） MT750',
'罗技（Logitech）M590']
#循环处理
for n in range(10):
	#读取文件
	html = open(filename[n]+'.txt', 'r').read()
	#提取评论字段信息
	content1 = re.findall(r'"guid".*?,"content":(.*?),',html)
	#去除图片代码
	content2 = []
	for i in content1:
		if not "img" in i:
			content2.append(i)
	#去除重复评论
	content=list(set(content2))
	#删除产品信息评论
	comment1 = []
	for i in content:
		if not filename[n] in i:
			comment1.append(i)
	#删除空格和符号码
	comment2 = []
	for i in range(len(comment1)):
		str = comment1[i]
		while '&' in str:
			str = re.sub('&.*;','',str)	
		str = str.replace(' ','')
		comment2.append(str.strip('"'))
	#剔除单纯评论
	comment = []
	for i in range(len(comment2)):
		if len(comment2[i]) > 10 :
			comment.append(comment2[i])
	#将前面提取的各字段信息汇总为table数据表，以便后面分析
	table=pd.DataFrame(comment,columns=['comment'])
	#保存table数据表
	table.to_csv(filename[n]+'.csv')