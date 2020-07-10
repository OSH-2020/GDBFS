import os
import requests
import base64
from urllib import request
import ssl
import json
from translate_api import translate_iciba_api
import logging


# 通用物体和场景识别
def get_keywords(filepath, filename_extension=None):
    if((filename_extension != 'jpg') and (filename_extension != 'jpeg') and (filename_extension != 'bmp') and (filename_extension != 'png')):
        logging.debug("%s can't be extracted by photo_extraction, filename_extension is %s", filepath, filename_extension)
        return {}
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
    keywords_final = {}
    try:
        # 二进制方式打开文件
        with open(filepath, 'rb') as f:
            # convert photo to base64
            img = base64.b64encode(f.read())

            # 发送API请求
            params = {"image": img}
            access_token = get_token()
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            # 判断网络是否出现异常
            if response.status_code == 200:
                # 格式转换
                result_dictType = json.loads(response.text)
                length = result_dictType['result_num']
                keywords = result_dictType['result']
                logging.debug("baidu:online api get Chinese keywords %s", keywords)
                # 统一数据结构
                cur_pos = 0
                for i in range(length):
                    # 把中文内容翻译成英文
                    en_keyword = translate_iciba_api(keywords[cur_pos]['keyword'])
                    if en_keyword is None:
                        continue
                    unit = {en_keyword.strip("\n\t \r"): keywords[cur_pos]['score']}
                    keywords_final.update(unit)
                    cur_pos += 1
                logging.debug("baidu:online api get English keywords %s", keywords_final)
            else:
                logging.error("baidu:online api network error with %d", response.status_code)
    except IOError:
        logging.error("baidu:can't open file %s", filepath)
    return keywords_final


# 调取百度接口需要注册账号的access token，token需要使用API key和Secret Key获取
def get_token():
    try:
        # 如果有token文件，则优先使用token，从而不用多次调用获取token的接口
        token_filepath = os.path.join(os.path.dirname(__file__)) + '/token.txt'
        if os.path.exists(token_filepath) is True:
            logging.info("baidu:find token file")
            with open(token_filepath, 'r', encoding='utf-8') as f:
                token = f.readline().strip(' \t\n')
        else:
            logging.info("baidu:cat't find token file, trying to find key file")
            # 如果没有token文件，则使用key获取token并保存
            gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            key_filepath = os.path.join(os.path.dirname(__file__)) + '/key.txt'
            key_file = open(key_filepath, 'r', encoding='utf-8')
            API_Key = key_file.readline().strip(' \t\n')
            Secret_Key = key_file.readline().strip(' \t\n')
            key_file.close()
            host = 'https://aip.baidubce.com/oauth/2.0/token?grant_' \
                'type=client_credentials&client_id='+API_Key +\
                '&client_secret=' + Secret_Key
            req = request.Request(host)
            response = request.urlopen(req, context=gcontext).read().decode('UTF-8')
            try:
                result = json.loads(response)
                token = result['access_token']
                logging.info("baidu:successfully get token")
                with open(os.path.split(__file__)[0] + '/token.txt', 'w', encoding='utf-8') as f:
                    f.write(token)
                logging.info("baidu:write token to file successfully")
            except AttributeError as e:
                logging.error("baidu:network error with: %d", e)
    except IOError:
        logging.error("baidu:file open error!")
    return token
