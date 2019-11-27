#导入科学计算库(拼表及各种分析汇总)
import pandas as pd
#导入正则库(从页面代码中提取信息)
import re
#导入字符串库
import string
#导入分词库
import pyltp
import os
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
#=====================设置ltp模型目录的路径=============================
LTP_DATA_DIR = 'D:\Applications\python\hit_ltp\ltp_data_v3.4.0'
#=============================模型调用==================================
##分词模型路径，模型名称为'cws.model'
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
##词性标注模型路径，模型名称为'pos.model'
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
##依存句法分析模型路径，模型名称为'parser.model'
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')
##初始化实例
segmentor = pyltp.Segmentor()
postagger = pyltp.Postagger()
parser = pyltp.Parser()
##加载模型
segmentor.load(cws_model_path)
postagger.load(pos_model_path)
parser.load(par_model_path)
print('ready')
#===================================文件级别============================
for n in range(10):
	#读取文件
	opfile = filename[n]+'.csv'
	print(opfile)
	content = pd.read_csv(opfile, engine = 'python', encoding = 'utf-8')
	content = content.comment
	shortcut = []
	#-------------------------------评论级别----------------------------
	#分句(sents_list)
	for t in range(len(content)):	
		sents = pyltp.SentenceSplitter.split(content[t])
		sents_list = list(sents)
		#---------------------------短句级别----------------------------
		for d in range(len(sents_list)):
			#-------------------------短句处理--------------------------
			##分词
			words = segmentor.segment(sents_list[d])
			words_list = list(words) 
			##标注
			postags = postagger.postag(words)
			postags_list = list(postags)
			##句法
			arcs = parser.parse(words, postags)
			arcs_list = ",".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)
			arcs_list = arcs_list.split(',')
			#----------------------筛选含态度的短语---------------------
			#------------------------生成短语索引-----------------------
			combine = [0]*len(words_list)
			for i in range(len(arcs_list)):
				s = re.match('\w*:VOB',arcs_list[i])
				if not str(s) == 'None':
					p = int(re.sub(':.*','',arcs_list[i]))
					combine[p-1]=i
				ss = re.match('\w*:FOB',arcs_list[i])
				if not str(ss) == 'None':
					p = int(re.sub(':.*','',arcs_list[i]))
					combine[p-1]=i
			#----------------------组成短句级短语列表-------------------
			for i in range(len(combine)):
				if combine[i] != 0:
					#---------------组合含态度的短语--------------------
					cut = ''
					#-----------------否定态度修改--------------------
					fword = ['没有','不是','并没']
					judge = [0]*(combine[i]+1)
					for m in range(i,combine[i]+1):
						if words_list[m] in fword:
							judge[m] = 1
					if not 1 in judge:
						for m in range(i,combine[i]+1):
							cut = cut + words_list[m]
					else:
						if postags_list[combine[i]] == 'a' :
							modify = '不' + words_list[combine[i]]
							for m in range(i,combine[i]):
								if judge[m] == 1:
									wo = ''
								else:
									wo = words_list[m]
								cut = cut + wo
							cut = cut + modify
						else:
							for m in range(i,combine[i]+1):
								cut = cut + words_list[m]
					shortcut.append(cut)
	#=====================进一步统计================================
	#----------------------重新分词---------------------------------
	adj = []
	noun = []
	for i in shortcut:
		##分词
		words = segmentor.segment(i)
		words_list = list(words) 
		##标注
		postags = postagger.postag(words)
		postags_list = list(postags)
		#--------有n&adj的短语---------------------------
		if 'a' in postags_list and 'n' in postags_list:
			obn = words_list[postags_list.index('n')]
			noun.append(obn)
			oba = words_list[postags_list.index('a')]
			adj.append(oba)
	#-----------生成n-a索引表------------------------------
	frames = []
	#-----------用户关注点列表---------------
	mylist = list(set(noun))
	for n in mylist:
		adjnew=[]
		#--------某一个用户关注点的用户态度列表------
		for i in range(len(adj)):
			if n == noun[i]:
				adjnew.append(adj[i])
		#----用户态度频数计算-------
		singleadjlist = []
		adjlist = list(set(adjnew))
		for i in adjlist:
			num = str(adjnew.count(i))
			singleadjlist.append(i + 'p='+ num)		
		frames.append(pd.DataFrame({n:singleadjlist}))
	n_a = pd.concat(frames, axis=1)
	#保存table数据表
	n_a.to_csv('pn_'+opfile)
	print(opfile+'down')	
#============================释放模型===================================
print('down')
segmentor.release()
postagger.release()
parser.release()
