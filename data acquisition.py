import requests
import time
import re
#设置请求中头文件的信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Referer':'https://list.jd.com/list.html?cat=670,686,690'}
#设置Cookie的内容
#设置jdb列表
jd = ['122270672.51.1524224130388537717708|6.1524721908',
'122270672.52.1524224130388537717708|6.1524721908',
'122270672.57.1524224130388537717708|6.1524721908',
'122270672.60.1524224130388537717708|6.1524721908',
'122270672.61.1524224130388537717708|6.1524721908',
'122270672.63.1524224130388537717708|6.1524721908',
'122270672.64.1524224130388537717708|6.1524721908',
'122270672.65.1524224130388537717708|6.1524721908',
'122270672.67.1524224130388537717708|6.1524721908',
'122270672.69.1524224130388537717708|6.1524721908']
#设置URL的第一部分的列表
url1 = ['https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv104483&productId=2269354&score=0&sortType=5&page=',
'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv28532&productId=2187061&score=0&sortType=5&page=',
'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv48038&productId=4155894&score=0&sortType=5&page=',
'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv37101&productId=3290993&score=0&sortType=5&page=',
'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv44383&productId=3756787&score=0&sortType=5&page=',
'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv55864&productId=3633865&score=0&sortType=5&page=',
'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6134&productId=4870951&score=0&sortType=5&page=',
'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv59950&productId=852431&score=0&sortType=5&page=',
'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv12761&productId=4543877&score=0&sortType=5&page=',
'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv8136&productId=4462467&score=0&sortType=5&page=']
#设置URL的第二部分
url2 = '&pageSize=10&isShadowSku=0&fold=1'
#设置文件名列表
filename = ["罗技（Logitech）G502",
"苹果（Apple）无线2代",
"罗技（Logitech）G102",
"罗技（Logitech）M330",
"雷蛇（Razer）蝰蛇2000",
"小米（MI）小米便携鼠标",
"罗技（Logitech）G903",
"罗技（Logitech）M545",
"雷柏（Rapoo） MT750",
"罗技（Logitech）M590"]
#抓取循环
for n in range(10):
	cookie={'PCSYCityID':'560',
	'__jda':'122270672.1524224130388537717708.1524224130.1524661928.1524721908.6',
	'__jdb':jd[n],
	'__jdc':'122270672',
	'__jdu':'1524224130388537717708',
	'__jdv':'122270672|baidu|-|organic|not set|1524661928412',
	'areaId':'1','ipLoc-djd':'1-72-2799-0',
	'ipLocation':'%u5317%u4EAC',
	'mx_xid':'V2_52007VwMWUVhbUV8fSxheDG4HEFRbWFRcHkApVQ1uAkBSWgtOUhcdEUAAbgRCTlQNWlsDSBwJBmdWEVQPXgJYL0oYXAx7AhdOXllDWhdCG1sOYwUiUG1YYlMaTxhcDWcBG1tUX1RZHkAeXAJXABVb',
	'unpl':'V2_ZzNtbUFSSxVwCUEHeBBZBWILFQ4RAkcXIA9BBysRXQxuVBZbclRCFXwUR1FnGlkUZwUZX0BcQxFFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VH8aWQZkBhJfQ1VKHHEKQFJ7H1oEbjMiWnJncxd2AUJTfyldNWYzUAkeUEEUcQtAGXsdXwBkABddQFZBHHwMRFJ9GVoDZgoiXHJU'}
	#拼接URL并乱序循环抓取页面
	for i in range(100):
		i=str(i)
		url=(url1[n]+i+url2)
		r=requests.get(url=url,headers=headers,cookies=cookie)
		html=r.content
		time.sleep(5)
		print("当前抓取页面:",url,"状态:",r)
		html=str(html, encoding = "GBK")
		#将编码后的页面输出为txt文本存储
		with open(filename[n]+".txt", "a") as file:
			file.write(html)
