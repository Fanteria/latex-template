#!/usr/bin/env python3
import sys

from TemplateMake import TemplateMake

if __name__ == "__main__":

    run = TemplateMake()

    if len(sys.argv) == 1:
        run.build()
        exit()

    if len(sys.argv) == 2 and not run.is_runtime(sys.argv[1]):
        run.build(sys.argv[1])
        exit()

    if len(sys.argv) == 2 and sys.argv[1] == "run":
        print("Command: ", end="")
        try:
            stdin=input()
        except:
            exit()

        while stdin != "exit":
            run.runtime(stdin)
            print("Next command: ", end="")
            stdin=input()

        exit()

    for i in range(1, len(sys.argv)-1):
        if not run.is_runtime(sys.argv[i]):
            continue
        run.runtime(sys.argv[i], sys.argv[i+1])

    if run.is_runtime(sys.argv[len(sys.argv)-1]):
        run.runtime(sys.argv[len(sys.argv)-1])
