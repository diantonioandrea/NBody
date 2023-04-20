# NBody

N bodies simulation utility written in Python and built with [CLIbrary](https://github.com/diantonioandrea/CLIbrary).[^1]

[^1]: **NBody** has been archived and should serve just as a fun project and a [CLIbrary](https://github.com/diantonioandrea/CLIbrary) example.

## Installation

### Prerequisites

There are some Python modules that need to be installed in order to compile and use **NBody**.

1. Compilation
	* pyinstaller: compilation of **NBody**.
2. Usage
	* [CLIbrary](https://github.com/diantonioandrea/CLIbrary): interface, inputs and outputs.
	* bcrypt: profile password-protection.
	* requests: Update notification.
	* matplotlib: plotting.
	* numpy: calculations.

As a one-liner:

	python3 -m pip install --upgrade pyinstaller CLIbrary bcrypt matplotlib numpy requests

### Compiling and installing from source

**NBody** can be compiled[^2] by:

	make PLATFORM

where PLATFORM must be replaced by:

* windows
* unix (Linux and macOS)

based on the platform on which **NBody** will be compiled.  
**NBody** can be then installed[^3] by:

	./NBody install

or

	.\NBody.exe install

on Windows.

[^2]: The Makefile for the Windows version is written for [NMAKE](https://learn.microsoft.com/en-gb/cpp/build/reference/nmake-reference?view=msvc-170).
[^3]: This is the only way to install **NBody**.

## Commands

**NBody** supports its own help through **CLIbrary**'s help system.  
By:

	help

you'll obtain the list of available commands.
