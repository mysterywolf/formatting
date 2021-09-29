# -*- coding: UTF-8 -*- 

# COPYRIGHT (C) 2021, Meco Jianting Man <jiantingman@foxmail.com>
#
# SPDX-License-Identifier: MIT License
#
# Change Logs:
# Date           Author       Notes
# 2021-03-02     Meco Man     The first version
# 2021-03-04     Meco Man     增加统一转换成UTF-8编码格式功能
# 2021-03-06     Meco Man     增加人工介入处理交互功能
# 2021-03-07     Meco Man     增加将RT-Thread版权信息的截至年份修改至今年功能
# 2021-03-14     Meco Man     增加将上海睿赛德版权信息的截至年份修改至今年功能
# 2021-06-07     iysheng      Add support with format single file and parse command line parameters
# 2021-08-24     陈迎春       解决格式化脚本需要和被格式化文件放在同一个磁盘的问题
# 2021-08-29     Meco Man     优化文件后缀名的判断

# 本文件会自动对指定路径下的所有文件包括子文件夹的文件（.c/.h/.cpp/.hpp）进行扫描
#   1)将源文件编码统一为UTF-8
#   2)将TAB键替换为空格
#   3)将每行末尾多余的空格删除，并统一换行符为'\n'
#   4)将RT-Thread版权信息的截至年份修改至今年
#   5)将上海睿赛德版权信息的截至年份修改至今年
# 使用时只需要双击本文件，输入要扫描的文件夹路径即可
# 不能保证100%全部成功转换为UTF-8，有一些编码特殊或识别不准确会在终端打印信息，需人工转换

# 欢迎对本文件的功能继续做出补充，欢迎提交PR

import os
import sys
import re
import chardet
import datetime

# 用空格代替TAB键
# 这里并不是简单的将TAB替换成4个空格
# 空格个数到底是多少需要计算，因为TAB制表本身有自动对齐的功能
def tab2spaces(line):
    list_str = list(line)  # 字符串打散成列表，方便操作
    i = list_str.count('\t')

    while i > 0:
        ptr = list_str.index('\t')
        del list_str[ptr]
        space_need_to_insert = 4 - (ptr % 4)
        j = 0
        while j < space_need_to_insert:
            list_str.insert(ptr, ' ')
            j = j + 1

        i = i - 1

    line = ''.join(list_str)  # 列表恢复成字符串
    return line


# 删除每行末尾多余的空格 统一使用\n作为结尾
def formattail(line):
    line = line.rstrip()
    line = line + '\n'
    return line

#搜索RT-Thread版权信息的截至年份修改至今年
def change_rtthread_copyright_year(line):
    search_result = re.search('200[0-9]-20[0-9][0-9]', line, flags=0) # 搜索200x-20xx字样
    if search_result != None:
        if re.search('RT-Thread', line, flags=0) != None: # 同时可以在本行中搜索到‘RT-Thread’字样
            end = search_result.end()
            str_year = str(datetime.datetime.now().year)
            line = line.replace(line[end-4:end], str_year)# 将20xx替换为今年
    return line

#搜索Real-Thread睿赛德版权信息的截至年份修改至今年
def change_realthread_copyright_year(line):
    search_result = re.search('20[0-9][0-9]-20[0-9][0-9]', line, flags=0) # 搜索20xx-20xx字样
    if search_result != None:
        if re.search('Real-Thread', line, flags=0) != None: # 同时可以在本行中搜索到‘Real-Thread’字样
            end = search_result.end()
            str_year = str(datetime.datetime.now().year)
            line = line.replace(line[end-4:end], str_year)# 将20xx替换为今年
    return line

