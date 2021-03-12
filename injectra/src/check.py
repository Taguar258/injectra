from glob import glob
from os import chdir, makedirs, path
from subprocess import call

from .get_app import get_app_name
from .logic import (check_app_path, check_injection, check_pkg_injection,
                    extracting_scripts)

C_None = "\x1b[0;39m"
C_BRed = "\x1b[1;31m"


def check_for_app_injection(args):

    # 1 | Check for valid folder
    check_app_path(args)

    # 2 | Get the application name
    get_app_name(args)

    # 3 | Check for injection
    check_injection(verbose_mode=True)

    quit()


def check_for_pkg_injection(args):

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

    # 4 | Fetching injectable packages
    print("[i] Fetching injectable packages.")
    print("")

    injectable_pkgs = list(glob("*.pkg"))

    if len(injectable_pkgs) == 0:

        if check_pkg_injection():

            print(C_BRed + "[i] An injection was found." + C_None)

        else:

            print("[i] The package was not injected.")

    else:

        status = []

        for pkg in injectable_pkgs:

            chdir(pkg)

            status.append(check_pkg_injection())

            chdir("../")

        if True in status:

            print(C_BRed + "[i] An injection was found." + C_None)

        else:

            print("[i] The package was not injected.")

    print("")

    # 10 | Cleaning up
    print("[i] Cleaning up.")

    chdir("../")

    try:

        call(f"rm -rf '.tmp_{output}'", shell=True)

    except Exception:

        print(C_BRed + "[!] Could not clean up." + C_None)
        quit()
