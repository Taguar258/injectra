from os import R_OK, access, chdir, getcwd, path

C_None = "\x1b[0;39m"
C_BRed = "\x1b[1;31m"


def check_app_path(args):
    print("[i] Checking application path.")

    if path.isdir(args.app[0]):
        print("[+] Found the application: %s" % args.app[0])
    else:
        print(C_BRed + "[!] Cannot find the application." + C_None)
        quit()


def check_injection(verbose_mode=False):
    try:
        chdir("MacOS/")
    except Exception:
        print(C_BRed + "[!] Cannot access applications main file." + C_None)
        quit()

    if verbose_mode:
        print("[i] Checking if application was injected by Injectra.\n")
    else:
        print("[i] Checking if application was injected by Injectra.")

    if path.isfile(path.abspath(getcwd()) + "/" + "injectra"):

        if verbose_mode:

            print(C_BRed + "[i] An injection was found." + C_None)
            quit()

        else:

            print("[i] An injection was found.")

    else:
        if verbose_mode:
            print("[!] The application was not injected by injectra.")
        else:
            print(C_BRed + "[!] The application was not injected by injectra." + C_None)
            quit()


def check_inputs(args):
    print("[i] Checking the script.")

    if path.isfile(args.inject[0]):
        print("[+] Found the script: %s" % args.inject[0])
    else:
        print(C_BRed + "[!] Cannot find the script." + C_None)
        quit()

    print("[i] Check if script is readable.")

    if access(args.inject[0], R_OK):
        print("[+] Script is readable.")
    else:
        print(C_BRed + "[!] Cannot read script." + C_None)
        quit()

    print("[i] Check if output path is writable.")
    try:
        output = args.output[0].split("/")
        output1 = "/".join(output[: len(output) - 1])
        output2 = "." + ("/".join(output[-1:]))

        if output1 != "":
            output2 = "/" + output2

        output = output1 + output2

    except Exception:
        print(C_BRed + ("[!] Cannot get output path: %s" % output) + C_None)
        quit()

    return output
