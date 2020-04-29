# Injectra
Injectra injects bash code into mac OSX applications.

## Installation
Install git and python3:

```apt/pacman/brew/... install git python3```

Run the following command to download injectra:

```git clone https://github.com/Taguar258/injectra ; cd injectra ; python3 injectra.py -h```

![render1585080763770](https://user-images.githubusercontent.com/36562445/77473525-e7c46d80-6e15-11ea-8fe8-235df7a24bb0.gif)

Preview version 1.0. | Current verion 1.3.

<a href="https://github.com/Taguar258/injectra/projects/1">Project status/ToDo</a>

## Include argument
To include files, you will need to make a folder and move all the files you would like to include into this new created folder.

The argument ```--include```will accept the folder and include all files inside into the application.

In your injection script you will be able to call those files from your current directory.

## Example
Try the following:

```python3 injectra.py -i example/include_some_files/shellcode.sh -in example/include_some_files/noodle/ -o INJECTEDAPP.app -a [app_path]```
