# Made by Taguar258 | Licence: MIT #

import argparse
import os
import subprocess
import sys
from os import path

from src.check import check_for_injection
from src.inject import inject_app
from src.remove_injection import remove_injection

# Colors
C_None = "\x1b[0;39m"
C_Blink = "\x1b[5;39m"
C_Bold = "\x1b[1;39m"
C_Red = "\x1b[31m"
C_Green = "\x1b[32m"
C_Yellow = "\x1b[33m"
C_Blue = "\x1b[34m"
C_BRed = "\x1b[1;31m"
C_BGreen = "\x1b[1;32m"
C_BYellow = "\x1b[1;33m"
C_BBlue = "\x1b[1;34m"
# C_Cyan = "\x1b[36m"
# C_Magenta = "\x1b[35m"
# C_BCyan = "\x1b[1;36m"
# C_BMagenta = "\x1b[1;35m"

mode = None

if '-r' in sys.argv or '--reset' in sys.argv:
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--reset', required=False, help='Remove the injection from an infected application', action='store_true')
    parser.add_argument('-a', '--app', type=str, nargs=1, required=True, help='Target OSX application')
    mode = "Reset"
elif '-c' in sys.argv or '--check' in sys.argv:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--check', required=False, help='Check if application was injected by injectra', action='store_true')
    parser.add_argument('-a', '--app', type=str, nargs=1, required=True, help='Target OSX application')
    mode = "Check"
else:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--check', required=False, help='Check if application was injected by injectra', action='store_true')
    parser.add_argument('-r', '--reset', required=False, help='Remove the injection of an application', action='store_true')
    parser.add_argument('-a', '--app', type=str, nargs=1, required=True, help='Target OSX application')
    parser.add_argument('-i', '--inject', type=str, nargs=1, required=True, help='Bash/Shell script to inject')
    parser.add_argument('-o', '--output', type=str, nargs=1, required=True, help='Output for the infected application')
    parser.add_argument('-in', '--include', type=str, nargs=1, required=False, help='Add files of a given folder to the application')
    mode = "Inject"


def banner():
    bannertxt = """
----------------------------------------------------------------
@@@ @@@  @@@     @@@ @@@@@@@@  @@@@@@@ @@@@@@@ @@@@@@@   @@@@@@ 
@@! @@!@!@@@     @@! @@!      !@@        @!!   @@!  @@@ @@!  @@@
!!@ @!@@!!@!     !!@ @!!!:!   !@!        @!!   @!@!!@!  @!@!@!@!
!!: !!:  !!! .  .!!  !!:      :!!        !!:   !!: :!!  !!:  !!!
:   ::    :  ::.::   : :: ::   :: :: :    :     :   : :  :   : :
----------------------------------------------------------------
               Made by Taguar258 | MIT 2020                     
"""
    bannertxt = bannertxt.replace("@", C_BRed + "@")
    bannertxt = bannertxt.replace(":", C_BGreen + ":")
    bannertxt = bannertxt.replace("!", C_BYellow + "!")
    bannertxt = bannertxt.replace(".", C_BYellow + ".")
    bannertxt = bannertxt.replace(" ", C_None + " ")
    bannertxt = bannertxt.replace("-", C_Bold + "-")
    print(bannertxt)


banner()
args = parser.parse_args()


# Grabing absolute path of
try:
    args.app[0] = path.abspath(args.app[0])
except Exception:
    print(C_BRed + "[!] Cannot get the full path of the given application." + C_None)
    quit()


if mode == "Reset":
    remove_injection(args)

elif mode == "Check":
    check_for_injection(args)

elif mode == "Inject":
    include_files = False

    try:
        args.inject[0] = path.abspath(args.inject[0])
        args.output[0] = path.abspath(args.output[0])

        try:

            if args.include[0] != "":

                args.include[0] = path.abspath(args.include[0])

                if args.include[0][-1:] == "/":

                    args.include[0] = args.include[0][-1:]

                include_files = True

        except Exception:
            pass

    except Exception:
        print(C_BRed + "[!] Cannot get the full path of the given files." + C_None)
        quit()

    inject_app(args, include_files)
