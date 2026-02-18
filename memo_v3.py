#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess

# Path to the engine
ENGINE_PATH = "/home/nerv0/.openclaw/workspace/memory/octagram/engine/main.py"

def main():
    parser = argparse.ArgumentParser(description="Sacred Essence v3.1 Bridge (memo_v3)")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", required=True)
    parser.add_argument("--abstract", default="")

    args = parser.parse_args()

    cmd = [
        "python3", ENGINE_PATH, "encode",
        "--topic", args.topic,
        "--title", args.title,
        "--content", args.content,
        "--abstract", args.abstract
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing engine: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
