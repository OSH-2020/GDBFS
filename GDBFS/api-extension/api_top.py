import sys
from yake_api.yake_api import keyword_yake_api
from baiducloud_api.translate_api.translate_api import translate_iciba_api
from baiducloud_api.photo_extraction import keyword_photo_extract


# TODO:增加关键词判优函数，增加API数量，通过不同API返回关键词的比较和综合，得到最终关键词列表
# TODO:增加图片、音乐等的识别
def get_keywords(filepath):
    keywords_yake = keyword_yake_api(filepath)
    print(keywords_yake)

    return keywords_yake


get_keywords(sys.argv[1])
