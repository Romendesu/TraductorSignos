import sys
from utils.auxiliarFunctions import *

def main() -> None:
    # Inicio del flujo normal del programa
    print(f'{"="*50}\n\nBienvenido al Compilador de Te-La-Choco (BETA)\n\n{"="*50}')

    # Comprobamos si el archivo ha sido proporcionado por el usuario
    if (len(sys.argv) < 2):
        raise Exception("[ERROR] No se ha proporcionado un archivo para compilar")
    
    # Comprobamos que el archivo proporcionado por el usuario es correcto
    fileArgument = sys.argv[1]
    if not (checkFileExtension(fileArgument)):
        raise Exception("[ERROR] El archivo proporcionado no esta escrito en Te-La-Choco.")
    
    # Conversion del texto plano
    instructions = arrayConversor(fileArgument)
    
    # Mostramos el array de tokens por pantalla
    print(instructions)
    

if __name__ == "__main__":
    main()