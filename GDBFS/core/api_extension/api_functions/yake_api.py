import yake
import requests
import json
import docx
import logging


# TODO: 把该函数改为class形式，并取消state参数设置，通过上层函数调用不同的对象函数来控制online api或offline api
# 目前该函数返回的置信系数时乱序的
def get_keywords(filepath, filename_extension=None):
    if (filename_extension != 'txt') and (filename_extension != 'docx'):
        logging.debug("%s can't be extracted by yake,filename_extension is %s", filepath, filename_extension)
        return {}
    logging.info("yake:ready to extract %s", filepath)
    text = ''
    try:
        if filename_extension == 'txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        elif filename_extension == 'docx':
            f = docx.Document(filepath)
            text = ''
            for para in f.paragraphs:
                text += para.text
        logging.info("yake:successfully got text from %s", filepath)
    except IOError:
        logging.error("yake:can't open file %s", filepath)
        text = ''
    except Exception as err:
        logging.error("yake:unexpect error %s happened,when open file %s", err, filepath)
        text = ''
    keywords = extract_keywords(text)
    return keywords


def extract_keywords(text):
    # 选择 state = 1 离线api，state = 0 使用在线api
    state = 1
    keywords_final = {}
    # 提取关键字 offline
    if state == 1:
        try:
            kw_extractor = yake.KeywordExtractor()
            keywords = kw_extractor.extract_keywords(text)
            # 统一数据结构
            length = len(keywords)
            for i in range(length):
                unit = {keywords[i][1].strip("\n\t \r"): keywords[i][0]}
                keywords_final.update(unit)
            logging.debug("yake:local api get keywords %s", keywords_final)
        except Exception as err:
            logging.error("yake:local api unexpect error: %s", err)
    # 提取关键字 online
    else:
        try:
            url = 'http://yake.inesctec.pt/yake/v2/extract_keywords?max_ngram_size=3&number_of_keywords=20'
            data_send = {'content': text}
            result_jsonType = requests.post(url, data=data_send)
            # 判断网络是否出现异常
            if result_jsonType.status_code != 200:
                logging.error("yake:online api network error with %d", result_jsonType.status_code)
            else:
                logging.info("yake:online api success")
                result_dictType = json.loads(result_jsonType.text)
                keywords = result_dictType["keywords"]
                # 统一数据结构
                length = len(keywords)
                for i in range(length):
                    unit = {keywords[i]["ngram"].strip("\n\t \r"): keywords[i]["score"]}
                    keywords_final.update(unit)
                logging.debug("yake:online api get keywords %s", keywords_final)
        except Exception as err:
            logging.error("yake:online api unexpect error: %s", err)
    return keywords_final