# 对单个文件进行格式整理
def format_codes(filename):
    try:
        filepath = os.path.dirname(filename)
        # 将temp_file放在和filename相同的路径下
        temp_file = filepath + "temp"
        file = open(filename, 'r', encoding='utf-8')
        file_temp = open(temp_file, 'w', encoding='utf-8')
        line_num = 0
        for line in file:
            line = tab2spaces(line)
            line = formattail(line)

            line_num = line_num + 1
            if line_num < 20: #文件前20行对版权头注释进行扫描，找到截至年份并修改至今年
                line = change_rtthread_copyright_year(line)
                line = change_realthread_copyright_year(line)

            file_temp.write(line)
        file_temp.close()
        file.close()
        os.remove(filename)
        os.rename(temp_file, filename)
    except UnicodeDecodeError:
        print("解码失败，该文件处理失败" + filename)
        file_temp.close()
        file.close()
    except UnicodeEncodeError:
        print("编码失败，该文件处理失败" + filename)
        file_temp.close()
        file.close()


def get_encode_info(file):
    encoding = None
    with open(file, 'rb') as f:
        encode_info = chardet.detect(f.read())
        encoding = encode_info['encoding']
        confidence = encode_info['confidence']

        # 对编码的判断可靠性小于90%不予以处理,需要人工介入处理
        if confidence < 0.90:
            if encoding != None:
                print('--------------------------------------------------------------------------')
                print('未处理，需人工确认: ' + encoding + ': ' + file)  # 需要人工确认
                print('自动判读结果仅供参考:')
                print(encode_info)
                man_result = input('1.GB2312\n2.Windows-1252\n3.utf-8\n4.手动输入其他类型编码\n5.略过本文件\n请输入人工研判结果: ')
                if man_result == '1':
                    encoding = 'GB2312'
                elif man_result == '2':
                    encoding == 'Windows-1252'
                elif man_result == '3':
                    encoding == 'utf-8'
                elif man_result == '4':
                    encoding = input('请输入编码类型: ')
                elif man_result == '5':
                    print('本文件略过,继续处理其他文件...')
                    encoding = None
                else:
                    print('输入参数无效,本文件略过,继续处理其他文件...')
    return encoding


# 将单个文件转为UTF-8编码
def convert_to_utf_8(path):
    encoding = get_encode_info(path)
    if encoding == None:
        return False  # 转换失败

    if encoding == 'utf-8': # 若检测到编码为UTF-8则直接返回成功
        return True

    try:
        file = open(path, 'rb+')
        data = file.read()
        string = data.decode(encoding)
        utf = string.encode('utf-8')
        file.seek(0)
        file.write(utf)
        file.close()
        return True  # 转换成功
    except UnicodeDecodeError:
        print("解码失败，该文件处理失败" + path)
        return False
    except UnicodeEncodeError:
        print("编码失败，该文件处理失败" + path)
        return False

def formatfile(file):
    if os.path.splitext(file)[1] in ['.c', '.h', '.cpp', '.hpp']: #处理.c/.h/.cpp/.hpp文件
    # if os.path.splitext(file)[1] in ['.md']: #处理markdown文档
    # if os.path.split(file)[1] in ['Kconfig', 'SConscript']: #处理Kconfig Sconscript
    # if os.path.splitext(file)[1] in ['.json']: #处理.json文件
        if convert_to_utf_8(file) == True: #先把这个文件转为UTF-8编码,1成功
            format_codes(file) #再对这个文件进行格式整理

# 递归扫描目录下的所有文件
def traversalallfile(path):
    filelist = os.listdir(path)
    for file in filelist:
        filepath = os.path.join(path, file)
        if os.path.isdir(filepath):
            traversalallfile(filepath)
        elif os.path.isfile(filepath):
            formatfile(filepath)

def formatfiles():
    if len(sys.argv) > 1:
        worktarget = sys.argv[1] # use the first command line parameter as worktarget
    else:
        worktarget = input('Please enter work path or file to format: ')

    if os.path.isdir(worktarget):
        traversalallfile(worktarget)
    else:
        formatfile(worktarget)

if __name__ == '__main__':
    formatfiles()
