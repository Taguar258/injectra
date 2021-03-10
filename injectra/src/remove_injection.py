from os import getcwd, path
from subprocess import call

from .get_app import get_app_name
from .logic import check_app_path, check_injection

C_None = "\x1b[0;39m"
C_BRed = "\x1b[1;31m"


def remove_injection(args):

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
