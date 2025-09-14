from subprocess import run, CalledProcessError
from pathlib import Path
import shutil
from sys import argv, exit
from os import listdir
from shutil import rmtree

print("Packaging...")

Version = None

if len(argv) >= 2:
    Argument = argv[1] if argv[1] in ['t', 'r'] else None
    for PassArgument in argv[1:]:
        VersionUpdate = PassArgument if PassArgument in ['s', 'm', '-'] else None


DistDir = Path("dist")
EggInfoDir = Path("CordForge.egg-info")
BuildVenv = Path("BuildVenv")
BuildVenvPython = BuildVenv / "Scripts" / "python.exe"
TestVenv = Path("TestVenv")
TestVenvPython = TestVenv / "Scripts" / "python.exe"

with open("pyproject.toml", "r") as TOML:
    Content = TOML.readlines()
    PreviousVersion = Content[6].strip().split(" = ")[1].replace("\"", "")
    Stable, Major, Minor = [int(Number) for Number in PreviousVersion.split(".")]
    if VersionUpdate in ["s", "m"]:
        UserInput = input("You sure?\n")
        if UserInput.lower() != "yes": (print("Dumbass"), exit())
        Version = f"{Stable+1}.{0}.{0}" if VersionUpdate == "s" else f"{Stable}.{Major+1}.{0}"
    elif VersionUpdate == "-":
        Version = f"{Stable}.{Major}.{Minor+1}"
    else:
        Version = f"{Stable}.{Major}.{Minor}"
    Content[6] = f'version = "{Version}"\n'
    
with open("pyproject.toml", "w") as TOML:
    TOML.write("".join(Content))

with open("setup.cfg", "r") as CFG:
    Content = CFG.readlines()
    Content[2] = f"version = {Version}\n"

with open("setup.cfg", "w") as CFG:
    CFG.write("".join(Content))

if DistDir.exists():
    for Item in DistDir.iterdir():
        if Item.is_file():
            Item.unlink()
        else:
            shutil.rmtree(Item)

if EggInfoDir.exists():
    for Item in EggInfoDir.iterdir():
        if Item.is_file():
            Item.unlink()
        else:
            shutil.rmtree(Item)


print(f"Building: {Version}")
run([BuildVenvPython, "-m", "build"], shell=True, check=True)
try:
    run([BuildVenvPython, "-m", "twine", "upload", "--repository", "testpypi", "dist/*", "--verbose"], shell=True, check=True)
except CalledProcessError:
    print("Failed to upload test package")
try:
    run([BuildVenvPython, "-m", "twine", "upload", "dist/*", "--verbose"], shell=True, check=True)
except CalledProcessError:
    print("Failed to upload official package")
