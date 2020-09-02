# h831-assembler
Assembler for H831 CPU in Minecraft.

#### Overview

This repository hosts the assembler for H831 CPU in minecraft, which converts the assembly code to native binary file for H831. The compiled binary is expected to be stored in the program ROM (PROM) of the H831 CPU.

Note that the program ROM (PROM) has only 2716b. Make sure the size your compiled program is less than that.

#### Usage

```bash
usage: h8as.py [-h] [-o OUT_FILENAME] IN_FILENAME MAPFILE

positional arguments:
  IN_FILENAME      File for assembly program
  MAPFILE          Microcode descriptor file

optional arguments:
  -h, --help       show this help message and exit
  -o OUT_FILENAME  File for assembler output
```

##### Required arguments

1. `IN_FILENAME`: The program code for H831 in assembly.
2. `MAPFILE`: The Instruction Decode Descriptor file (Since there is no instruction decoder in that CPU)
	- If you download this repository, the `MAPFILE` would be `config/ucode.map`. It is a text file.

##### Optional arguments

- `OUT_FILENAME`: The filename for the compiled binary file.
	- The program will output the binary line-by-line regardless of having this parameter specified.

#### Examples

The following examples assumed that you have changed your working directory to the downloaded repository folder.

```bash
python3 h8as.py demo/memtest.asm config/ucode.map -o memtest.bin
```

```bash
python3 h8as.py demo/15x17.asm config/ucode.map
```

#### Running on H831

Available soon.





