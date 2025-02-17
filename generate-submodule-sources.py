#!/usr/bin/env python

import os
import sys
import subprocess

def parse_gitmodules(root, root_commit, relroot = None, out = None):
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
            # nonzero exit code probably means the directory doesn't exist at all
            if result.returncode == 0:
                commit = result.stdout.decode("utf-8").strip()
                # if the directory exists, but rev-parse returned the same hash as it did on the level above,
                # that means the directory isn't a git repo in itself, so we should ignore it
                if commit != root_commit:
                    if relroot:
                        module["dest"] = os.path.join(relroot, dest)
                    else:
                        module["dest"] = dest
                    module["commit"] = commit
                    out.append(module)
                    parse_gitmodules(nextroot, commit, dest, out)
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
    result = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    modules = parse_gitmodules(root, result.stdout.decode("utf-8").strip())
    
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
