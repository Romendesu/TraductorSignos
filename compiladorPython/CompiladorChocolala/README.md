# 🧠 Virtual Machine – Documentación del Proyecto

## 📘 Descripción General

Este proyecto implementa una **máquina virtual (VM)** personalizada capaz de **interpretar y ejecutar un conjunto de instrucciones** (similares a un lenguaje ensamblador o intermedio).  
El objetivo principal es simular operaciones básicas de **manipulación de registros, operaciones aritméticas y lógicas, estructuras de control (IF/ELSE/LOOP)** y visualización del estado de memoria.

---

## 🧩 Estructura del Proyecto

```bash
CompiladorChocolala/
│
├── src/
│   ├── assembler/
│   │   ├── __pycache__/
│   │   ├── assembly.py          # Aquí se encuentra la clase VirtualMachine
│   │   └── memory.json          # Archivo de memoria persistente
│   │
│   ├── parser/                  # (Aun no implementada)
│   │
│   ├── utils/
│   │   ├── __pycache__/
│   │   ├── auxiliaryFunctions.py
│   │   └── dataStructures.py    # Contiene las clases Stack y Queue
│   │
│   └── main.py                  # Punto de entrada del compilador
│
└── test/                        # Carpeta contenedora para pruebas
```
## ⚙️ Dependencias

El proyecto utiliza únicamente librerías estándar de Python:

- `json` → Se emplea principalmente para poder acceder al mapa de registros, actualizar los registros y guardar los cambios al final del tiempo de vida del programa.
- `time` → Mide el tiempo de ejecución del programa en segundos.
- `os` → Se emplea principalmente para la gestión de rutas del archivo
- `sys` → Se emplea para la lectura del programa

Y depende de dos estructuras propias del proyecto:

- `from utils.dataStructures import Stack`
- `from utils.dataStructures import Queue`

Estas estructuras permiten manejar:
- **Stack:** pila de operaciones aritméticas/lógicas.

- **Queue:** cola de instrucciones del programa, tanto para el flujo normal, como la implementación de bucles.

## 🧮 Estructura de datos empleadas:

### 🧱 Clase Stack 

📁 Ubicación: `src/utils/dataStructures.py`

Estructura tipo **pila (LIFO)**, utilizada para manejar operaciones de la ALU y control de ejecución.

#### 🧩 **Atributos**

| Método | Descripción |
|---------|--------------|
| `self.__body` | Método privado, que a su vez es una Subestructura de datos `Array` que define la capacidad de almacenamiento de nuestro `Stack` |

#### ⚙️ **Métodos**

| Método | Descripción |
|---------|--------------|
| `push(item)` | Agrega un elemento a la cima de la pila. |
| `pop()` | Elimina y devuelve el último elemento agregado. |
| `peek()` | Devuelve el elemento en la cima **sin eliminarlo**. |
| `isEmpty()` | Retorna `True` si la pila está vacía. |
| `__str__` | Devuelve una representación legible del contenido de la pila|


### 🌀 Clase `Queue`

📁 **Ubicación:** `src/utils/dataStructures.py`

La clase **`Queue`** implementa una estructura de datos tipo **cola (FIFO: First In, First Out)**, utilizada principalmente para almacenar las **instrucciones** que ejecuta la `VirtualMachine`.

---

#### 🧩 Atributos Internos

| Atributo | Tipo | Descripción |
|-----------|------|--------------|
| `self.items` | `list` | Lista interna que almacena los elementos de la cola. |

---

#### ⚙️ Métodos Disponibles

| Método | Descripción |
|---------|--------------|
| `push(item)` | Agrega un elemento al **final** de la cola. |
| `pop()` | Elimina y devuelve el **primer** elemento de la cola. |
| `peek()` | Devuelve el primer elemento **sin eliminarlo**. |
| `isEmpty()` | Retorna `True` si la cola está vacía, de lo contrario `False`. |
| `__str__()` | Devuelve una representación legible del contenido de la cola. |
---

## 🧠 Clase Principal: VirtualMachine

📁 **Ubicación:** `src/assembler/assembly.py`

La clase `VirtualMachine` es el núcleo del proyecto.  
Se encarga de interpretar las instrucciones encoladas, simular operaciones de la **ALU**, gestionar los **registros de memoria** y manejar estructuras de control como `IF`, `ELSE`, `LOOP` y `PRINT`.

