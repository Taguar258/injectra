# Injectra<br><img src="https://img.shields.io/badge/Language-Python3-blue"> <img src="https://img.shields.io/badge/Version-3.0-red"> <img src="https://img.shields.io/badge/Licence-MIT-yellowgreen">

Injectra injects shellcode payloads into MacOS applications and package installers.

Injectra makes so that applications and packages run user-given code on start.

<!--MEDIA-->


## Installation 

Due to the installation using setuptools the only requirement is python3 with pip installed.

Installation:

```bash
pip3 install git+https://github.com/Taguar258/injectra
```

Execution:

```bash
injectra -h
```

Uninstallation:

```bash
pip3 uninstall injectra
```

_Tested on MacOS._

## Instructions

Injectra has three working modes: Injection, Removal, and Detection. All those modes can be applied to packages as well as applications.

### Injection

A simple injection of an application would look like this:

```bash
injectra -a INPUT_APP.app -i PAYLOAD.sh -o OUTPUT.app
```

The `-a` argument inputs an application whereas this can be replaced with `-p` which stands for package:

```bash
injectra -a INPUT_PKG.pkg -i PAYLOAD.sh -o OUTPUT.pkg
```

The `-i` argument injects the given shell payload and `-o` defines an output location.

In case you would like to include files to the directory of the payload you can use the `-in` argument. The `-in` argument accepts a folder with all the files in it you would like to add. You can then call all the injected files from you current working directory of the payload.

### Detection

You can easily identify injections via injectra using:

```bash
injectra -c -a INPUT.app
```

Whereas `-c` stands for _check_. The application argument (`-a`) can be replaced with `-p` for packages as well.

### Removal

Injections can be removed by applying the `-r` argument (stands for _remove_):

```bash
injectra -r -p INPUT.pkg
```

You can also replace `-p` with `-a` for application.

This will remove the injection from the given input.

## Explanation

MacOS applications, as well as pkg installers, contain executables that are executed by a parent process. Injectra renames those executables so that a parent payload can be injected which calls your payload before starting the actual process.

There are some application which will not work yet though will work in feature updates. An example of such applications is the applications provided by MacOS itself. All other tested applications worked fine.

The injection of a package installer can escalate the payloads permissions due to the privilege escalation of the installer itself.

The injection method provided by Injectra was fully developed and discovered by Taguar258.
