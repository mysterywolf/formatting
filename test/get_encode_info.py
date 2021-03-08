#递归遍历并打印每一个.c/.h/.cpp文件的编码格式文件
import os
import chardet

def get_encode_info(file):
    with open(file, 'rb') as f:
        code = chardet.detect(f.read())
        print(code)

def traversalallfile(path):
    filelist=os.listdir(path)
    for file in filelist:
        filepath=os.path.join(path,file)
        if os.path.isdir(filepath):
            traversalallfile(filepath)
        elif os.path.isfile(filepath):
            if filepath.endswith(".c") == True or filepath.endswith(".h") or filepath.endswith(".cpp")== True:
                get_encode_info(path)

if __name__ == '__main__':
    workpath = input('enter work path: ')
    traversalallfile(workpath)
    