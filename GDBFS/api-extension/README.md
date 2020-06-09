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
<font color=red size=3>**Attention**</font>  
**该函数目前为半成品函数，理想返回值应该为关键字列表**  
## Note for yake
yake是一个用于关键词提取(keyword extraction)的API  
要使用yake请用`pip3 install yake`安装yake,官方github上的安装方式可能无法正常运行  

<font color=red size=3>**Attention**</font>  
**yake需要在python 3.x环境下运行**  
更多问题请参阅yake官方github:https://github.com/LIAAD/yake  
