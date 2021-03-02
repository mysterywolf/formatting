import os

#用空格代替TAB键
def tab2spaces(line):
    #此处有问题，不是每次都是4个空格的
    line = line.replace('\t','    ')
    return line


#删除每行末尾多余的空格 统一使用\n作为结尾
def formatend(line):
    line = line.rstrip()
    line = line + '\n'
    return line


def change_indent_to_spaces(filename, encode):
    try:
        file=open(filename,'r', encoding=encode)
        file_temp=open('temp','w')
        for line in file:
            line = tab2spaces(line)
            line = formatend(line)
            file_temp.write(line)
        file_temp.close()
        file.close()
        os.remove(filename)
        os.rename('temp',filename)
    except FileNotFoundError:
        print("No file of such name")
    except UnicodeEncodeError:
        pass
    except UnicodeDecodeError:
        pass

def traversalallfile(path,encode):
    filelist=os.listdir(path)
    for file in filelist:
        filepath=os.path.join(path,file)
        if os.path.isdir(filepath):
            traversalallfile(filepath,encode)
        elif os.path.isfile(filepath):
            if filepath.endswith(".c") == True or filepath.endswith(".h") == True: #只扫描.c.h文件
                change_indent_to_spaces(filepath,encode)

if __name__ == '__main__':
    workpath = input('enter work path: ')
    #每种编码都扫一遍
    traversalallfile(workpath,'utf-8')
    traversalallfile(workpath,'gbk')
