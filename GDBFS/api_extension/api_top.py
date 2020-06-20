import sys
from .api_functions.yake_api import keyword_yake_api
from .api_functions.file_information_extractor import get_file_information
from .api_functions.photo_extraction import keyword_photo_extract


# TODO:增加关键词判优函数，增加API数量，通过不同API返回关键词的比较和综合，得到最终关键词列表
# TODO:增加音乐、视频等的识别
def get_keywords_properties(filepath, keys_limit=-1, filename_extension_specified=None):
    # 获取文件信息
    if filename_extension_specified is None:
        filename_extension = filepath.split('.')[-1].lower()
    else:
        filename_extension = filename_extension_specified
    file_information = get_file_information(filepath)
    # print(filename_extension)
    if (filename_extension == 'txt') or (filename_extension == 'docx'):
        keywords_yake = keyword_yake_api(filepath, filename_extension)
        # print(keywords_yake)
    else:
        keywords_yake = {}
    if (filename_extension == 'jpg') or (filename_extension == 'jpeg') or (filename_extension == 'png') or (filename_extension == 'bmp'):
        keywords_baidu = keyword_photo_extract(filepath)
        # print(keywords_baidu)
    else:
        keywords_baidu = {}
    keywords = {**keywords_yake, **keywords_baidu}
    return {'keywords': list(keywords.keys())[:keys_limit], 'properties': file_information}


if __name__ == "__main__":
    get_keywords_properties(sys.argv[1])
