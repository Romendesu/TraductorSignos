#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int checkExtension(const char *filename, const char *ext) {
    // Busca la última aparición del carácter '.'
    const char *dot = strrchr(filename, '.');
    
    // Si no hay punto, o el punto es el primer carácter, no tiene una extensión válida.
    if (!dot || dot == filename) {
        return 0;
    }
    
    // Compara la cadena después del punto con la extensión esperada.
    return strcmp(dot + 1, ext) == 0;
}

int main(int argc, char*argv[]) {
    // 1. Manejo de errores de argumentos
    if (argc < 2) {
        printf("[ERROR]: Didn't receive any argument. Please provide a file name.\n");
        return 1;
    }
    
    // 2. Manejo de errores de extensión de archivo
    if (!checkExtension(argv[1], "tlc")) {
        // Nota: La función checkExtension espera "tlc" sin el punto
        printf("[ERROR]: File must be a .tlc file. Given file: %s\n", argv[1]);
        return 1;
    }
    
    // 3. Apertura del archivo
    FILE *expectedFile = fopen(argv[1], "r");

    // 4. Error de ejecución al abrir el archivo
    if (expectedFile == NULL) {
        printf("[ERROR]: An error has occurred while opening the file '%s'. Please ensure the file exists and is accessible.\n", argv[1]);
        return 1;
    }

    // 5. Procesamiento línea por línea
    char line[256];
    printf("--- Starting Tokenization ---\n");
    
    // Lee una línea del archivo
    while (fgets(line, sizeof(line), expectedFile)) {
        // Eliminamos el salto de linea ('\n') al final, si existe
        line[strcspn(line,"\n")] = 0;
        
        printf("Reading line: \"%s\"\n", line); // Muestra la línea original
        
        // Iteraremos con un puntero cada token, usando el punto y coma como delimitador
        char *token = strtok(line, ";");
        
        // Bucle para procesar cada token en la línea
        while (token != NULL) {
            // CORRECCIÓN CRUCIAL: Imprimir el 'token' actual, no toda la 'line'
            printf("  -> Token: %s\n", token); 
            
            // Llama a strtok con NULL para continuar la tokenización en la misma cadena
            token = strtok(NULL, ";");
        }
        printf("--------------------------------------\n");
    }
    
    // 6. Cierre del archivo
    fclose(expectedFile);
    printf("--- File closed successfully. ---\n");
    
    return 0;
}