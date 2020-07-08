# Notes for API

您可以使用`./onestep.sh`来执行一键安装一部分所需要的库，如果其中有出错，请移步Google

## Note for api_top

返回值{'keywords':[key1,key2,...],'properties':[proper1:information1,proper2:information2,...]}

### 调用方法

```python
from api_functions import api_top
result = api_top.get_keywords_properties(<filepath>)
# 示例
# 在/home/ubuntu/下有一个text.txt文件
# 建议不管文件在何处，都要填完整路径
>>> from GDBFS.api_extension import api_top
>>> api_top.get_keywords_properties('/home/ubuntu/test.txt')
# 输出
{'keywords': ['kaggle', 'google', 'ceo anthony goldbloom', 'san francisco', 'ceo anthony', 'data', 'co-founder ceo anthony', 'platform', 'anthony goldbloom declined', 'francisco this week', 'machine learning', 'service', 'acquiring kaggle', 'machine', 'learning', 'conference in san', 'goldbloom', 'ben hamner', 'cloud', 'competition'], 'properties': {'file_size': 2290, 'file_create_time': '2020-06-09T14:52:27', 'file_modified_time': '2020-06-09T14:52:27', 'file_accessed_time': '2020-06-11T17:13:13', 'file_create_location': None}}
```

### 关于插件

目前api部分的调用已经可以使用插件了

插件的使用方法如下

+ **若该插件是识别keywords的，则该插件必须有get_keywords函数；若是识别properties的，则必须有get_properties函数**
+ get_keywords函数和get_properties函数都必须有且仅有两个参数，分别是filepath[用于接收要解析文件的绝对路径]，filename_extension[用于接收要解析的文件的类型，通常为后缀名]
+ **判断文件类型是否可以解析的部分需要自己在api中定义，并通过filename_extension参数判断，如果该文件类型不能被api所解析，则需要返回空字典{}**
+ 把插件文件`foo.py`放入`api_functions`文件夹
+ 修改`api_extension/config.txt`

config.txt的文件格式为`[pluginName] [properties/keywords]`

+ `[pluginName]`代表插件文件的名字，例如`foo.py`可以写成`foo`或`foo.py`  
+ `[properties/keywords]`代表该插件可以解析的文件信息种类，如果该插件是解析keywords的就填入keywords  

#### 示例

`foo.py`文件可以解析docx和txt文件的keywords

```
# 项目结构
|- config.txt  
|- api_extension  
    |- foo.py  
# config.txt文件
foo keywords
```

<font color=red size=3>**Attention**</font>  
config.txt文件中要严格按照两项填入，项与项之间用一个空格隔开


### 所需的python库  
requests  
os  
sys  
yake  
json  
base64  
ssl  
urllib  
re  
exifread  
geopy  
time  
docx  
importlib

<font color=red size=3>**Attention**</font>

该函数目前能实现对txt、docx、jpeg、jpg、bmp、png的关键字提取，以及其他文件的属性提取

该函数不会返回None，keywords只会返回空列表，file_information返回值见[file_information_extractor](#note-for-file_information_extractor)的说明

## Note for yake

yake是一个用于关键词提取(keyword extraction)的API

要使用yake请用`pip3 install yake`安装yake,官方github上的安装方式可能无法正常运行  

<font color=red size=3>**Attention**</font>

**yake需要在python 3.x环境下运行**

更多问题请参阅yake官方github:https://github.com/LIAAD/yake  

## Note for baiducloud_api

百度图像识别是一个拥有'通用物体和场景识别'的API，通过上传图片，可以识别出物体所属的类别和名称

要使用该图像识别API，你需要在[百度AI平台](https://ai.baidu.com/)中注册，并获取API Key和Secret Key，并在photo_extraction.py同级目录下建立`key.txt`，第一行为API Key，第二行为Secret Key.

<font color=red size=3>**Attention**</font>

所上传图片需要满足:
+ base编码后大小不超过4M(意味着大图可能要压缩)
+ 最短边至少15px，最长边最大4096px(意味着可能需要裁剪)
+ 支持jpg/png/bmp格式  

更多问题请参阅文档:https://cloud.baidu.com/doc/IMAGERECOGNITION/s/Xk3bcxe21

## Note for translate_api

该函数解析[爱词霸](http://dict-co.iciba.com/search.php)的网页，并从网页返回的结果中，解析出**中文所对应的英文**

该网页的使用方式如下

`http://dict-co.iciba.com/search.php?word=你好`

即可获取’你好‘对应的英文

## Note for file_information_extractor

该函数用于解析文件的"大小，创建时间，修改时间，访问时间，(照片)拍摄地点”

返回值为dict  
{  
 'file_size': fsize,  
 'file_create_time': fctime,  
 'file_modified_time': fmtime,  
 'file_accessed_time': fatime,  
 'file_create_location': location  
 }

当里面任意一个信息获取失败的时候，相应字典的值为None

获取file_create_location时需要保证网络正常，有可能因为网络原因获取失败

### 调用示例
```python
#Example 1(文件不存在)
>>> get_file_information('/home/ubuntu/NotExistFile.jpg')
{'file_size': None, 'file_create_time': None, 'file_modified_time': None, 'file_accessed_time': None, 'file_create_location': None}

#Example 2(文件某些信息不存在)
>>> get_file_information('/home/ubuntu/IncompleteFile.jpg')
{'file_size': 10262, 'file_create_time': '2020-06-10T06:05:55', 'file_modified_time': '2020-06-10T06:05:46', 'file_accessed_time': '2020-06-11T06:30:30', 'file_create_location': None}

#Example 3(所有信息都正常)
>>> get_file_information('/home/ubuntu/NormalFile.jpg')
{'file_size': 3713044, 'file_create_time': '2020-06-11T07:08:56', 'file_modified_time': '2020-06-11T07:07:46', 'file_accessed_time': '2020-06-11T07:08:56', 'file_create_location': [' Jiaxing', ' Zhejiang', ' China']}
```

<font color=red size=3>**Attention**</font>

当遇到文件不存在之类的错误的时候，该函数**不会返回空字典**，而是字典中**每一个字段值都为None**