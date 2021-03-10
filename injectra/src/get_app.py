from os import chdir


def get_app_name(args):

    C_None = "\x1b[0;39m"
    C_BRed = "\x1b[1;31m"

    print("[i] Determining application name.")

    if args.app[0][-1:] == "/":
        output = args.app[0]
        # app = args.app[0][: len(args.app[0]) - 1]

    else:
        output = args.app[0]
        # app = args.app[0]

    try:

        chdir(output + "/Contents/")

    except Exception:

        print(C_BRed + "[!] Cannot access the application." + C_None)
        quit()

    try:

        info = open("Info.plist", "r").read()
        info = info.split("<key>CFBundleExecutable</key>")[1]
        info = info.split("</string>")[0]
        info = info.split("<string>")[1]
        appname = info

    except Exception:

        print(C_BRed + "[!] Cannot determin application name." + C_None)
        appname = input("[?] Enter original application name: ")

    print(f"[+] The application name was sucessfully analyzed: {appname}")

    return appname
