from utils.dataStructures import Queue
import os

# Comprobar la extension del archivo
def checkFileExtension(file, extension = "atlc") -> bool:
    fileSliced = file.split(".")
    return True if (fileSliced[-1] == extension) else False

# Convertir el archivo de texto a un Array de instrucciones
def addInstructionsQueue(fileArgument) -> Queue: 
    instructionsQueue = Queue()
    with open(fileArgument, "r", encoding="utf-8") as file:
        for instruction in file:
            clean_instruction = instruction.strip().replace(";", "")
            if clean_instruction:  # 
                instructionsQueue.push(clean_instruction)

    return instructionsQueue

# Limpiar pantalla
def clear():
    # Para Windows
    if os.name == "nt":
        os.system("cls")
    # Para Linux/Mac
    else:
        os.system("clear")
