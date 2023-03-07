# NBody

N bodies simulation utility written in Python and built with [CLIbrary](https://github.com/diantonioandrea/CLIbrary).

## Installation

### Prerequisites

There are some Python modules that need to be installed in order to compile and use **NBody**.

1. Compilation
	* pyinstaller: compilation of **NBody**.
2. Usage
	* [CLIbrary](https://github.com/diantonioandrea/CLIbrary): interface, inputs and outputs.
	* bcrypt: profile password-protection.
	* requests: update system.
	* matplotlib: plotting.
	* numpy: calculations.

As a one-liner:

	python3 -m pip install pyinstaller CLIbrary bcrypt requests matplotlib numpy

### Compiling and installing from source

**NBody** can be compiled by:

	make PLATFORM

where PLATFORM must be replaced by:

* windows
* linux
* darwin (macOS)

based on the platform on which **NBody** will be compiled. This will also produce a release package under ./release/NBody-PLATFORM.zip.  
Note that the Makefile for the Windows version is written for [NMAKE](https://learn.microsoft.com/en-gb/cpp/build/reference/nmake-reference?view=msvc-170).  
**NBody** can be then installed by:

	./NBody install

or

	.\NBody.exe install

on Windows.
	
### Installing from release

After decompressing *NBody-PLATFORM.zip*, it can be installed by:

	./NBody install

or

	.\NBody.exe install

on Windows.

## Commands

**NBody** supports its own help through **CLIbrary**'s help system.  
By:

	help

you'll obtain the list of available commands.
