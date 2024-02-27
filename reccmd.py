#!/usr/bin/env python3
import sys
import os
import json
import subprocess

FILE_NAME = ".reccmd"


def record():
    argv = sys.argv[1:]
    if len(argv) == 0:
        print("error: no command", file=sys.stderr)
        sys.exit(255)

    result = subprocess.run(argv, capture_output=True, text=True)
    with open(FILE_NAME, "a") as f:
        json.dump(
            {
                "argv": argv,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit": result.returncode,
            },
            f,
        )
        f.write("\n")


def play():
    try:
        with open(FILE_NAME, "r") as f:
            for cmd_str in f.readlines():
                cmd = json.loads(cmd_str)
                if cmd["argv"] == sys.argv:
                    break
            else:
                print("error: no recorded output for command", file=sys.stderr)
                sys.exit(255)
    except FileNotFoundError as e:
        print("error: no recorded commands in directory", file=sys.stderr)
        sys.exit(255)

    sys.stdout.write(cmd["stdout"])
    sys.stderr.write(cmd["stderr"])
    sys.exit(cmd["exit"])


def main():
    # Python always adds a path to argv[0]
    sys.argv[0] = os.path.basename(sys.argv[0])
    if sys.argv[0] in ("reccmd", "reccmd.py"):
        record()
    else:
        play()


if __name__ == "__main__":
    main()
