## 关于调用nltk的一些说明
### 安装
* **安装语言包参考**：当你使用正常方式`import nltk`并执行`nltk.download()`之后大概率会遇到问题，推荐使用如下方式：[直接下载data包](https://blog.csdn.net/weixin_34613450/article/details/78682612?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase)  
但是上面的包被打包的有些问题，你需要手动进行一些修改：
    - 手动将其解压完全（指子目录）
    - 这个包`grammars`包命名有点小问题，你需要将`grammers`目录下的内容全拷贝到`grammars`中（并将`grammers`删去）
    - `tokenizers/punkt`、`chunkers/maxent_ne_chunker`目录下新建`PY3`文件夹并将原目录下内容在`PY3`文件夹中备份一次
* **如果你在编译中遇到UnicodeDecodeError**
    ```python
    #take windows for example
    #C:\Users\xxx\AppData\Local\Programs\Python\Python37-32\lib\site-packages\nltk\data.py", line 757
    #delete  
    resource_val = pickle.load(opened_resource) 
    #add
    resource_val = pickle.load(opened_resource, encoding='iso-8859-1')

    ```
