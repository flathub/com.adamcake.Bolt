#!/usr/bin/env python

import os
import sys
import subprocess

def parse_gitmodules(root, relroot = None, out = None):
    if not out:
        out = []
    
    try:
        f = open(os.path.join(root, gitmodules_filename), "r")
    except FileNotFoundError:
        return out

    module = None
    while True:
        l = f.readline()
        if len(l) == 0:
            break
        line = l.strip()
        if line.startswith("[submodule "):
            module = {}
        elif line.startswith("path = "):
            dest = line[7:]
            nextroot = os.path.join(root, dest)
            result = subprocess.run(["git", "-C", nextroot, "rev-parse", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                if relroot:
                    module["dest"] = os.path.join(relroot, dest)
                else:
                    module["dest"] = dest
                module["commit"] = result.stdout.decode("utf-8").strip()
                out.append(module)
                parse_gitmodules(nextroot, dest, out)
        elif line.startswith("url = "):
            module["url"] = line[6:]

    f.close()
    return out

argc = len(sys.argv)
gitmodules_filename = ".gitmodules"

if __name__ == "__main__" and argc > 0:
    if argc != 2:
        print("Usage: '{} <path>', where path is the root of your chromium build directory containing .gitmodules".format(sys.argv[0]))
        exit(1)

    root = sys.argv[1]
    modules = parse_gitmodules(root)
    
    f = open("chromium-submodules.yaml", "w")
    for module in modules:
        f.writelines([
            "- type: git\n",
            "  url: {}\n".format(module["url"]),
            "  commit: {}\n".format(module["commit"]),
            "  dest: {}\n".format(module["dest"]),
            "  disable-submodules: true\n"
        ])

    f.close()
