# Made by Taguar258 | Licence: MIT #

import argparse
import os
import subprocess
import sys
from os import path

from .src.check import check_for_injection
from .src.inject import inject_app
from .src.remove_injection import remove_injection


class Main:

    def __init__(self):

        # Colors
        self.C_None = "\x1b[0;39m"
        self.C_Blink = "\x1b[5;39m"
        self.C_Bold = "\x1b[1;39m"
        self.C_Red = "\x1b[31m"
        self.C_Green = "\x1b[32m"
        self.C_Yellow = "\x1b[33m"
        self.C_Blue = "\x1b[34m"
        self.C_BRed = "\x1b[1;31m"
        self.C_BGreen = "\x1b[1;32m"
        self.C_BYellow = "\x1b[1;33m"
        self.C_BBlue = "\x1b[1;34m"
        # self.C_Cyan = "\x1b[36m"
        # self.C_Magenta = "\x1b[35m"
        # self.C_BCyan = "\x1b[1;36m"
        # self.C_BMagenta = "\x1b[1;35m"

        self.mode = None
        self.include_files = False

    def parse_args(self):

        if '-r' in sys.argv or '--reset' in sys.argv:
            self.parser = argparse.ArgumentParser()
            self.parser.add_argument('-r', '--reset', required=False, help='Remove the injection from an infected application', action='store_true')
            self.parser.add_argument('-a', '--app', type=str, nargs=1, required=True, help='Target OSX application')
            self.mode = "Reset"

        elif '-c' in sys.argv or '--check' in sys.argv:
            self.parser = argparse.ArgumentParser()
            self.parser.add_argument('-c', '--check', required=False, help='Check if application was injected by injectra', action='store_true')
            self.parser.add_argument('-a', '--app', type=str, nargs=1, required=True, help='Target OSX application')
            self.mode = "Check"

        else:
            self.parser = argparse.ArgumentParser()
            self.parser.add_argument('-c', '--check', required=False, help='Check if application was injected by injectra', action='store_true')
            self.parser.add_argument('-r', '--reset', required=False, help='Remove the injection of an application', action='store_true')
            self.parser.add_argument('-a', '--app', type=str, nargs=1, required=True, help='Target OSX application')
            self.parser.add_argument('-i', '--inject', type=str, nargs=1, required=True, help='Bash/Shell script to inject')
            self.parser.add_argument('-o', '--output', type=str, nargs=1, required=True, help='Output for the infected application')
            self.parser.add_argument('-in', '--include', type=str, nargs=1, required=False, help='Add files of a given folder to the application')
            self.mode = "Inject"

        self.args = self.parser.parse_args()

    def banner(self):

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

        bannertxt = bannertxt.replace("@", self.C_BRed + "@")
        bannertxt = bannertxt.replace(":", self.C_BGreen + ":")
        bannertxt = bannertxt.replace("!", self.C_BYellow + "!")
        bannertxt = bannertxt.replace(".", self.C_BYellow + ".")
        bannertxt = bannertxt.replace(" ", self.C_None + " ")
        bannertxt = bannertxt.replace("-", self.C_Bold + "-")

        print(bannertxt)

    def get_abs_path(self):

        try:
            self.args.app[0] = path.abspath(self.args.app[0])
        except Exception:
            print(self.C_BRed + "[!] Cannot get the full path of the given application." + self.C_None)
            quit()

        if self.mode == "Inject":

            try:
                self.args.inject[0] = path.abspath(self.args.inject[0])
                self.args.output[0] = path.abspath(self.args.output[0])

                try:

                    if self.args.include[0] != "":

                        self.args.include[0] = path.abspath(self.args.include[0])

                        if self.args.include[0][-1:] == "/":

                            self.args.include[0] = self.args.include[0][-1:]

                        self.include_files = True

                except Exception:
                    pass

            except Exception:
                print(self.C_BRed + "[!] Cannot get the full path of the given files." + self.C_None)
                quit()

    def main_logic(self):

        if self.mode == "Reset":
            remove_injection(self.args)

        elif self.mode == "Check":
            check_for_injection(self.args)

        elif self.mode == "Inject":
            inject_app(self.args, self.include_files)

    def run(self):

        self.banner()
        self.parse_args()
        self.get_abs_path()
        self.main_logic()


def exec_main():

    main = Main()
    main.run()


if __name__ == '__main__':
    exec_main()
