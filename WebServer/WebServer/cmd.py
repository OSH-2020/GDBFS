import sys
import getopt
import os
import subprocess


def add(file: str, option: list):
    """
    加入文件/新建文件
    file 是文件路径
    option 是参数
    """
    cmd = "cp {file_path} /mnt".format(file_path=file)
    option.insert(0, cmd)
    subprocess.call(option, shell=True)


def rm(file: str, option: list):
    """
    删除文件
    file 是文件名
    option 是参数
    """
    cmd = "rm /mnt/{file_name}".format(file_name=file)
    option.insert(0, cmd)
    subprocess.call(option, shell=True)


def open(file: str, option: list):
    """
    打开文件
    file 是文件名
    option 是参数
    """
    cmd = "nohup xdg-open /mnt/{file_name}".format(file_name=file)  # 有了nohup就不会莫名其妙中断了，但是会生成一个文件nohup.out
    option.insert(0, cmd)
    option.append('&')
    subprocess.call(option, shell=True)
