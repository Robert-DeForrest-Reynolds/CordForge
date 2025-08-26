from subprocess import run
from pathlib import Path
import shutil
from sys import argv, exit

print("Packaging...")

Argument = argv[1] if len(argv) == 2 and argv[1] == "s" or len(argv) == 2 and argv[1] == "m" else None

DistDir = Path("dist")
EggInfoDir = Path("CordForge.egg-info")
VenvPython = Path("BuildVenv") / "Scripts" / "python.exe"

with open("pyproject.toml", "r") as TOML:
    Content = TOML.readlines()
    PreviousVersion = Content[6].strip().split(" = ")[1].replace("\"", "")
    Stable, Major, Minor = [int(Number) for Number in PreviousVersion.split(".")]
    if Argument == "s":
        Version = f"{Stable+1}.{0}.{0}"
    elif Argument == "m":
        Version = f"{Stable}.{Major+1}.{0}"
    else:
        Version = f"{Stable}.{Major}.{Minor+1}"
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

run([VenvPython, "-m", "build"], shell=True, check=True)

run([VenvPython, "-m", "twine", "upload", "--repository", "testpypi", "dist/*", "--verbose"], shell=True, check=True)
