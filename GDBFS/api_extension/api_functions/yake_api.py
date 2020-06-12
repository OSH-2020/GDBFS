import yake
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

        # 提取关键字 offline
        if state == 0:
            kw_extractor = yake.KeywordExtractor()
            keywords = kw_extractor.extract_keywords(text)
            # 统一数据结构
            length = len(keywords)
            keywords_final = {}
            for i in range(length):
                unit = {keywords[i][1]: keywords[i][0]}
                keywords_final.update(unit)
                # print(keywords_final[i])
        else:
            # 提取关键字 online
            url = 'http://yake.inesctec.pt/yake/v2/extract_keywords?max_ngram_size=3&number_of_keywords=20'
            data_send = {'content': text}
            result_jsonType = requests.post(url, data=data_send)
            result_dictType = json.loads(result_jsonType.text)
            keywords = result_dictType["keywords"]
            # 统一数据结构
            length = len(keywords)
            keywords_final = {}
            for i in range(length):
                unit = {keywords[i]["ngram"]: keywords[i]["score"]}
                keywords_final.update(unit)

        return keywords_final
