from subprocess import run
import sys
from os import cpu_count, getcwd, environ


if sys.platform.startswith("win"):
    print("Windows Installation")
elif sys.platform.startswith("linux"):
    print("Linux Installation")
    run(["sudo", "apt", "update"])
    run([
        "sudo", "apt", "install", "-y",
        "build-essential", "libssl-dev", "zlib1g-dev",
        "libncurses5-dev", "libncursesw5-dev", "libreadline-dev",
        "libsqlite3-dev", "libgdbm-dev", "libdb5.3-dev",
        "libbz2-dev", "libexpat1-dev", "liblzma-dev",
        "tk-dev", "uuid-dev", "libffi-dev", "wget"
    ])
    run(["wget", "https://www.python.org/ftp/python/3.13.7/Python-3.13.7.tgz"])
    run(["mkdir", "-p", "install"])
    run(["tar", "-xf", "Python-3.13.7.tgz", "-C", "install", "--strip-components=1"])
    run(["./configure", f"--prefix={getcwd()}/py", "--enable-optimizations"], cwd="install")
    jobs = cpu_count() or 2  # fallback to 2 if detection fails
    run(["make", "-s", f"-j{jobs}"], cwd="install")
    run(["rm", "-r", "Python-3.13.7.tgz"])
    run(["make", "install"], cwd="install")
    run(["sudo", "rm", "-r", "install"])
    env = environ.copy()
    env["PYTHONNOUSERSITE"] = "1"
    run(["py/bin/python3", "-m", "pip", "install", "e", "."], env=env)
    run(["sudo", "rm", "-r", "build"])
    run(["sudo", "rm", "-r", "CordForge.egg-info"])

elif sys.platform.startswith("darwin"):
    print("macOS Installation")
