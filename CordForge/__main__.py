from subprocess import Popen
from CordForge.launcher import Launcher

def run():
    print("Launcher running...")
    try:
        Launcher()
    except Exception as e:
        print(e)
    print("Launcher closing...")

if __name__ == "__main__":
    run()