# WebServer

这个文件夹下是GDBFS的一个Web端的操作界面.

## Packages Version

|Packge|Version|
|:-|:-|
|Django|3.0.7|
|py2neo|5.0b1|

## Step-by-Step Usage

### Onestep

只需要执行`python3 start.py`即可启动服务,通过浏览器访问http://localhost:8000/home即可

### Start Up

首先, 你需要打开该项目的Django服务器.

```shell script
python manage.py runserver 0.0.0.0:8000
```

然后你就可以通过浏览器访问主界面(http://localhost:8000/home).

### Mount GDBFS

在主界面中，选择GDBFS的挂载点, 并点击`enter`, 即可进入操作界面.

### Operations

#### 添加文件

点击`添加文件`, 即可添加文件

#### 查找

输入相关信息, 点击`find`即可查找.

#### 打开和删除

查找操作后, 点击文件结点, 右侧会显示相应文件信息, 点击`open`或`delete`即可打开或删除文件.

#### 卸载 GDBFS

点击卸载即可.

## TODO

1. 确认`neo4j`数据库是否启动.
