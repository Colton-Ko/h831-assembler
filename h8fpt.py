#!/usr/bin/python3
import csv, re, os
from argparse import ArgumentParser

NOTHING                 = ""
PROM_LINES              = 32
PROM_PINS               = 68
PIN_O                   = "N"   #       Inverse of repeater direction on PROM address line
LINE_O                  = "E"   #       Direction towards next line of code from current line, E for east, W for west
PIN_O_LUT               = {"N": -1, "S": 1}
LINE_O_LUT              = {"W": -1, "E": 1}
TORCH_DIRECTION         = "west"
GAP_SIZE                = 2
LINE_DELIMINATOR        = 238

def convertToMCFunction(content):

        z0 = PIN_O_LUT[PIN_O]
        dx = LINE_O_LUT[LINE_O] * PROM_LINES * GAP_SIZE
        dz = PIN_O_LUT[PIN_O] * PROM_PINS * GAP_SIZE

        statements = [f"fill ~ ~ ~{z0} ~{dx} ~ ~{dz} air replace minecraft:redstone_wall_torch"]
        statements.append(f"fill ~ ~-1 ~{z0} ~ ~-1 ~{dz} void_air replace minecraft:redstone_wire")

        # Convert binContent to List of pins on each line
        torchArray = list()
        pinPerLine = list()

        for pin in content:
                if pin != LINE_DELIMINATOR:
                        pinPerLine.append(pin)
                else:
                        torchArray.append(tuple(pinPerLine))
                        pinPerLine.clear()
                        
        for ln, line in enumerate(torchArray):
                for pin in line:
                        z = PIN_O_LUT[PIN_O] + PIN_O_LUT[PIN_O] * GAP_SIZE * pin
                        x = ln * GAP_SIZE
                        statements.append(f'setblock ~{x} ~ ~{z} minecraft:redstone_wall_torch[facing={TORCH_DIRECTION}]')

        statements.append(f"fill ~ ~-1 ~{z0} ~ ~-1 ~{dz} redstone_wire replace minecraft:void_air")

        try:
                file = open("romflash.mcfunction", 'w+')
                file.writelines("\n".join(statements)+'\n')
                file.close()

        except IOError:
                print("Unable to write romflash.mcfunction due to IO error.")
        except Exception:
                print("Unable to write romflash.mcfunction due to unknown error.")

        print('\n'+f'{len(statements)} lines written to romflash.mcfunction.')

        print("\nThe romflash script is created. Check out romflash.mcfunction")
        print("To use it, copy it to your world/data/functions folder and run /function romflash\n")

        return

def loadBinFile(binfile):
        with open(binfile, "rb") as file:
                byte = file.read()

        return list(byte)

def showHelp():
        HELP_MSG_1 = '-'*80 + "\n" + "| " + f'{"H831 Minecraft CPU Flash Programming Tool": ^76}' + " |\n| " + " "*76 + " |"
        HELP_MSG_2 = f'{"| Author: HyperXraft": <78}' + " |"
        HELP_MSG_3 = f'{"| Date  : 2020-09-05 (3 years after disaster on 2017-09-05)": <78}' + " |"
        HELP_MSG_4 = '-'*80

        print(HELP_MSG_1)
        print(HELP_MSG_2)
        print(HELP_MSG_3)
        print(HELP_MSG_4)

        parser = ArgumentParser()
        parser.add_argument(help="Compiled binary", dest="BINFILE", default="", type=str)

        args = parser.parse_args()
        
        inputFile = args.BINFILE

        if inputFile == NOTHING:
                parser.print_help()
                quit()

        print(f'{"Compield binary:": <30}{inputFile}')

        content = loadBinFile(inputFile)
        convertToMCFunction(content)

        
showHelp()