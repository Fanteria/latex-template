#!/usr/bin/env python3

from LatexInputWorker import LatexInputWorker
from SettingsWorker import SettingsWorker
import sys
import os
import getopt

def proccess_args(argv, settingsWorker: SettingsWorker, latexInputWorker: SettingsWorker):
    try:
        opts, args = getopt.getopt(argv, "vschf", ["verbose", "silcence", "code", "help", "force"])
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
        return

    while len(args) > 0:
        if args[0] == "build":
            if len(args) == 1: # It's last argument.
                print("full build")
                latexInputWorker.all_file_list()
            else:
                files_list = latexInputWorker.proccess_files(args[1])
                if files_list == None: # Next argument is not list of files.
                    print("FULL build")
                else: # Next argument is list of files.
                    print("build: ", files_list)
                    del args[0]
        elif args[0] == "init":
            print("init")
        elif args[0] == "clean":
            print("clean")
        elif args[0] == "clear":
            print("clear")
        elif args[0] == "help":
            print("help")
        elif args[0] == "getref":
            print("get references to project file")
        elif args[0] == "pack":
            print("pack")
        elif args[0] == "encrypt":
            print("encrypt")
        else: 
            user_commands = settingsWorker.get_list_of_commands()
            if args[0] in user_commands:
                print(user_commands[args[0]])
            else:
                print("unknown command:", args[0])

        del args[0]


if __name__ == "__main__":
    settingsWorker = SettingsWorker(os.path.split(os.path.realpath(__file__))[0], os.getcwd())
    latexInputWorker = LatexInputWorker(settingsWorker)
    proccess_args(sys.argv[1:], settingsWorker, latexInputWorker)
    