# This is BtFk version 0.0.55
# Console is version 0.55
import tkinter as tk
from tkinter import messagebox
import os
import sys

name_of_program = os.path.basename(__file__)
fullpath = os.path.dirname(os.path.abspath(__file__))
console_loation = os.path.join(os.environ["TEMP"], "console.py")
a3 = os.path.join(fullpath, "del_console.bat")
a2 = os.path.join(fullpath, "restart.bat")

batch_restart = f"""
@echo off
title restarting
echo trying restart
start "" /MIN cmd /c "python {console_loation}"
exit /b 0
"""

batch_delete_console = f"""
@echo off
title deleting console and shuting down
echo deleting console
timeout /t 3 >nul
if exist "{console_loation}" (
    del /Q "{console_loation}"
)
if exist "{a2}" (
    del /Q "{a2}"
)
echo shuting down....
echo.
echo.
echo when your ready press enter this will exit the program
echo hope you liked the program just press on it and it opens agen do not
pause
exit /b 0
"""

if name_of_program != "console.py":
    if not os.path.exists(a3):
        with open(a3, "w") as file:
            file.write(batch_delete_console)

    import shutil

    if os.path.exists(console_loation):
        if not os.path.exists(a2):
            with open(a2, "w") as file:
                file.write(batch_restart)
        
        os.startfile(a2)
        sys.exit(0)

    shutil.copyfile(os.path.abspath(__file__), console_loation)

    if not os.path.exists(a2):
        with open(a2, "w") as file:
            file.write(batch_restart)

    os.startfile(a2)
    sys.exit(0)

print("###############################################")

def make_messagebox():
    messagebox.askyesno("hello what you doing?", "banana")

def make_size(size: tuple[int, int]) -> str:
    if size is None:
        return ""

    width, height = size
    return f"{width}x{height}"

def main(is_max_size: bool, start_messgae_box_auto: bool):
    root = tk.Tk()
    root.title("BtFk - Menu/Page 1")

    if start_messgae_box_auto:
        make_messagebox()

    if is_max_size:
        max_size = root.maxsize()
        root.geometry(make_size(max_size))
    else:
        min_size = root.minsize()
        root.geometry(make_size(min_size))

    Button_1 = tk.Button(root, text='does somthing', command=make_messagebox)
    Button_1.pack(padx=20, pady=20)

    root.mainloop()

    print("###############################################")
    return

def ask_for_commands(is_on: bool):
    is_maxsize = False
    start_menu = False
    inst_start_banana_message_box = False

    print("BtFk Console v0.55")
    print("Type 'help' to show all commands")
    print()

    while is_on:
        if start_menu:
            main(is_maxsize, inst_start_banana_message_box)
            return

        command = input(">> ")
        if command == "help":
            print("fullscreen on")
            print("fullscreen off")
            print("start_menu TRUE")
            print("start_menu FALSE")
            print("start_message_box TRUE")
            print("start_message_box FALSE")
            print("clear/cls")
            print("exit")
        if command == "fullscreen on" or command == "fs on":
            is_maxsize = True
            print("menu will now start in fullscreen")
        if command == "fullscreen off" or command == "fs off":
            is_maxsize = False
            print("menu will now that in min screen size")

        if command == "start_message_box TRUE" or command == "smb TRUE":
            inst_start_banana_message_box = True
            print("when starting menu it will start message box automatically")
        if command == "start_message_box FALSE" or command == "smb FALSE":
            inst_start_banana_message_box = False
            print("when starting menu it will not start the message box automatically")

        if command == "start_menu TRUE" or "sm TRUE":
            start_menu = True
            print("starting menu.....")
        if command == "start_menu FALSE" or "sm FALSE":
            start_menu = False
            print("menu will not start until 'start_menu' is True")

        if command == "clear" or command == "cls" or command == ";;clear":
            os.system('cls' if os.name == 'nt' else 'clear')

        if command == "exit" or command == "EX" or command == ";;exit":
            print("exiting......")
            if not os.path.exists(a3):
                with open(a3, "w") as file:
                    file.write(batch_delete_console)
            os.startfile(a3)
            sys.exit(0)

ask = input("do you want to start menu now or go into console (Y/N) ")
if ask == "Y" or ask == "y":
    main(True, False)
else:
    ask_for_commands(True)

if not os.path.exists(a3):
    with open(a3, "w") as file:
        file.write(batch_delete_console)
os.startfile(a3)
