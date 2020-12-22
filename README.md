# Injectra<br><img src="https://img.shields.io/badge/Language-Python3-blue"><img src="https://img.shields.io/badge/Version-2.0-red"><img src="https://img.shields.io/badge/Licence-MIT-yellowgreen">
Injectra injects shellcode payloads into mac OSX applications.


![render1585080763770](https://user-images.githubusercontent.com/36562445/77473525-e7c46d80-6e15-11ea-8fe8-235df7a24bb0.gif)

_Preview version 1.0. | Current verion 2.0._


## How it works
MacOS applications are called from an included file which can be easily replaced with the payload of injectra.

This payload will then call your payload while the application is running.

**The application is not able to detect the injection because the injection is called before the actual application.**

_The injection method includes in injectra was fully developed by Taguar258._

## Installation
To use injectra you will need to install python3 and preferably git:

```apt/pacman/brew/... install git python3```

_You can download it using your package manager or just install it manually._

Run the following command to download injectra or download the zip file from the release page:

```git clone https://github.com/Taguar258/injectra ; cd injectra ; python3 injectra.py -h```

<a href="https://github.com/Taguar258/injectra/projects/1">Project status/ToDo</a>

## Include argument
To include files, you will need to make a folder and move all the files you would like to include into this new created folder.

The argument ```--include``` will accept the folder and include all files inside of it.

In your injection script you will be able to call those files from your current working directory.

## Example
As an example you can inject an application using the following arguments:

```python3 injectra.py -i example/include_some_files/shellcode.sh -in example/include_some_files/injection/ -o INJECTEDAPP.app -a [app_path]```