#### ⚙️ Métodos principales

| Método | Descripción |
|---------|-------------|
| `__init__(queue)` | Inicializa la VM con una cola de instrucciones. |
| `execute(queue)` | Ejecuta todas las instrucciones en la cola principal. |
| `_execute_single_instruction()` | Método privado empleado en `LOOP`, Ejecuta una instrucción aislada. |
| `accessMemory()` / `writeMemory()` | Lectura y escritura del archivo `memory.json`. |
| `updateRegister(register, value)` | Asigna valores a registros disponibles. |
| `freeRegister(register)` | Libera un registro. |
| `decodeTeLaChoco(text)` | Interpreta la notación con emojis y la convierte a números. |

## 💾 Archivo de Memoria (`memory.json`)

Este archivo almacena el estado de los **registros** de la máquina virtual antes, durante y después de la ejecución.

**⚠️ Importante:** Siempre que se ejecute el codigo, tienes que asegurarte que los registros que vayas a emplear estén liberados. Es muy importante por que puede petar el programa. No se pueden sobreescribir los registros

**📜 Tipos de Registro**

- `RN`: Registros empleados por el usuario, abarcan desde el `R1` hasta el `R8`.

- `TN`: Registros empleados para almacenar valores por el usuario, que posteriormente no tendrán relevancia. Los 3 primeros registros temporales son reservados exclusivamente por el sistema. Abarcan desde el `T1` hasta el `T6`.

- `UTN`: Registros empleados por el usuario los cuales cumplen la misma función que los registros temporales. Abarcan desde el `UT1` hasta el `UT9`.
- `OPERATION`: Registro empleado para indicar en el `Stack` el tipo de operación

#### 🧩 Contenido del mapa de registros:

```json
{
    "R1": null,
    "R2": null,
    "R3": null,
    "R4": null,
    "R5": null,
    "R6": null,
    "R7": null,
    "R8": null,
    "T1": null,
    "T2": null,
    "T3": null,
    "T4": null,
    "T5": null,
    "T6": null,
    "UT1": null,
    "UT2": null,
    "UT3": null,
    "UT4": null,
    "UT5": null,
    "UT6": null,
    "UT7": null,
    "UT8": null,
    "UT9": null,
    "OPERATION": null
}

---
```

## 🔠 Tipos de Instrucciones Soportadas
Lista las instrucciones que puede reconocer ATLC. esta sección es muy importante para aquellos que quieren programar con este lenguaje


### 🔠 Lista de Instrucciones Soportadas

| Tipo | Ejemplo | Descripción |
|------|----------|-------------|
| Asignación de Registro | `PR R1 i(🤚)` | Asigna el valor `1` al registro `R1`. |
| Liberación de Registro| `FR R1` | Libera el registro `R1`. |
| Aritméticas | `AND R1 R2 RS`, `OR R1 R2 RS`, `XOR R1 R2 RS`, `NOT R1 RS`, `NAND R1 R2 RS`, `NOR R1 R2 RS`, `XNOR R1 R2 RS`| Ejecuta operaciones lógicas, almacenandolos en un registro `RS` |
| Lógicas | `ADD R1 R2 R3`, `SUB R1 R2 R3`, `MUL R1 R2 R3`, `DIV R1 R2 R3`| `R3 = R1 + R2`, `R3 = R1 - R2`, `R3 = R1 * R2`, `R3 = R1 // R2 ` |
| Condicionales | `IF R1 R2` ... `ENDIF` | Ejecuta un bloque si los registros son iguales. |
| Bucles | `LOOP R1 R2` ... `ENDLOOP` | Repite el bloque hasta que `R1 == R2`. |
| Impresión | `PRINT R1 R2` | Muestra los valores de los registros indicados. |
---
## ⚙️ Función y Procesado de los comandos

Dividiremos el funcionamiento de las funciones según el tipo de operación.

- 🧠 **Acceso a memoria:** Dentro de esta categoría nos encontramos con las siguientes operaciones: 

    1) **`PR RN Valor`** Su funcionamiento es el siguiente:   
        1. Verifica que el registro esté vacio
        2. En caso de estar vacio, almacena el valor en el registro `RN`.

    2) **`FR RN`**: Su pseudocódigo es el siguiente:   
        1. Verifica que el registro no esté vacio
        2. En caso de estar vacio, libera el valor del registro `RN`.
