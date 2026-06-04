# run.py

import subprocess
import sys
import os

def main():
    script = "main.py"  # change this if your file has a different name
    if not os.path.exists(script):
        print(f"Error: {script} not found!")
        return

    try:
        subprocess.run([sys.executable, script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e}")

if __name__ == "__main__":
    main()
