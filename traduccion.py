def codificador(mensaje) -> str:
    # Separamos el mensaje por espacios
    mensajeSpliteado = mensaje.split(" ")
    mensajeCodificado = ""
    diccionario = {
    'A': '.',
    'B': '..',
    'C': '…',
    'D': '._',
    'E': '_',
    'F': '_.',
    'G': '_..',
    'H': '_…',
    'I': '.^',
    'J': '^',
    'K': '^.',
    'L': '^..',
    'M': '^…',
    'N': '.v',
    'O': 'v',
    'P': 'v.',
    'Q': 'v..',
    'R': 'v…',
    'S': '.^^',
    'T': '^^',
    'U': '^^.',
    'V': '^^..',
    'W': '^^…',
    'X': '.^v',
    'Y': '^v',
    'Z': '^v.',
    ',': ','
    }
    for texto in mensajeSpliteado:
        cadenaCodificada = ""
        # Analisis de las cadenas
        for letra in range(len(texto)):
            caracter = texto[letra].upper()
            cadenaCodificada += diccionario[caracter]
            if ((letra + 1) < len(texto)):
                cadenaCodificada += "I"
        mensajeCodificado += cadenaCodificada 
        # Si el caracter NO se encuentra en la ultima posicion, agregar espacio
        if texto != mensajeSpliteado[-1]:
           mensajeCodificado += "II"

    return mensajeCodificado

def decodificador(mensaje) -> str:
    mensajeSpliteado = mensaje.split("I")
    diccionario = {
    '.': 'A',
    '..': 'B',
    '…': 'C',
    '._': 'D',
    '_': 'E',
    '_.': 'F',
    '_..': 'G',
    '_…': 'H',
    '.^': 'I',
    '^': 'J',
    '^.': 'K',
    '^..': 'L',
    '^…': 'M',
    '.v': 'N',
    'v': 'O',
    'v.': 'P',
    'v..': 'Q',
    'v…': 'R',
    '.^^': 'S',
    '^^': 'T',
    '^^.': 'U',
    '^^..': 'V',
    '^^…': 'W',
    '.^v': 'X',
    '^v': 'Y',
    '^v.': 'Z',
    '': " ",
    ',':','
    }
    mensajeDecodificado = ""
    for indiceSimbolo in range(len(mensajeSpliteado)):
        letra = mensajeSpliteado[indiceSimbolo]
        traducida = diccionario[letra]
        mensajeDecodificado += traducida
    return mensajeDecodificado.lower()

def main():
    # Flujo normal del programa
    opcion = True
    while opcion:
        mensaje = input("Introduce un mensaje:\n")
        try:
            print("Mensaje codificado", codificador(mensaje))
            print("Mensaje decodificado", decodificador(codificador(mensaje)))
            continuar = input("Desea continuar: S/N: ")
            while True:
                if continuar.lower() == "s": 
                    break
                elif continuar.lower() == "n": 
                    opcion = False
                    break
                else:  
                    continuar = input("Opcion ingresada no valida, introduce una opcion valida: S/N: ")
        except Exception:
            print(f"No se ha podido codificar el mensaje:{mensaje}.")

    return None

if __name__ == "__main__":
    main()
    