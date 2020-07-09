import sys
import os
import importlib
# from .api_functions.yake_api import keyword_yake_api
# from .api_functions.file_information_extractor import get_file_information
# from .api_functions.photo_extraction import keyword_photo_extract


# TODO:增加关键词判优函数，增加API数量，通过不同API返回关键词的比较和综合，得到最终关键词列表
# TODO:增加音乐、视频等的识别
# PM_code专为测试准备，PM_code=1,则只运行keywords，PM_code=2,只运行properties,PM_code=3则两者都运行
def get_keywords_properties(filepath, keys_limit=-1, filename_extension_specified=None, PM_code=3):
    keywords = {}
    properties = {}
    # 获取文件后缀
    if filename_extension_specified is None:
        filename_extension = filepath.split('.')[-1].lower()
    else:
        filename_extension = filename_extension_specified
    # 添加插件
    plugin_path = os.path.join(os.path.dirname(__file__)) + '/api_functions'
    sys.path.append(plugin_path)
    conf_path = os.path.join(os.path.dirname(__file__)) + '/config.txt'
    with open(conf_path, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            attr = line.strip().split(' ')
            if len(attr) < 2:
                continue
            # 加载模块
            module = importlib.import_module('.', attr[0].replace('.py', ''))
            if((attr[1] == 'keywords') and (PM_code&1)):
                keywords = {**keywords, **module.get_keywords(filepath,filename_extension=filename_extension)}
            elif((attr[1] == 'properties') and (PM_code&2)):
                properties = {**properties, **module.get_properties(filepath,filename_extension=filename_extension)}
    keywords_final = list(keywords.keys())[:keys_limit]
    keywords_final += [filename_extension]
    return {'keywords': keywords_final, 'properties': properties}


if __name__ == "__main__":
    print(get_keywords_properties(sys.argv[1]))
