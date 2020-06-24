# GDBFS

## 下一步工作

1. 把input结果转化为cypher语句
    - 建议中间加一层, 关键词转化为为list, 文件时间等转化为dict
    - 把上述结果转化为cypher语句
2. 将查询的结果呈现给用户  
(结果可能就给出一堆路径(列表形式), 或给出neo4j的那种图)
    - 列表形式: 将cypher查询的返回值(应该得用run函数直接运行cypher)中路径提取为一个列表返回
    - neo4j图: **没想好怎么做**, 这得是GUI问题了, 很可能要涉及js等
3. 让用户能直接通过查询结果打开文件等的交互界面或命令行界面
    - **没想好怎么做**
4. 综合起来

## 综合测试文件 top 的使用说明

### 代码内容介绍
在`main()`中, 第一大段代码是用来把sample.py文件夹里的文件加入数据库的, 请确保此时数据库服务已经在运行(`neo4j start`). 其中第二小段用来加一张猫咪图片, 耗时较长, 第一次初始化完可以删掉或者注释掉.
第二大段是高总用来接受用户查询输入的关键词和时间的, 原封不动地复制了一下.
第三大段用以和数据库交互, 将关键词和时间信息输入到数据库, 从而获取文件信息, 并输出之.

### 测试数据

```shell script
python top.py "cats"
```

```shell script
python top.py "a document about neo4j"
```

## 文件类型结点

- 视频
- 音频
- 文档(暂时不要富文本)
- 图片

## 接口说明

### neobase.py
所有测试代码都放在sample.py
#### :class FileNode:
通过给出文件路径等信息, 可以构造该类对象.
##### 方法说明
###### :function push_into():
方法原型:
```
def push_into(self, graph, update_key=False, delete_node=False)
```
将文件结点, 关键词结点及其间关系提交到数据库里.
**注**: 原来的`merge_into()`已弃用. 改用push_into的时候不需要作任何其他修改, 直接将所有merge_into()改为push_into()即可.
#### :Function get_files:
函数原型:
```python
def get_files(graph: Graph, keywords=None, file_properties=None) -> List[FileNode]
```
调用该函数, 能返回图`graph`中满足与`keywords`相邻且满足`file_properties`中条件的文件信息列表(其元素为`dict`)
#### :Function delete_file:
函数原型:
```python
def delete_file(graph: Graph, path: str, properties=None)
```
- 将路径为`path`的文件结点从数据库中删除, 并且相邻关键词结点若已孤立则也删除.
- 如需要给出其他属性, 可以用`properties`参数给出. 但`path`是必须给出的, 因为将会根据path做索引.

### UsrInputConv.py
提供了类`KeyWord`，类内包含转换后的`keywords`，`atime`,`ctime`,`mtime`,均以list类型呈现  
* 时间的默认值为最近三年内
> p.s. 仅通过了独立测试，还没完成包装  
##### example
* 你可以通过`python UsrInputConv.py --help`查看使用方式  
* 一个I/O的示例如下：
```bash
//input
python test.py "a movie about Tom Smith and Jack in USTC" --ctime "in September last year"
//output
keywords:  ['movie', 'Tom Smith', 'Jack', 'USTC']
atime:     [('2017-06-12T00:00:00', '2020-06-12T23:31:37')]
ctime:     [('2019-09-01T00:00:00', '2019-09-30T23:59:59')]
mtime:     [('2017-06-12T00:00:00', '2020-06-12T23:31:37')]

```

## Fuse

### Step by Step

这里讲解怎么使用 `fusebase.py`

首先, 确保目录下有`mnt`文件夹和`GDBFS_root`文件夹.
- `mnt`文件夹: 实际操作(cp, mv等)都是对`mnt`文件夹内文件做的.
- `GDBFS_root`文件夹: 对`mnt`文件夹的操作会同步到该文件夹, 以达成永久保存文件的目的.

然后在一个终端运行挂在GDBFSFuse.
```shell script
python fusebase.py mnt
```

这样, `mnt`文件夹上就挂载好了GDBFS.

此后可以进行一些操作, 因为这些操作有一定顺序关系, 建议你第一次使用的时候按顺序尝试.

假设现在我们**另外打开了一个终端**, 并且工作路径在`mnt`目录下.

#### 添加文件

执行以下代码, 将`sample_files`文件夹下的示例文件复制到`mnt`里, 此时图数据库也会有相应操作.
```shell script
cp ../sample_files/neo4j.txt ./
cp ../sample_files/cat.jpg ./
ls
```
此后, 在你的图数据库中查看操作结果, 你会发现已经创建好了两个文件结点及其关键词结点, 以及之间的关系.
```cypher
MATCH(N) RETURN N
```

#### 查看图片

```
eog cat.jpg
```

#### 编辑文件

执行以下命令, 编辑文件后保存, 退出. 你会发现图数据库中的修改时间, 文件大小等皆有改变.(如果修改比较大, 可能会发生关键词的改变)
```shell script
gedit neo4j.txt
```

#### 重命名文件

```shell script
mv neo4j.txt wtf.txt
```

#### 删除文件

执行以下命令删除文件, 你会发现图数据库中对应结点(和关键词结点)也被删除了.
```shell script
rm neo4j.txt
```

#### 卸载GDBFS

直接Ctrl+C关掉就行了

### 操作结果记录

综合以下操作结果, 目前看来, 需要做的有
1. 在write的时候记录文件写的动作(后面flush再更新)
2. 在flush的时候, 检查有没有经历过write, 若有, 更新.
2. 在rename的时候对文件结点作更新(更新文件名即可, 不必重新更新关键词等)
3. 在unlink的时候删除结点(及其相邻无效了的关键词结点)


#### cat操作

```shell script
[open] 打开了/hh.log
[read] 读了/hh.log
[flush] flush了/hh.log
[release] 释放了/hh.log
```

#### echo hh > hh.log

```shell script
[open] 打开了/hh.log
[flush] flush了/hh.log
[write] 应该调用neo4j相关操作更新 {/hh.log}的关键词等！
[flush] flush了/hh.log
[release] 释放了/hh.log
```

#### rm hh.log

```shell script
[access] /hh.log
[unlink] /hh.log
```

#### gedit hh.log

```shell script
[open] 打开了/hh.log
[readdir] /
[access] /hh.log
[read] 读了/hh.log
[flush] flush了/hh.log
[release] 释放了/hh.log
[access] /hh.log
[access] /hh.log
[access] /hh.log
```

#### 在gedit中保存的时候

```shell script
[open] 打开了/hh.log
[create] 创建了/.goutputstream-IVRFM0
[chown] /.goutputstream-IVRFM0
[chmod] /.goutputstream-IVRFM0
[flush] flush了/hh.log
[release] 释放了/hh.log
[write] 应该调用neo4j相关操作更新 {/.goutputstream-IVRFM0}的关键词等！
[flush] flush了/.goutputstream-IVRFM0
[rename] /.goutputstream-IVRFM0 -> /hh.log
[flush] flush了/hh.log
[release] 释放了/hh.log
[access] /hh.log
[access] /hh.log
```

#### mv 17EB8BD89E18115395F95B881F3AB8A2.jpg pic.jpg

```shell script
[rename] /17EB8BD89E18115395F95B881F3AB8A2.jpg -> /pic.jpg
```

#### eog pic.jpg

```shell script
[open] 打开了/pic.jpg
[read] 读了/pic.jpg
[flush] flush了/pic.jpg
[release] 释放了/pic.jpg
[access] /pic.jpg
```

关闭后没有其他反应.