- 🖩 **Operaciones Aritmético-Lógicas**: Dentro de esta sección, englobaremos el funcionamiento de todas las operaciones aritméticas y lógicas. Su funcionamiento en pseudocódigo es el siguiente:
    
    1) Análizamos el tipo de operación, almacenando el tipo en el registro `OPERATION`
    2) Hacemos un push en el Stack de operaciones en este orden: `OPERATION` `V1` `V2` (Depende de la operación es `None` o un valor numérico)
    3) Desencolamos los valores, almacenandolos en los registros temporales `T1` y `T2`
    4) Dependiendo del tipo de operación, ejecutamos el método correspondiente, almacenando el resultado en el registro pasado para almacenar (`RS`)
    5) Liberamos los registros temporales y de ejecución

- ❓ **Condicionales**: Dentro de los condicionales, su funcionamiento es el siguiente:
    
    1)  Comparamos si los valores de los registros pasados
    2) En caso de ser cierto, ejecutamos el bloque de código comprendido entre `IF`, `ELSEIF`,`ELSE`,`ENDIF`.
    3) En caso de no ser cierta, saltamos las instrucciones hasta llegar a los siguientes bloques: `ELSEIF`,`ELSE`,`ENDIF`.
    
- 🔄 **Bucles**: El funcionamiento de los bucles es el siguiente:

    1) Comparamos la condición. Se dejará de ejecutar si la condición es falsa
    2) En caso de no cumplirse la condición, se realizará una copia de todo el código en la cola principal del programa, que abarcará desde `LOOP` hasta `ENDLOOP`, borrando la instrucción del flujo normal con `pop` y almacenandola en la cola secundaria
    3) Se ejecutará cada linea de código con el método privado `execute_line`
    4) Tras la ejecución de la instrucción, se borra y se vuelve a encolar en la cola secundaria
    5) Se verifica al final del funcionamiento si la condición es cierta, en caso de ser cierta, se elimina todo el contenido de la cola secundaria y se sale del flujo de ejecución del programa

⚠️ **Nota**: En caso de ingresar valores numéricos, se hará un paso previo de traducción. 

⚠️ **IMPORTANTE**: Puede ser que la instrucción `LOOP` tenga fallos en la ejecución. Además, no es posible concatenar 2 bucles en una misma instrucción de un bucle.

## Funcionamiento básico del programa

El flujo básico del programa es el siguiente:

1) Creamos y programamos nuestro archivo `.atlc`

2) Ejecutamos nuestro archivo con la siguiente instrucción:
 
```
python (ruta del archivo main.py) (ruta del archivo.atlc)
```

3) Tras ingresar la instrucción, se verifica si el archivo tiene terminación ``.atlc``, en caso de no ser cierto, manda error.

4) Posteriormente, se convierten las instrucciones en un `Array`, separandolos por ``;``, creando los Tokens 

5)  Se almacenan todos los Tokens en una ``Queue`` por fecha de creación

6) Se llamará a la máquina virtual y se ejecutará el método ``execute``

7) Tras finalizar el programa, se informa al usuario que el programa terminó y se muestra el tiempo de ejecución

## 🚨 Manejo de Errores y Validaciones

La VM realiza diversas comprobaciones para asegurar la consistencia de la ejecución:

- ❌ Intentar escribir en un registro ocupado → Error de colisión.
- ❌ Liberar un registro vacío → Error de acceso nulo.
- ⚠️ Uso de registros inexistentes → Error de instrucción inválida.
- ⚠️ Instrucciones mal formadas → Error de sintaxis.

## 🧩 Ejemplo de Programa `.atlc`

```atlc
PR R1 i(✌️);       # R1 = 2
PR R2 i(🤚);       # R2 = 1
ADD R1 R2 R3;      # R3 = R1 + R2
PRINT R3;          # Muestra 3
FR R1; FR R2; FR R3;
```
## 🚀 Mejoras Futuras

-  Implementar el módulo `parser` para análisis léxico y sintáctico.
- Añadir soporte para variables y constantes simbólicas.
- Ampliar el set de instrucciones (`MOD`, `POW`, `CMP`, etc.).
- Implementar optimizaciones de código en tiempo de ejecución.

## 👥 Autores

- **Romendesu, Rodcam** – Desarrolladores principales de ATLC 
