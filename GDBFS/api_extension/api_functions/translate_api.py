import requests
import re
import logging
'''
该函数用于返回’text‘所对应的英文
返回值：返回网页中的第一个数据，如果网页中没有搜索到需要的结果，则返回None
输入'你好',网页返回'hello,hi,how do you do',但实际函数只返回'hello'
主要是因为这个api没有介绍。。。我直接把网页curl下来了，然后用正则解析(水平太菜) T^T
'''


# TODO:考虑修改网页解析部分，从而函数可以用列表的方式返回多个结果
def translate_iciba_api(text):
    url = 'http://dict-co.iciba.com/search.php'
    data_send = {'word': text}
    # 向网页发送请求
    result_htmlType = requests.post(url, data=data_send)
    if result_htmlType.status_code == 200:
        # 将请求得到的结果进行正则匹配，去掉网页中的垃圾HTML信息
        logging.debug("Translate:successfully get result: %s", result_htmlType)
        result_beforeProcess = re.search('<br><br>\n(.*)&nbsp;&nbsp;\n\n', result_htmlType.text)
        if result_beforeProcess is None:
            logging.warning("Translate:can't find proper word in English,error word is: %s", text)
            result = None
        else:
            # 去除空格和分号
            result = re.sub('&nbsp;&nbsp;(.*)', '', result_beforeProcess.group(1))
            # 去除解释性说明
            result = re.sub('\\[(.*)\\]', '', result)
            logging.info("Translate:successfully get translate: %s", result)
    else:
        logging.error("Translate:network error with code: %d", result_htmlType.status_code)
        result = None
    return result
