# Notes for API
您可以使用`./onestep.sh`来执行一键安装一部分所需要的库，如果其中有出错，请移步Google
## Note for api_top
### 调用方法
```python
python3 api_top.py <filepath>
#示例
#在/usr/local下有一个text.txt文件
#建议不管文件在何处，都要填完整路径
python3 api_top.py /usr/local/text.txt
```
### 所需的python库  
requests  
sys  
yake  
json  
base64  
ssl  
urllib  
re  


<font color=red size=3>**Attention**</font>  
**该函数目前为半成品函数，理想返回值应该为关键字列表**  

## Note for yake
yake是一个用于关键词提取(keyword extraction)的API  
要使用yake请用`pip3 install yake`安装yake,官方github上的安装方式可能无法正常运行  

<font color=red size=3>**Attention**</font>  
**yake需要在python 3.x环境下运行**  
更多问题请参阅yake官方github:https://github.com/LIAAD/yake  

## Note for baiducloud_api
百度图像识别是一个拥有'通用物体和场景识别'的API，通过上传图片，可以识别出物体所属的类别和名称  
要使用该图像识别API，你需要在[百度AI平台](https://ai.baidu.com/)中注册，并获取API Key和Secret Key，填入photo_extraction.py中get_token()函数中相应位置  

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