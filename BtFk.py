# This is BtFk version 0.0.66
# Console is version 0.65
import tkinter as tk
from tkinter import messagebox
import os
import sys
import platform
from pathlib import Path
import subprocess
import hashlib
import requests as requ

name_of_program = os.path.basename(__file__)
fullpath = os.path.dirname(os.path.abspath(__file__))
console_loation = os.path.join(os.environ["TEMP"], "console.py")
a3 = os.path.join(fullpath, "del_console.bat")
a2 = os.path.join(fullpath, "restart.bat")
PVoVP_1 = "0XTf/f/ffffaaaaaa-ffffaaaaaa"
PVOVP_2 = "0XTf/ffffaaaaaa-fffffaaaaa"

class VersionIDError(Exception):
    pass

class FileHashError(Exception):
    pass

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

def play_media_file(file_path):
    """
    Opens a media file using the operating system's default player.
    Accepts a string path or a pathlib.Path object.
    """
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return False
        
    current_os = platform.system()
    
    try:
        if current_os == "Windows":
            os.startfile(file_path)
        elif current_os == "Darwin":
            subprocess.run(["open", file_path], check=True)
        else:
            subprocess.run(["xdg-open", file_path], check=True)
        
        print(f"Successfully started: {os.path.basename(file_path)}")
        return True
        
    except Exception as e:
        print(f"Failed to play file. Error: {e}")
        return False

def make_it_play(root: tk.Tk, dir_path: Path):
    playable_extensions = (
        ".mp4", ".m4v", ".mov", ".mkv", ".avi", ".wmv", ".flv", ".webm", ".mpg", ".mpeg", ".3gp", 
        ".mp3", ".aac", ".wav", ".flac", ".m4a", ".ogg", ".opus", ".wma", ".alac", ".aiff"
    )
    
    end_files = [
        f.name for f in dir_path.iterdir() 
        if f.is_file() and f.suffix.lower() in playable_extensions
    ]

    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    for one_end_file in end_files:
        full_path = os.path.join(dir_path, one_end_file)
        button = tk.Button(
            frame, 
            text=f"play: {one_end_file}?", 
            command=lambda file_to_play=full_path: play_media_file(file_to_play)
        )
        button.pack(fill="x", pady=5)

def verify_file_hash(file_path, expected_hash):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
            
    calculated_hash = sha256_hash.hexdigest()
    return calculated_hash == expected_hash

def install_installer():
    global fullpath

    path = os.path.join(fullpath, "config.txt")
    path2 = os.path.join(fullpath, "installer.exe")

    print("installing installer.exe...")

    installer = requ.get(
        "https://github.com/thompog/installer-helper/releases/download/versions/installer.helper.exe",
        stream=True
    )
    installer.raise_for_status()

    with open(path2, "wb") as file:
        for chunk in installer.iter_content(chunk_size=8192):
            file.write(chunk)

    if not verify_file_hash(
        path2,
        "44FAA24155EFED76E0D24B997DA6F46464A2B7EBB49C23AE4128D5BC9F3CEBE5"
    ):
        os.remove(path2)
        raise FileHashError(
            "file hash is not the same as the website. "
            "This can be a fake file with malware. "
            "The file has been removed."
        )

    print("installing config.txt and replacing old lines...")

    config_file = requ.get(
        "https://raw.githubusercontent.com/thompog/BtFk/refs/heads/main/config.txt"
    )
    config_file.raise_for_status()

    with open(path, "w") as file:
        file.write(config_file.text)

    if not verify_file_hash(
        path,
        "7CF038ED079D451F779E4D91A971C4B51DB04E3BBE4A20297C62F1B0C1D1B5E0"
    ):
        os.remove(path)
        raise FileHashError(
            "file hash is not the same as the website. "
            "This can be a fake file with malware. "
            "The file has been removed."
        )

    with open(path, "r") as file:
        config_lines = file.read().splitlines()

    new_config = []

    for line in config_lines:
        if line == "PATHHERE":
            line = os.path.join(fullpath, "BtFk.py")

        new_config.append(line)

    with open(path, "w") as file:
        file.write("\n".join(new_config))

    print("running installer")
    print()
    print()
    print()

    subprocess.run([path2], check=True)

def make_size(size: tuple[int, int]) -> str:
    if size is None:
        return ""

    width, height = size
    return f"{width}x{height}"

def main(is_max_size: bool, start_messgae_box_auto: bool, will_delete_after_start: bool):
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

    Button_2 = tk.Button(root, text='make it play', command=lambda: make_it_play(root, Path(fullpath)))
    Button_2.pack(padx=20, pady=30)

    root.mainloop()

    print("###############################################")
    return will_delete_after_start

def get_version_ID():
    global fullpath

    path = os.path.join(fullpath, "ver.BtFk.txt")

    version_file = requ.get("https://raw.githubusercontent.com/thompog/BtFk/refs/heads/main/ver.BtFk.txt")
    version_file.raise_for_status()

    with open(path, "w") as file:
        file.write(version_file.text)

    if not verify_file_hash(
        path,
        "151BA65D70CEEEA3F550E8C29C507DBF4D79C29B21FF1AC67E01A1EBA0B0AE8E"
    ):
        os.remove(path)
        raise VersionIDError("0XTffffffaaaa-0XOffffffaaaa")

    with open(path, "r") as file:
        versions = file.read().splitlines()

    ver1 = ""
    ver2 = ""

    for version in versions:
        if version.startswith("PVoVP_1 = "):
            version = version.replace("PVoVP_1 = ", "")
            target = 1

        elif version.startswith("PVOVP_2 = "):
            version = version.replace("PVOVP_2 = ", "")
            target = 2

        else:
            continue

        decoded = ""

        for c in version:
            if c in ("0", "X", "T", "H", "O"):
                continue
            elif c == "/":
                decoded += "."
            elif c == "-":
                decoded += "."
            elif c == "f":
                decoded += "0"
            elif c == "a":
                decoded += "1"
            else:
                decoded += c

        if target == 1:
            ver1 = decoded
        else:
            ver2 = decoded

    if not ver1:
        raise VersionIDError(
            "0XTfffffffffa-0XHfffffffffa-0XOfffffffffa"
        )

    if not ver2:
        raise VersionIDError(
            "1XTfffffffffa-1XHfffffffffa-1XOfffffffffa"
        )

    return ver1, ver2

