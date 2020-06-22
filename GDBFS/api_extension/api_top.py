import sys
import os
import importlib
# from .api_functions.yake_api import keyword_yake_api
# from .api_functions.file_information_extractor import get_file_information
# from .api_functions.photo_extraction import keyword_photo_extract


# TODO:增加关键词判优函数，增加API数量，通过不同API返回关键词的比较和综合，得到最终关键词列表
# TODO:增加音乐、视频等的识别
def get_keywords_properties(filepath, keys_limit=-1, filename_extension_specified=None):
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
            if len(attr) < 3:
                continue
            # 解析可以进行信息提取的文件拓展名列表
            adapted_filename_extension = attr[2].split(',')
            if not adapted_filename_extension:
                continue
            # 加载模块
            module = importlib.import_module('.', attr[0].replace('.py', ''))
            if(attr[1] == 'keywords'):
                for extension in adapted_filename_extension:
                    if (extension == filename_extension) or (extension == 'all'):
                        keywords = {**keywords, **module.get_keywords(filepath)}
                        break
            elif(attr[1] == 'properties'):
                for extension in adapted_filename_extension:
                    if (extension == filename_extension) or (extension == 'all'):
                        properties = {**properties, **module.get_properties(filepath)}
                        break
    return {'keywords': list(keywords.keys())[:keys_limit], 'properties': properties}


if __name__ == "__main__":
    print(get_keywords_properties(sys.argv[1]))
