import sys
import getopt
import os
import subprocess

def add(file, option):
    """
    加入文件/新建文件
    将file cp到一个文件夹里

    file 是文件路径,str类型
    option 是参数
    假设fuse的位置是/mnt/fuse
    """
    cmd = "cp {file_path} /mnt/fuse".format(file_path = file)
    option.insert(0,cmd)
    subprocess.call(option,shell=True)

def rm(file, option):
    """
    删除文件
    file 是文件名
    option 是参数
    假设fuse的位置是/mnt/fuse
    """
    cmd = "rm /mnt/fuse/{file_name}".format(file_name= file)
    option.insert(0,cmd)
    subprocess.call(option,shell=True)

#def open(file, option):

def main(argv):
    try:
        """
            options, args = getopt.getopt(args, shortopts, longopts=[])
            
            参数shortopts：短格式分析串。没有冒号，表示后面不带参数；有冒号，表示后面带参数。
            参数longopts：长格式分析串列表。没有等号，表示后面不带参数；带冒号，表示后面带参数。
            
            返回值options是以元组为元素的列表，每个元组的形式为：(option, value) 
            返回值args是个列表，其中的元素是那些不含'-'或'--'的参数。
        """
        opts, args = getopt.getopt(argv,"",["add=","rm=","open="])
    
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
        sys.exit()
    elif(args[0] == 'rm'):
        rm(args[1], option)
        sys.exit()
    elif(args[0] == 'open'):
        rm(args[1], option)
        sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])