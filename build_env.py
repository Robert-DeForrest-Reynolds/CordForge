import subprocess, sys, os, zipfile
from urllib.request import urlretrieve

if sys.platform.startswith("win"):
    print("Windows installation unsupported")
elif sys.platform.startswith("linux"):
    print("Linux Installation")
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run([
        "sudo", "apt", "install", "-y",
        "build-essential", "libssl-dev", "zlib1g-dev",
        "libncurses5-dev", "libncursesw5-dev", "libreadline-dev",
        "libsqlite3-dev", "libgdbm-dev", "libdb5.3-dev",
        "libbz2-dev", "libexpat1-dev", "liblzma-dev",
        "tk-dev", "uuid-dev", "libffi-dev", "wget"
    ])
    subprocess.run(["wget", "https://www.python.org/ftp/python/3.13.7/Python-3.13.7.tgz"])
    subprocess.run(["mkdir", "-p", "install"])
    subprocess.run(["tar", "-xf", "Python-3.13.7.tgz", "-C", "install", "--strip-components=1"])
    subprocess.run(["./configure", f"--prefix={os.getcwd()}/py", "--enable-optimizations"], cwd="install")
    jobs = os.cpu_count() or 2  # fallback to 2 if detection fails
    subprocess.run(["make", "-s", f"-j{jobs}"], cwd="install")
    subprocess.run(["rm", "-r", "Python-3.13.7.tgz"])
    subprocess.run(["make", "install"], cwd="install")
    subprocess.run(["sudo", "rm", "-r", "install"])
    env = os.environ.copy()
    env["PYTHONNOUSERSITE"] = "1"
    subprocess.run(["py/bin/python3", "-m", "pip", "install", "e", "."], env=env)
    subprocess.run(["sudo", "rm", "-r", "build"])
    subprocess.run(["sudo", "rm", "-r", "CordForge.egg-info"])
elif sys.platform.startswith("darwin"):
    print("macOS installation unsupported")
