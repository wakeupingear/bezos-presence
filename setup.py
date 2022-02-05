import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI"
setup(
    name = "Bezos Presence",
    version = "1.0",
    description = "garbage",
    options = {"build_exe": build_exe_options},
    executables = [Executable("Bezos.py", base=base)]
)