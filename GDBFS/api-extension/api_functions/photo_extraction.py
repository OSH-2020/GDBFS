import requests
import base64
from urllib import request
import ssl
import json
from translate_api import translate_iciba_api


# 通用物体和场景识别
def keyword_photo_extract(filepath):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
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
        
        # 格式转换
        result_dictType = json.loads(response.text)
        length = result_dictType['result_num']
        keywords = result_dictType['result']
        # 统一数据结构
        keywords_final = [[] for i in range(length)]
        # TODO:讨论返回值形式，目前返回值为[[keyword,accuracy],...]形式，之后考虑改成字典
        cur_pos = 0
        for i in range(length):
            # 把中文内容翻译成英文
            en_keyword = translate_iciba_api(keywords[cur_pos]['keyword'])
            if en_keyword is None:
                continue
            keywords_final[cur_pos].append(en_keyword)
            keywords_final[cur_pos].append(keywords[cur_pos]['score'])
            cur_pos += 1
        return keywords_final


# 调取百度接口需要注册账号的access token，token需要使用API key和Secret Key获取
def get_token():
    try:
        # 如果有token文件，则优先使用token，从而不用多次调用获取token的接口
        with open('token.txt', 'r', encoding='utf-8') as f:
            token = f.readline().strip(' \t\n')
    except:
        # 如果没有token文件，则使用key获取token并保存
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        key_file = open('key.txt', 'r', encoding='utf-8')
        API_Key = key_file.readline().strip(' \t\n')
        Secret_Key = key_file.readline().strip(' \t\n')
        key_file.close()
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_' \
            'type=client_credentials&client_id='+API_Key +\
            '&client_secret=' + Secret_Key
        req = request.Request(host)
        response = request.urlopen(req, context=gcontext).read().decode('UTF-8')
        result = json.loads(response)
        token = result['access_token']
        with open('token.txt', 'w', encoding='utf-8') as f:
            f.write(token)

    return token