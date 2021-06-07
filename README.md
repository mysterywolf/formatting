# Formatting 源码格式自动化调整工具

## 如果喜欢本项目，欢迎star，谢谢

本文件会自动递归遍历**指定文件夹**下的所有文件或者**指定的文件**（默认对.c/.h/.cpp，也可以改成你想要的文件类型）进行扫描：

- 将源文件编码统一为UTF-8

- 将TAB键替换为空格


- 将每行末尾多余的空格删除，并统一换行符为'\n'
- 将RT-Thread版权信息的截至年份修改至今年(若文件不涉及此问题，程序会自动忽略)
- 将上海睿赛德版权信息的截至年份修改至今年(若文件不涉及此问题，程序会自动忽略)


使用时可以直接在命令行参数中指定需要格式化的**文件夹或者文件名**
``` python
▸ python formatting.py [dir/file_name]
```
或者直接运行脚本,根据提示信息,输入要扫描的**文件夹或者文件名**即可。
``` python
▸ python formatting.py
Please enter work path or file to format: test_dir
--------------------------------------------------------------------------
未处理，需人工确认: ISO-8859-1: test_dir/gd32f4xx_rtc.c
自动判断结果仅供参考:
{'encoding': 'ISO-8859-1', 'confidence': 0.73, 'language': ''}
1.GB2312
2.Windows-1252
3.手动输入其他类型编码
4.略过本文件
请输入人工研判结果:
```

## 使用方法

可以通过VS Code等软件，直接打开 `formatting.py` 文件，输入要扫描的文件夹目录或者具体的某个文件，即可运行。

或者，可以通过命令行的方式指定扫描的文件夹目录或者具体的某个文件。

教学视频：https://www.bilibili.com/video/BV1XN411Q7n3



不要忘记先安装依赖软件包：

```shell
pip install -r requirements.txt
```

