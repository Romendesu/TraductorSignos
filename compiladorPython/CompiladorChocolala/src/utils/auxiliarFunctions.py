
# Comprobar la extension del archivo
def checkFileExtension(file, extension = "tlc") -> bool:
    fileSliced = file.split(".")
    return True if (fileSliced[-1] == extension) else False

# Convertir el archivo de texto a un Array de instrucciones
def tokenConversor(fileArgument) -> list:
    with open(fileArgument, "r") as file:
        # En principio es una COLA
        instructions = []
        # Vaciamos los saltos de linea
        for token in file:
            instructions.append(token.strip())
        return instructions