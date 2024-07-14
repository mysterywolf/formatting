@echo off
rem 声明采用UTF-8编码
rem 声明采用UTF-8编码
@chcp 65001
::@echo off执行以后，后面所有的命令均不显示，包括本条命令。
@cd /d %~dp0
@start cmd.exe /c "python formatting.py"
