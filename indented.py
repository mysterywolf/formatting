import os

#用空格代替TAB键
def tab2spaces(line):
    list_str = list(line) #字符串变成列表
    i = list_str.count('\t')
    
    while i > 0:
        ptr = list_str.index('\t')
        del list_str[ptr]
        space_need_to_insert = 4 - (ptr%4)
        j = 0
        while j < space_need_to_insert:
            list_str.insert(ptr,' ')
            j = j+1
        
        i = i-1

    line = ''.join(list_str) #列表恢复成字符串
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
        file.close()
    except UnicodeDecodeError:
        file.close()

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
