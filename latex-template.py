#!/usr/bin/env python3

import sys
import getopt

def proccess_args(argv):
    try:
        opts, args = getopt.getopt(argv, "vschf", ["verbose", "silcence", "code", "help", "force"])
        print(args)
    except:
        print("Invalid: print help")
        sys.exit(2)

    
    flag_code = False       # Generate only LaTeX code, not compile it.
    flag_silence = False    # Run program with silence output.
    flag_verbose = False    # Run program with verbose output.
    flag_force = True       # Force program to update every file.

    for opt, arg in opts:
        if opt in ("-c", "code"):
            flag_code = True
        elif opt in ("-s", "silence"):
            flag_silence = True
            flag_verbose = False
        elif opt in ("-v", "--verbose"):
            flag_verbose = True
            flag_silence = False
        elif opt in ("-f", "--force"):
            flag_force = True
        elif opt in ("-h", "--help"):
            print("Help")
            return

    if len(args) == 0:
        print("full build")
    elif args[0] == "build":
        print("build")
    elif args[0] == "init":
        print("init")
    elif args[0] == "clean":
        print("clean")
    elif args[0] == "clear":
        print("clear")
    elif args[0] == "help":
        print("help")


if __name__ == "__main__":
    proccess_args(sys.argv[1:])