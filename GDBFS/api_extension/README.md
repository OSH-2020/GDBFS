# Notes for API
您可以使用`./onestep.sh`来执行一键安装一部分所需要的库，如果其中有出错，请移步Google
## Note for api_top
返回值{'keywords':[key1,key2,...],'properties':[proper1:information1,proper2:information2,...]}
### 调用方法
```python
from api_functions import api_top
result = api_top.get_keywords_properties(<filepath>)
# 示例
# 在/usr/local下有一个text.txt文件
# 建议不管文件在何处，都要填完整路径
>>> from GDBFS.api_extension import api_top
>>> api_top.get_keywords_properties('/home/ubuntu/test.txt')
# 输出
{'keywords': ['kaggle', 'google', 'ceo anthony goldbloom', 'san francisco', 'ceo anthony', 'data', 'co-founder ceo anthony', 'platform', 'anthony goldbloom declined', 'francisco this week', 'machine learning', 'service', 'acquiring kaggle', 'machine', 'learning', 'conference in san', 'goldbloom', 'ben hamner', 'cloud', 'competition'], 'properties': {'file_size': 2290, 'file_create_time': '2020-06-09T14:52:27', 'file_modified_time': '2020-06-09T14:52:27', 'file_accessed_time': '2020-06-11T17:13:13', 'file_create_location': None}}
```
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

<font color=red size=3>**Attention**</font>  
该函数目前能实现对txt、jpeg、jpg、bmp、png的关键字提取，以及其他文件的属性提取  
该函数不会返回None，keywords只会返回空列表，file_information返回值见file_information_extractor的说明  
TODO:有人会md文件内标题的超链接吗，把file_information_extractor链接到下面的Note for file_information_extractor标题上吧）

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