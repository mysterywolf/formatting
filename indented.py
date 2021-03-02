#
# File      : indented.py
# This file is part of RT-Thread RTOS
# COPYRIGHT (C) 2006 - 2018, RT-Thread Development Team
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


#本文件会自动对指定路径下的所有文件包括子文件夹的文件（仅针对.c.h）
#进行扫描，将TAB键替换为空格，将每行末尾多余的空格删除，并统一换行符为'\n'
#使用时只需要双击本文件，输入要扫描的文件夹路径即可。

import os

#用空格代替TAB键,这里并不是简单的将TAB替换成4个空格；
#空格个数到底是多少需要计算，因为TAB制表本身有自动对齐的功能
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

# 递归扫描目录下的所有文件
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
    #尝试每种编码
    traversalallfile(workpath,'utf-8')
    traversalallfile(workpath,'gbk')