def check_version_ID() -> bool:
    global PVoVP_1
    global PVOVP_2

    old_PVoVP_1, old_PVoVP_2 = get_version_ID()

    PVoVP_1_good = False
    PVOVP_2_good = False

    if old_PVoVP_1 == PVoVP_1:
        PVoVP_1_good = True

    if old_PVoVP_2 == PVOVP_2:
        PVOVP_2_good = True

    if PVoVP_1_good and PVOVP_2_good:
        return True
    return False

def ask_for_commands(is_on: bool, will_delete: bool | None = None):
    is_maxsize = False
    start_menu = False
    inst_start_banana_message_box = False

    if will_delete:
        delete_after_start = True
    else:
        delete_after_start = False

    print("BtFk Console v0.65")
    print("Type 'help' to show all commands")
    print()

    while is_on:
        if start_menu:
            return main(is_maxsize, inst_start_banana_message_box, delete_after_start)

        command = input(">> ")
        if command == "help":
            print("fullscreen on")
            print("fullscreen off")
            print("start_menu TRUE")
            print("start_menu FALSE")
            print("start_message_box TRUE")
            print("start_message_box FALSE")
            print("delete_after_start TRUE")
            print("delete_after_start FALSE")
            print("clear/cls")
            print("exit")

        if command in ("fullscreen on", "fs on", "FS on", "FS ON", "Fullscreen on", "Fullscreen ON"):
            is_maxsize = True
            print("menu will now start in fullscreen")
        if command in ("fullscreen off", "fs off", "FS off", "FS OFF", "Fullscreen off", "Fullscreen OFF"):
            is_maxsize = False
            print("menu will now that in min screen size")

        if command in ("start_message_box TRUE", "smb TRUE", "SMB TRUE", "smb true", "Start_message_box TRUE", "start_message_box true", "Start_message_box true"):
            inst_start_banana_message_box = True
            print("when starting menu it will start message box automatically")
        if command in ("start_message_box FALSE", "smb FALSE", "SMB FALSE", "smb false", "Start_message_box FALSE", "start_message_box false", "Start_message_box false"):
            inst_start_banana_message_box = False
            print("when starting menu it will not start the message box automatically")

        if command in ("start_menu TRUE", "sm TRUE", "Start_menu TRUE", "start_menu true", "Start_menu true", "SM TRUE", "SM true", "sm true"):
            start_menu = True
            print("starting menu.....")
        if command in ("start_menu FALSE", "sm FALSE", "Start_menu FALSE", "start_menu false", "Start_menu false", "SM FALSE", "SM false", "sm false"):
            start_menu = False
            print("menu will not start until 'start_menu' is True")

        if command in ("delete_after_start TRUE", "delete_after_start true", "Delete_after_start TRUE", "Delete_after_start true", "dat TRUE", "dat true", "DAT true", "DAT TRUE"):
            delete_after_start = True
            print("this program will now almost not delete it all (have to delete some files after runing)")
        if command in ("delete_after_start FALSE", "delete_after_start false", "Delete_after_start FALSE", "Delete_after_start false", "dat FALSE", "dat false", "DAT false", "DAT FALSE"):
            delete_after_start = False
            print("this program will now delete all files that it made")

        if command in ("clear", "cls", ";;clear"):
            os.system('cls' if os.name == 'nt' else 'clear')

        if command in ("exit", "EX", "ex", ";;exit"):
            print("exiting......")
            if delete_after_start:
                if not os.path.exists(a3):
                    with open(a3, "w") as file:
                        file.write(batch_delete_console)
                os.startfile(a3)
            else:
                if not os.path.exists("C:\\Users\\Public\\Documents\\will_not_delete.txt"):
                    with open("C:\\Users\\Public\\Documents\\will_not_delete.txt", "w") as file:
                        file.write("dont delete this is here to make BtFk check it to not delete files that it makes")

            sys.exit(0)

if not check_version_ID():
    print("version ID is not the newest this means that you have and old version")
    print("do you want to install installer for BtFk? (Y/N)")
    ask = input(">> ")
    if ask in ("y", "Y", "Yes", "yes", "yEs", "yeS", "YEs", "YeS", "YES"):
        install_installer()
    else:
        print("when done please install the newest version: https://github.com/thompog/BtFk/releases/tag/verions")
        print()
        print()
        print()

ask = input("do you want to start menu now or go into console (Y/N) ")
if ask == "Y" or ask == "y":
    if os.path.exists("C:\\Users\\Public\\Documents\\will_not_delete.txt"):
        will_del = main(True, False, False)
    else:
        will_del = main(True, False, True)
else:
    will_del = ask_for_commands(True)

if will_del:
    if not os.path.exists(a3):
        with open(a3, "w") as file:
            file.write(batch_delete_console)
    os.startfile(a3)
else:
    if not os.path.exists("C:\\Users\\Public\\Documents\\will_not_delete.txt"):
        with open("C:\\Users\\Public\\Documents\\will_not_delete.txt", "w") as file:
            file.write("dont delete this is here to make BtFk check it to not delete files that it makes")
