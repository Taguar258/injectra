from glob import glob
from os import chdir, getcwd, makedirs, path
from subprocess import call

from .get_app import get_app_name
from .logic import check_app_path, check_injection, check_pkg_injection

C_None = "\x1b[0;39m"
C_BRed = "\x1b[1;31m"


def remove_app_injection(args):

    # 1 | Check for valid folder
    check_app_path(args)

    # 2 | Get the application name
    appname = get_app_name(args)

    # 3 | Check for injection
    check_injection(verbose_mode=False)

    # 4
    print("[i] Changing the start order.")

    try:
        print("[i] Please enter yes twice.")

        call(f"rm -i '{appname}'", shell=True)
        call("rm -i 'payload'", shell=True)

        if path.isfile(path.abspath(getcwd()) + "/" + appname):
            print(C_BRed + "[!] Cannot continue without your permission." + C_None)

            raise Exception("Permission denied")

        call(f"mv 'injectra' '{appname}'", shell=True)

        print("[+] The operation was sucessful.")
        quit()

    except Exception:

        print(C_BRed + "[!] Cannot remove the injection." + C_None)
        quit()


def remove_pkg_injection(args):

    # 1 | Gathering filename

    output = args.pkg[0]

    if output[:-1] == "/":

        output = output.split("/")[-2]

    else:

        output = output.split("/")[-1]

    # 2 | Creating temporary directory
    print("[i] Creating temporary directory...")

    try:

        makedirs(f".tmp_{output}")

        # call(f"cp -r '{args.pkg[0]}' '{output}'", shell=True)

        chdir(f".tmp_{output}")
 
        print("[+] The package was sucessfully cloned.")

    except Exception:

        print(C_BRed + f"[!] Cannot write to output: .tmp_{output}" + C_None)
        quit()

    # 3 | Decompression of package
    print("[i] Decompressing the package...")

    try:

        call(f"xar -xf '{args.pkg[0]}'", shell=True)

    except Exception:

        print(C_BRed + "[!] Cannot decompress the package." + C_None)
        print("[i] Make sure xar is available.")
        quit()

    # 4 | Fetching injected packages
    print("[i] Fetching injectable packages.")

    injectable_pkgs = list(glob("*.pkg"))
    injected_pkgs = []

    if len(injectable_pkgs) == 0:

        if check_pkg_injection():

            injected_pkgs.append(".")

        chdir("../")

    else:

        for pkg in injectable_pkgs:

            chdir(pkg)

            if check_pkg_injection():

                injected_pkgs.append(pkg)

            chdir("../../")

    # 5 | Removing injection
    print("[i] Removing injections...")

    identify_string = '#!/bin/sh\nDIR=$(cd "$(dirname "$0")"; pwd) ; cd $DIR\n$DIR/payload &\n$DIR/injectra &'

    for pkg_path in injected_pkgs:

        chdir(pkg_path + "/Scripts/")

        print("[i] Identifing previous state.")

        scripts = list(glob("*"))

        if "preinstall" in scripts:

            with open("preinstall", "r") as file:

                if file.read() == identify_string:

                    injection_point = "preinstall"

        elif "postinstall" in scripts:

            with open("postinstall", "r") as file:

                if file.read() == identify_string:

                    injection_point = "postinstall"

        else:

            print(C_BRed + "[!] Fatal Error, while removing injection." + C_None)
            quit()

        print("[i] Removing an injection.")

        try:

            call(f"rm {injection_point}", shell=True)
            call(f"rm payload", shell=True)
            call(f"mv injectra {injection_point}", shell=True)

        except Exception:

            print(C_BRed + "[!] Could not remove injection." + C_None)
            quit()

        chdir("../../")

    # 6 | Repacking the package
    print("[i] Repacking the package...")

    try:

        print("Please answer with yes...")
        call(f"rm {args.pkg[0]}")

        call(f"pkgutil --flatten . {args.pkg[0]}", shell=True)

    except Exception:

        print(C_BRed + "[!] Could not repack the package." + C_None)
        print("[i] Make sure pkgutil is available.")
        quit()

    # 7 | Cleaning up
    print("[i] Cleaning up.")

    try:

        call(f"rm -rf '.tmp_{output}'", shell=True)

    except Exception:

        print(C_BRed + "[!] Could not clean up." + C_None)
        quit()

    print("[i] Removed the injections.")
