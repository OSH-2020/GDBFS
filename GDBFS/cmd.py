import sys
import getopt
import os
import subprocess

def add(file:str, option:list):
    """
    加入文件/新建文件
    file 是文件路径
    option 是参数
    """
    cmd = "cp {file_path} /mnt".format(file_path = file)
    option.insert(0,cmd)
    subprocess.call(option,shell=True)

def rm(file:str, option:list):
    """
    删除文件
    file 是文件名
    option 是参数
    """
    cmd = "rm /mnt/{file_name}".format(file_name= file)
    option.insert(0,cmd)
    subprocess.call(option,shell=True)

def open(file:str, option:list):
    """
    打开文件
    file 是文件名
    option 是参数
    """
    cmd = "xdg-open /mnt/{file_name}".format(file_name= file)
    option.insert(0,cmd)
    subprocess.call(option,shell=True)

def main():
    while(True):
        str = input("# ")
        argv = str.split()
        if(str == '\n'):
            break

        try:
            """
                options, args = getopt.getopt(args, shortopts, longopts=[])
            
                参数shortopts：短格式分析串。没有冒号，表示后面不带参数；有冒号，表示后面带参数。
                参数longopts：长格式分析串列表。没有等号，表示后面不带参数；带冒号，表示后面带参数。
            
                返回值options是以元组为元素的列表，每个元组的形式为：(option, value) 
                返回值args是个列表，其中的元素是那些不含'-'或'--'的参数。
            """
            opts, args = getopt.getopt(argv,"",[])
    
        except getopt.GetoptError:
            print('Error: GetoptError')
            sys.exit(2)
    
        option = []
        # 处理opts列表,假设都不带参数
        for opt, arg in opts:
            option.append(opt)

        # 处理args列表,假设只有两个元素，第一个是操作，第二个是文件名
        if(args[0] == 'add'):
            add(args[1], option)
            
        elif(args[0] == 'rm'):
            rm(args[1], option)
            
        elif(args[0] == 'open'):
            open(args[1], option)
            

if __name__ == "__main__":
    main()