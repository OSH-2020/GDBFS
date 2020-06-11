import yake
import sys
import requests
import json
# TODO:目前只支持txt文件的提取，未来可以增加doc，docx等文件的提取
# TODO: 把该函数改为class形式，并取消state参数设置，通过上层函数调用不同的对象函数来控制online api或offline api
# 目前该函数返回的置信系数时乱序的
def keyword_yake_api(filepath):
	# 选择 state = 0 离线api，state = 1 使用在线api
	state = 0
	with open(filepath, 'r', encoding='utf-8') as f:
		text = f.read()
		
		# 提取关键字
		if state == 0:
			kw_extractor = yake.KeywordExtractor()
			keywords = kw_extractor.extract_keywords(text)
			# 统一数据结构
			keywords_final = [[] for i in keywords]
			length = len(keywords)
			
			for i in range(length):
				# TODO:讨论返回值形式，目前返回值为[[keyword,accuracy],...]形式，之后考虑改成字典
				keywords_final[i].append(keywords[i][1])
				keywords_final[i].append(keywords[i][0])
				# print(keywords_final[i])
		else :
			# 提取关键字
			url = 'http://yake.inesctec.pt/yake/v2/extract_keywords?max_ngram_size=3&number_of_keywords=20'
			data_send = {'content': text}
			result_jsonType = requests.post(url, data = data_send)
			result_dictType = json.loads(result_jsonType.text)
			keywords = result_dictType["keywords"]
			# 统一数据结构
			length = len(keywords)
			keywords_final = [[] for i in keywords]
			for i in range(length):
				keywords_final[i].append(keywords[i]["ngram"])
				keywords_final[i].append(keywords[i]["score"])

		return keywords_final