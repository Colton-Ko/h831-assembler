#!/usr/bin/python3
import csv,re
from argparse import ArgumentParser

COMMENT_REGEX = r';.+|;'
NOTHING = ""
LABEL_REGEX = r'\.[A-za-z]+:'
TRAILING_REGEX = r'^\s+'
INSTRUCTION_REGEX = r'[A-z]+\s'
INSTR_COL_LAYOUT = "#instr"
PIN_COL_LAYOUT = "pin"
ARG0_COL_LAYOUT = "arg0"
ARG1_COL_LAYOUT = "arg1"
ARG2_COL_LAYOUT = "arg2"
ARGCOUNT_COL_LAYOUT = "argCount"
PIN = 0
DEST = 1
SRC0 = 2
SRC1 = 3
ARGS = 4
BIN_DELIMINATOR = 238                   # Use EE as deliminiator

def loadMapFile(mapFile):
        with open(mapFile, newline='') as csvfile:
                layout = csv.DictReader(csvfile)
                output = dict()
                for row in layout:
                        output[row[INSTR_COL_LAYOUT]] =  (  
                                        row[PIN_COL_LAYOUT],
                                        row[ARG0_COL_LAYOUT],  
                                        row[ARG1_COL_LAYOUT], 
                                        row[ARG2_COL_LAYOUT], 
                                        row[ARGCOUNT_COL_LAYOUT]
                                )
        return output
        
def loadAssembly(input):
        assembly = open(input,"r")
        assembly = assembly.read().split("\n")
        assembly = [re.sub(COMMENT_REGEX, NOTHING, line) for line in assembly]
        assembly = [line for line in assembly if line]
        return assembly

def convertLabelsToPAddr(assembly):
        labels = dict()
        for ln, line in enumerate(assembly):
                if re.search(LABEL_REGEX, line):
                        label = str(re.search(LABEL_REGEX, line).group(0))
                        labels[label.strip(':')] = ln
        
        asmString = '\n'.join(assembly)

        for key in labels.keys():
                asmString = asmString.replace(f'{key}:', " "*(len(key)+1))

        del labels['.main']

        for label, ln in labels.items():
                asmString = asmString.replace(label, str(ln))

        assembly = asmString.split('\n')
                      
        return [re.sub(TRAILING_REGEX, NOTHING, line) for line in assembly]

def determineLiteralType(instr,layout, argID):
        typeDescriptor = layout[instr][argID]

        pinStart = int(re.findall(r'\d+', typeDescriptor)[0])
        pinEnd = int(re.findall(r'\d+', typeDescriptor)[1])

        bits = pinEnd - pinStart+1
        flipRequire = True if typeDescriptor.find("[^") == -1 else False
        return (pinStart, pinEnd, bits, flipRequire)

def parseArgs(instr, args, layout,ln):
        output = 0
        for i in range(int(layout[instr][ARGS])):
                typeParameters = determineLiteralType(instr, layout, i+1)
                try:
                        literal = int(re.search(r'\d+',args[i]).group(0))
                except IndexError:
                        print(f'{ln: >2}: At {instr + " " +", ".join(args)} -> Not enough arguments supplied. Probably missing source and dest address?')
                        quit()
                if literal > pow(2, typeParameters[2]):   #       If literal is oversized
                        print(f'{ln: >2}: At {instr + " " +", ".join(args)} -> The literal {literal} is too big. At most {typeParameters[2]} is accepted.')
                        quit()

                argBinary = str(bin(literal)).replace("0b", NOTHING)            # Replace 0b suffix
                argBinary = f"{argBinary:0>{typeParameters[2]}}"                # Add padding

                if typeParameters[3]:                                           # Flip if required
                        argBinary = argBinary[::-1]

                for offset, n in enumerate(argBinary):
                        output += int(n) * pow(2,(offset + typeParameters[0]))

        return output

def assembleArgs(instr, args, layout,ln):
        args = args.replace(" ","").split(',')
        return parseArgs(instr, args, layout,ln)

def assembleInstruction(assembly, layout, output='', showPins=False):

        if showPins:
                print(f'{" Pin configuration ":-^45}')
        else:
                print(" "*4+"0"*72)

        code = list()
        for ln, line in enumerate(assembly):
                instr = re.search(INSTRUCTION_REGEX, line).group(0).strip(' ')
                pins = tuple(map(int,layout[instr][PIN].split(',')))
                opcode = 0
                for n in pins:
                        opcode += pow(2,n)
                opcode += assembleArgs(instr, line.replace(instr + ' ',''),layout,ln)
                binCode = f'{str(bin(opcode)).replace("0b",NOTHING)[::-1]:0<68}'

                if showPins:
                        print(f"{ln: >2}: {', '.join(map(str, [m.start() for m in re.finditer('1', binCode)]))}") # Show pins
                else:
                        print(f'{ln: >2}: 0000{binCode} ({hex(int(binCode,2))})')
                
                code.append(bytearray([m.start() for m in re.finditer('1', binCode)] + [BIN_DELIMINATOR]))
        
        if output == '':
                quit()
        else:
                file = open(output, "wb")
                for line in code:
                        data = line
                        file.write(data)
                file.close()
        return

def assemble(input, output, mapFile, pin):
        layout = loadMapFile(mapFile)
        assembly = loadAssembly(input)
        assembly = convertLabelsToPAddr(assembly)
        [print(f'{ln: >2}: {line}') for ln, line in enumerate(assembly)]
        assembleInstruction(assembly, layout, output, showPins=pin)
        return

def showHelp():
        HELP_MSG_1 = '-'*60 + "\n" + "| " + f'{"H831 Minecraft CPU Assembler tool": ^56}' + " |\n| " + " "*56 + " |"
        HELP_MSG_2 = f'{"| Author: HyperXraft": <58}' + " |"
        HELP_MSG_3 = f'{"| Date  : 2020-09-02": <58}' + " |"
        HELP_MSG_4 = '-'*60 

        print(HELP_MSG_1)
        print(HELP_MSG_2)
        print(HELP_MSG_3)
        print(HELP_MSG_4)

        parser = ArgumentParser()
        parser.add_argument(help="File for assembly program", dest="IN_FILENAME", default="", type=str)
        parser.add_argument(help="Microcode descriptor file", dest="MAPFILE", default="", type=str)
        parser.add_argument("-p", "--pin", action="store_true", help="Show pin code instead of binary")
        parser.add_argument("-o", help="File for assembler output", dest="OUT_FILENAME", default="", type=str)

        args = parser.parse_args()
        
        inputFile = args.IN_FILENAME
        outputFile = args.OUT_FILENAME
        mapFile = args.MAPFILE
        showPins = args.pin 

        if inputFile == NOTHING or mapFile == NOTHING:
                parser.print_help()
                quit()

        print(f'{"Input:": <30}{inputFile}')
        print(f'{"Mapfile:": <30}{mapFile}')
        print(f'{"Output:": <30}{outputFile}')
        
        assemble(inputFile, outputFile, mapFile, showPins)
        
showHelp()