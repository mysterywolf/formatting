#
# File      : formatting.py
# This file is part of RT-Thread RTOS
# COPYRIGHT (C) 2006 - 2021, RT-Thread Development Team
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Change Logs:
# Date           Author       Notes
# 2021-03-02     Meco Man     The first version
# 2021-03-04     Meco Man     增加统一转换成UTF-8编码格式功能


#本文件会自动对指定路径下的所有文件包括子文件夹的文件（仅针对.c.h）进行扫描
#   1)将源文件编码统一为UTF-8;
#   2)将TAB键替换为空格;
#   3)将每行末尾多余的空格删除，并统一换行符为'\n'; 
#使用时只需要双击本文件，输入要扫描的文件夹路径即可
#不能保证100%全部成功转换为UTF-8，有一些编码特殊或识别不准确会在终端打印信息，需人工转换

#欢迎对本文件的功能继续做出补充，欢迎提交PR

import os
import chardet

#用空格代替TAB键
#这里并不是简单的将TAB替换成4个空格
#空格个数到底是多少需要计算，因为TAB制表本身有自动对齐的功能
def tab2spaces(line):
    list_str = list(line) #字符串打散成列表，放边操作
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
def formattail(line):
    line = line.rstrip()
    line = line + '\n'
    return line

#对单个文件进行格式整理
def format_codes(filename):
    try: 
        file=open(filename,'r',encoding = 'utf-8')
        file_temp=open('temp','w',encoding = 'utf-8')
        for line in file:
            line = tab2spaces(line)
            line = formattail(line)
            file_temp.write(line)
        file_temp.close()
        file.close()
        os.remove(filename)
        os.rename('temp',filename)
    except UnicodeDecodeError:
        print("解码失败，该文件处理失败"+filename)
        file_temp.close()
        file.close()
    except UnicodeEncodeError:
        print("编码失败，该文件处理失败"+filename)
        file_temp.close()
        file.close()

def get_encode_info(file):
    encoding = None
    with open(file, 'rb') as f:
        encode_info = chardet.detect(f.read())
        encoding = encode_info['encoding']
        confidence = encode_info['confidence']

        #对编码的判断可靠性小于85%不予以处理,需要人工介入处理;但是如果是Windows-1252或者utf-8可靠性小于85%依然进行处理
        # Windows-1252 是由于意法半导体是法国企业's的'是法语的'导致的
        if confidence < 0.85 and not (encoding == 'Windows-1252' or encoding == 'utf-8'): 
            if encoding != None:
                print('--------------------------------------------------------------------------')
                print('未处理，需人工确认: '+encoding+': '+file) #需要人工确认
                print('自动判断结果仅供参考:')
                print(encode_info)
                man_result = input('1.GB2312\n2.Windows-1252\n3.others\n4.略过本文件\n请输入人工研判结果: ')
                if man_result == '1':
                    encoding = 'GB2312'
                elif man_result == '2':
                    encoding == 'Windows-1252'
                elif man_result == '3':
                    encoding = input('请输入编码类型: ')
                elif man_result == '4':
                    print('本文件略过,继续处理其他文件...')
                else:
                    print('输入参数无效,本文件略过,继续处理其他文件...')
    return encoding

#将单个文件转为UTF-8编码
def convert_to_utf_8 (path):
        encoding = get_encode_info(path)
        if encoding == None:
            return False #转换失败

        if encoding == 'utf-8': #若检测到编码为UTF-8则直接返回成功
            return True
        else:
            try: 
                file=open(path,'rb+')
                data = file.read()
                string = data.decode(encoding)
                utf = string.encode('utf-8')
                file.seek(0)
                file.write(utf)
                file.close()
                return True #转换成功
            except UnicodeDecodeError:
                print("解码失败，该文件处理失败"+path)
                return False
            except UnicodeEncodeError:
                print("编码失败，该文件处理失败"+path)
                return False

# 递归扫描目录下的所有文件
def traversalallfile(path):
    filelist=os.listdir(path)
    for file in filelist:
        filepath=os.path.join(path,file)
        if os.path.isdir(filepath):
            traversalallfile(filepath)
        elif os.path.isfile(filepath):
            if filepath.endswith(".c") == True or filepath.endswith(".h") == True:
                #若为.c/.h文件，则开始进行处理
                if convert_to_utf_8(filepath) == True: #先把这个文件转为UTF-8编码
                    format_codes(filepath) #再对这个文件进行格式整理

def formatfiles():
    workpath = input('enter work path: ')
    traversalallfile(workpath)

if __name__ == '__main__':
    formatfiles()
