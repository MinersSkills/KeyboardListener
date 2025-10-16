@echo off
powershell -Command "Start-Process 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\FRC Driver Station.lnk' -Verb runAs"
cmd /c start /min python "C:\Users\Bernardo\Documents\code\ws-vscode\KeyboardListener_Python\opener\keyboard_listener.py"