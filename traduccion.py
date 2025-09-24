def codificador(mensaje) -> str:
    # Separamos el mensaje por espacios
    mensajeSpliteado = mensaje.split(" ")
    mensajeCodificado = ""
    diccionario = {
        'A': '🤚',
        'B': '🤚🤚',
        'C': '🤚🤚🤚',
        'D': '🤚✋',
        'E': '✋',
        'F': '✋🤚',
        'G': '✋🤚🤚',
        'H': '✋🤚🤚🤚',
        'I': '🤚👊',
        'J': '👊',
        'K': '👊🤚',
        'L': '👊🤚🤚',
        'M': '👊🤚🤚🤚',
        'N': '👊🤚✋',
        'O': '👊✋🤚',
        'P': '👊✋🤚🤚',
        'Q': '👊✋🤚🤚🤚',
        'R': '🤚👊👊',
        'S': '👊👊',
        'T': '👊👊🤚',
        'U': '👊👊🤚🤚',
        'V': '👊👊🤚🤚🤚',
        'W': '👊👊🤚✋',
        'X': '👊👊✋',
        'Y': '👊👊✋🤚',
        'Z': '👊👊✋🤚🤚',
        ',': ',',
        '.':'·',
        '1': '(🤚)i',
        '2': '(🤚🤚)i',
        '3': '(🤚🤚🤚)i',
        '4': '(🤚✋)i',
        '5': '(✋)i',
        '6': '(✋🤚)i',
        '7': '(✋🤚🤚)i',
        '8': '(✋🤚🤚🤚)i',
        '9': '(🤚👊)i',
        '0': '(👊)i'
    }
    for texto in mensajeSpliteado:
        cadenaCodificada = ""
        for letra in range(len(texto)):
            caracter = texto[letra].upper()
            cadenaCodificada += diccionario[caracter]
            if ((letra + 1) < len(texto)):
                cadenaCodificada += " "
        mensajeCodificado += cadenaCodificada 
        if texto != mensajeSpliteado[-1]:
           mensajeCodificado += "  "

    return mensajeCodificado


def decodificador(mensaje) -> str:
    diccionario_invertido = {
        '🤚': 'A',
        '🤚🤚': 'B',
        '🤚🤚🤚': 'C',
        '🤚✋': 'D',
        '✋': 'E',
        '✋🤚': 'F',
        '✋🤚🤚': 'G',
        '✋🤚🤚🤚': 'H',
        '🤚👊': 'I',
        '👊': 'J',
        '👊🤚': 'K',
        '👊🤚🤚': 'L',
        '👊🤚🤚🤚': 'M',
        '👊🤚✋': 'N',
        '👊✋🤚': 'O',
        '👊✋🤚🤚': 'P',
        '👊✋🤚🤚🤚': 'Q',
        '🤚👊👊': 'R',
        '👊👊': 'S',
        '👊👊🤚': 'T',
        '👊👊🤚🤚': 'U',
        '👊👊🤚🤚🤚': 'V',
        '👊👊🤚✋': 'W',
        '👊👊✋': 'X',
        '👊👊✋🤚': 'Y',
        '👊👊✋🤚🤚': 'Z',
        ',': ',',
        '·': '.',
        '(🤚)i':'1',
        '(🤚🤚)i':'2',
        '(🤚🤚🤚)i':'3',
        '(🤚✋)i':'4',
        '(✋)i':'5',
        '(✋🤚)i':'6',
        '(✋🤚🤚)i':'7',
        '(✋🤚🤚🤚)i':'8',
        '(🤚👊)i':'9',
        '(👊)i':'0'
    }
    
    palabras = mensaje.split("  ")  # separar palabras
    mensajeDecodificado = []
    
    for palabra in palabras:
        letras_codificadas = palabra.split(" ")  # separar letras
        palabraDecodificada = ""
        for simbolo in letras_codificadas:
            if simbolo:  # ignorar vacíos
                letra = diccionario_invertido.get(simbolo)
                if letra:  # ignorar símbolos desconocidos
                    palabraDecodificada += letra
        mensajeDecodificado.append(palabraDecodificada)
    
    return " ".join(mensajeDecodificado).lower()


def main():
    opcion = True
    while opcion:
        mensaje = input("Introduce un mensaje (No incluir numeros, funcion no implementada):\n")
        try:
            print("Mensaje codificado:", codificador(mensaje))
            print("Mensaje decodificado:", decodificador(codificador(mensaje)))
            continuar = input("Desea continuar: S/N: ")
            while True:
                if continuar.lower() == "s": 
                    break
                elif continuar.lower() == "n": 
                    opcion = False
                    break
                else:  
                    continuar = input("Opcion ingresada no valida, introduce una opcion valida: S/N: ")
        except Exception as e:
            print(f"No se ha podido codificar el mensaje: {mensaje}. Error: {e}")

    return None


if __name__ == "__main__":
    main()

    