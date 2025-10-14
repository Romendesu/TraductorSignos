from utils.dataStructures import Stack
from utils.dataStructures import Queue
import json
import time
import os

# Variables globales
scriptPath = os.path.dirname(os.path.abspath(__file__))
memoryPath = os.path.join(scriptPath, "memory.json")

# Pequeño script para cargar la memoria
def accessMemory() -> dict:
    with open(memoryPath, "r") as file: 
        return json.load(file)
# Pequeño script para actualizar la memoria
def writeMemory(memory) -> None:
    with open(memoryPath, "w") as file:
        json.dump(memory, file, indent=4)

# Clase Virtual machine
class VirtualMachine:
    def __init__(self, queue):
        # Pasamos el programa como cola
        self.queue = queue
        self.memory = accessMemory()
        self.loopQueue = Queue()
        self.operationsStack = Stack()
        self.resultsStack = Stack()
        
    def execute(self, queue=None) -> None:
        timeI = time.time()
        if queue is  None:
            queue = self.queue
        for indexInstruction in range(len(queue)):
            if self.queue.isEmpty():
                print("\033[96m[INFO] Program finalizated\033[0m")
                break

            # Convertimos la instruccion en una lista
            instruction = (queue.peek()).split()

            # Identificamos el tipo de operacion
            print("="*50)
            print(f"[INSTRUCTION Nº{indexInstruction+1}]: {instruction}")
            self.showRegisters()
            print(f"[INFO] QUEUE:\n", self.queue)

            # Operaciones con Registros
            if (instruction[0] == 'PR' or instruction[0] == "FR"):
                print("[READ] OPERATION TYPE: MODIFY REGISTER")
                match (instruction[0]):
                    # Actualizamos el valor del registro
                    case 'PR':
                        register = instruction[1]
                        value = str(self.decodeTeLaChoco(instruction[2]))

                        print(f"[READ] Register: {register}")
                        print(f"[READ] Value to save: {value}")
                        # Almacenamos el registro
                        if not (self.updateRegister(register,value)):
                            break
                        
                    # Liberamos el registro
                    case 'FR':
                        register = instruction[1]
                        print(f"[READ] Register: {register}")
                        # Liberamos el registro
                        if not (self.freeRegister(register)):
                            break
                    case _:
                        continue
            
            # Operaciones de ALU
            elif instruction[0] in ("ADD","SUB","MUL","DIV","AND","OR","XOR","NAND","NOR","XNOR","NOT"):
                print("\033[95mOPERATION TYPE: ALU OPERATION\033[0m")

                # Paso previo: verificar que el registro para guardar esté vacío
                if instruction[0] == "NOT":
                    value1 = str(self.decodeTeLaChoco(instruction[1]))
                    value2 = None
                    saveReg = instruction[1]  
                else:
                    value1 = instruction[1]
                    value2 = str(self.decodeTeLaChoco(instruction[2]))
                    saveReg = instruction[3]


                # Paso 2: Comprobación si los valores son registros
                if value1[0] == "R":
                    value1 = self.memory[value1]
                if value2 and value2[0] == "R":
                    value2 = self.memory[value2]


                # Paso 3: Pushing en stack
                print("\033[93m[STATUS] PUSHING TO STACK OPERATIONS...\033[0m")
                self.operationsStack.push(instruction[0])
                self.operationsStack.push(value1)
                if value2 is not None:
                    self.operationsStack.push(value2)
                print(self.operationsStack)

                # Paso 4: Procesar operaciones
                print("\033[93m[STATUS] ADDING TO TEMPORAL REGISTER\033[0m")
                t1 = self.memory["T1"] = self.operationsStack.pop()
                print(f"\033[92m[STATUS] ADDED REGISTER TO T1 = {t1}\033[0m")
                t2 = self.memory["T2"] = self.operationsStack.pop() if value2 is not None else None
                if t2 is not None:
                    print(f"\033[92m[STATUS] ADDED REGISTER TO T2 = {t2}\033[0m")
                operation = self.memory["OPERATION"] = self.operationsStack.pop()
                print(f"\033[96m[STATUS] OPERATION = {operation}\033[0m")

                # Paso 5: Realizar operación
                match operation:
                    case "ADD":
                        self.memory[saveReg] = str(self.addOperation(t2, t1))
                    case "SUB":
                        self.memory[saveReg] = str(self.resOperation(t2, t1))
                    case "MUL":
                        self.memory[saveReg] = str(self.mulOperation(t2, t1))
                    case "DIV":
                        self.memory[saveReg] = str(self.divOperation(t2, t1))
                    case "AND":
                        self.memory[saveReg] = str(self.andOperation(t2, t1))
                    case "OR":
                        self.memory[saveReg] = str(self.orOperation(t2, t1))
                    case "XOR":
                        self.memory[saveReg] = str(self.xorOperation(t2, t1))
                    case "NOT":
                        self.memory[saveReg] = str(self.notOperation(t1))
                    case "NAND":
                        self.memory[saveReg] = str(self.nandOperation(t2, t1))
                    case "NOR":
                        self.memory[saveReg] = str(self.norOperation(t2, t1))
                    case "XNOR":
                        self.memory[saveReg] = str(self.xnorOperation(t2, t1))
                    case _:
                        print("\033[91mOperacion no implementada\033[0m")

                # Paso 6: Limpiar registros temporales
                print("\033[94m[DEPURACION] Limpiando registros temporales...\033[0m")
                self.freeRegister("T1")
                self.freeRegister("T2")
                self.freeRegister("OPERATION")

                print("\033[93mMemory actual:\033[0m")
                self.showRegisters()

            # Condicionales
            elif instruction[0] in ("IF", "ELSEIF", "ELSE", "ENDIF"):
                op = instruction[0]

                # ENDIF: finalizamos el bloque
                if op == "ENDIF":
                    print("\033[96mINSTRUCTION FINALIZATED\033[0m")
                    continue

                # IF o ELSEIF: verificamos condiciones
                if op in ("IF", "ELSEIF"):
                    if len(instruction) < 3:
                        print(f"\033[91m[ERROR] {op} WITHOUT ENOUGH PARAMETERS\033[0m")
                        continue
                    subcondition1, subcondition2 = instruction[1], instruction[2]

                    # Si la condición es falsa, saltamos hasta ELSEIF, ELSE o ENDIF
                    if subcondition1 != subcondition2:
                        print(f"\033[93m[STATUS] {op} CONDITION IS FALSE, SKIPPING UNTIL ELSEIF, ELSE OR ENDIF\033[0m")
                        while not self.queue.isEmpty():
                            skipped_instruction = self.queue.pop()
                            print(f"\033[95mSkipped instruction: {skipped_instruction}\033[0m")

                            next_instruction = self.queue.peek()
                            if not next_instruction:
                                break

                            next_op = next_instruction.split()[0]
                            print(f"\033[94mNext operation: {next_op}\033[0m")
                            if next_op in ("ELSEIF", "ELSE", "ENDIF"):
                                break
                    else:
                        print(f"\033[92m[STATUS] {op} CONDITION IS TRUE, EXECUTING BLOCK\033[0m")
                
                # ELSE: siempre se ejecuta si llegamos hasta aquí
                elif op == "ELSE":
                    print("\033[96m[STATUS] ELSE BLOCK, EXECUTING\033[0m")
            elif instruction[0] == "&&":
                print("Comment, omit")
            elif instruction[0] == "PRINT":
                print("\033[96m[PRINT] Mostrando registros:\033[0m")
                # Iteramos sobre los registros pasados como parámetros
                for reg in instruction[1:]:
                    # Comprobamos si el registro existe en memoria
                    if reg in self.memory:
                        value = self.memory[reg]
                        if value is None:
                            print(f"REGISTRO {reg}: \033[91mEMPTY\033[0m")
                        else:
                            print(f"REGISTRO {reg}: {value}")
                    else:
                        print(f"REGISTRO {reg}: \033[91mINVALID REGISTER\033[0m")

            elif instruction[0] == "LOOP":
                print("\033[95m[STATUS] DETECTED LOOP BLOCK\033[0m")
                reg1, reg2 = instruction[1], instruction[2]

                # *** CORRECCIÓN CRÍTICA: Consumir la instrucción 'LOOP R1 R2' ***
                self.queue.pop() 

                # Capturar instrucciones del LOOP
                loopQueue = Queue()
                while True:
                    instr_raw = self.queue.peek()
                    if instr_raw is None:
                        print("\033[91m[ERROR] Unexpected end of queue while reading LOOP block.\033[0m")
                        return # Terminar la ejecución
                    
                    # Consumir la instrucción del flujo principal
                    instr = self.queue.pop()
                    
                    # Usamos .strip().startswith() para ignorar espacios/comentarios
                    if instr.strip().startswith("ENDLOOP"):
                        print("[LOOP] ENDLOOP detected and consumed.")
                        break
                    loopQueue.push(instr)

                print(f"[LOOP] Captured {len(loopQueue)} instructions.")

                # Ejecutar LOOP mientras reg1 != reg2
                iteration = 0
                
                # *** NORMALIZACIÓN CRÍTICA: Obtener y normalizar los valores a cadena para la comparación ***
                val1 = str(self.memory.get(reg1, ''))
                val2 = str(self.memory.get(reg2, ''))
                
                while val1 != val2:
                    iteration += 1
                    print(f"\n\033[96m{'='*15} [LOOP ITERATION {iteration}] {reg1}={val1}, {reg2}={val2} {'='*15}\033[0m")

                    # Usamos una cola temporal para preservar las instrucciones originales
                    tempQueue = Queue()
                    error_during_iteration = False 
                    
                    while not loopQueue.isEmpty():
                        instr_loop_raw = loopQueue.pop()
                        tempQueue.push(instr_loop_raw)
                        
                        # *** CORRECCIÓN DE PARSING: Limpiar comentarios anexos y encabezados ***
                        # Eliminar comentarios '//' y '&&' antes de dividir, luego limpiar extremos y ;
                        instr_cleaned = instr_loop_raw.split('//')[0].split('&&')[0].rstrip(';').strip()
                        instr_loop = instr_cleaned.split()

                        # Si la lista está vacía (era solo un comentario o línea vacía), continuar
                        if not instr_loop:
                            continue 
                        
                        # LLAMADA CLAVE: Usamos el método auxiliar
                        print(f"\033[94m[LOOP EXEC] {instr_loop}\033[0m")
                        if not self._execute_single_instruction(instr_loop):
                            print(f"\033[91m[ERROR] Failed instruction during LOOP: {instr_loop_raw}\033[0m")
                            error_during_iteration = True
                            break # Romper el bucle interno
                            
                    loopQueue = tempQueue # Reasignamos para la siguiente iteración
                    
                    # *** SALIDA DE EMERGENCIA ***
                    if error_during_iteration:
                        print("\033[91m[FATAL] Exiting program due to LOOP error.\033[0m")
                        return # Salir de la función execute inmediatamente

                    # *** ACTUALIZACIÓN DE VALORES PARA LA PRÓXIMA CONDICIÓN ***
                    val1 = str(self.memory.get(reg1, ''))
                    val2 = str(self.memory.get(reg2, ''))
                    
                print(f"\033[92m[LOOP] Finalized after {iteration} iterations.\033[0m")
                continue # Saltar al siguiente ciclo del for
            
            # Operacion no encontrada
            else:
                print(f"[ERROR] Invalid operation, passed argument: {instruction[0]}")
                break
            print("[INFO] Pass to next instruction...")
            self.queue.pop()
        writeMemory(self.memory)
        print(f"\033[96m[EXIT] Program executed in {time.time() - timeI:.4f} seconds.\033[0m")

    def _execute_single_instruction(self, instruction_list) -> bool:
        """
        Ejecuta una única instrucción (PR, FR, ALU, PRINT) sin consumir de la cola principal.
        Devuelve True si la ejecución fue exitosa, False en caso de error.
        """
        instruction = instruction_list
        op = instruction[0]

        # Operaciones con Registros (PR/FR)
        if op == 'PR' or op == "FR":
            print("[READ] OPERATION TYPE: MODIFY REGISTER")
            match (op):
                # Inside _execute_single_instruction, case 'PR':
                case 'PR':
                    register = instruction[1]  # Destino (e.g., 'R1')
                    source = instruction[2]    # Fuente (e.g., 'T7', 'i(🤚)', o '3')
                    
                    value_to_save = None

                    # 1. Verificar si la fuente es un registro ('R' o 'T')
                    
                    if isinstance(source, str) and (source.startswith('R') or source.startswith('T')):
                        value_to_save = self.memory.get(source)
                        
                        if value_to_save is None:
                            print(f"\033[91m[ERROR] Source register {source} is EMPTY during PR.\033[0m")
                            return False
                    
                    # 2. Si no es un nombre de registro, es un literal (i(...) o un número)
                    else:
                        value_to_save = self.decodeTeLaChoco(source)

                    return self.updateRegister(register, str(value_to_save))
                
                case 'FR':
                    register = instruction[1]
                    print(f"[READ] Register: {register}")
                    return self.freeRegister(register)
                case _:
                    return True # Continua

        # Operaciones de ALU
        elif op in ("ADD","SUB","MUL","DIV","AND","OR","XOR","NAND","NOR","XNOR","NOT"):
            print("\033[95mOPERATION TYPE: ALU OPERATION\033[0m")

            # La lógica de ALU permanece casi intacta
            if op == "NOT":
                value1_raw = instruction[1]
                value2_raw = None
                saveReg = instruction[1] 
            else:
                value1_raw = instruction[1]
                value2_raw = instruction[2]
                saveReg = instruction[3]

            # Obtención de valores (decodificación y lectura de registro)
            value1 = self.decodeTeLaChoco(value1_raw)
            value2 = self.decodeTeLaChoco(value2_raw) if value2_raw else None
            
            if isinstance(value1, str) and value1.startswith("R") and value1 in self.memory:
                value1 = self.memory[value1]
            if value2 is not None and isinstance(value2, str) and value2.startswith("R") and value2 in self.memory:
                value2 = self.memory[value2]

            # Pushing en stack (la lógica de la pila se mantiene)
            print("\033[93m[STATUS] PUSHING TO STACK OPERATIONS...\033[0m")
            self.operationsStack.push(instruction[0])
            self.operationsStack.push(str(value1))
            if value2 is not None:
                self.operationsStack.push(str(value2))

            # Procesar operaciones (pop de pila a registros temporales T1, T2, OPERATION)
            print("\033[93m[STATUS] ADDING TO TEMPORAL REGISTER\033[0m")
            t1 = self.memory["T1"] = self.operationsStack.pop()
            t2 = self.memory["T2"] = self.operationsStack.pop() if value2 is not None else None
            operation = self.memory["OPERATION"] = self.operationsStack.pop()

            # Realizar operación
            try:
                result = None
                match operation:
                    case "ADD": result = self.addOperation(t2, t1)
                    case "SUB": result = self.resOperation(t2, t1)
                    case "MUL": result = self.mulOperation(t2, t1)
                    case "DIV": result = self.divOperation(t2, t1)
                    case "AND": result = self.andOperation(t2, t1)
                    case "OR": result = self.orOperation(t2, t1)
                    case "XOR": result = self.xorOperation(t2, t1)
                    case "NOT": result = self.notOperation(t1)
                    case "NAND": result = self.nandOperation(t2, t1)
                    case "NOR": result = self.norOperation(t2, t1)
                    case "XNOR": result = self.xnorOperation(t2, t1)
                    case _:
                        print("\033[91mOperacion no implementada\033[0m")
                        return False
                
                self.memory[saveReg] = str(result)
            except Exception as e:
                print(f"\033[91m[ERROR] ALU Operation failed: {e}\033[0m")
                return False

            # Limpiar registros temporales
            self.freeRegister("T1")
            self.freeRegister("T2")
            self.freeRegister("OPERATION")
            return True

        # Operación PRINT
        elif op == "PRINT":
            print("\033[96m[PRINT] Mostrando registros:\033[0m")
            for reg in instruction[1:]:
                if reg in self.memory:
                    value = self.memory[reg]
                    print(f"REGISTRO {reg}: \033[91mEMPTY\033[0m" if value is None else f"REGISTRO {reg}: {value}")
                else:
                    print(f"REGISTRO {reg}: \033[91mINVALID REGISTER\033[0m")
            return True
        
        # Omitir condicionales y comentarios en esta sub-ejecución, o dejar la lógica de 'execute' manejarlos.
        elif op in ("IF", "ELSEIF", "ELSE", "ENDIF", "&&"):
             return True # Dejar que el ciclo principal de 'execute' maneje el flujo/salto.

        else:
            print(f"[ERROR] Invalid operation, passed argument in loop: {op}")
            return False   

    '''
    ------------------------------------------------------------------------------------
    --------------------------- LOGICA DE LAS INSTRUCCIONES ----------------------------
    ------------------------------------------------------------------------------------
    
    '''

    # Operaciones con acceso de memoria

    # Funcion para mostrar registros
    def showRegisters(self) -> None:
        print(f"\033[93m{'='*21} MEMORY {'='*21}\033[00m")
        for register, value in self.memory.items():
            print(f"\033[93m{register}: \033[91mEMPTY\033[00m\033[93m" if value is None else f"\033[93m{register}: {value}\033[00m")
        print(f"\033[93m{'='*50}\033[00m")

    # Funcionamiento de PR
    def updateRegister(self, register, value) -> bool:
        # Verificamos que el registro este ocupado
        if (self.memory[register] is not None):
            print(f"\033[91m[ERROR] Can't update register, {register} = {self.memory[register]}\033[00m")
            return False
        self.memory[register] = value
        print(f"\033[92m[SUCCESS] Register updated with value: {value}\033[00m")
        return True

    # Funcionamiento de FR
    def freeRegister(self, register) -> bool:
        # Comprobamos que el registro se ha usado
        if (self.memory[register] is None):
            print(f"\033[91m[ERROR] Can't free register {register}: The register is not used\033[00m")
            return False
        self.memory[register] = None
        print(f"\033[92m[SUCCESS] The register {register} is free\033[00m")
        return True
    # Comprobacion del estado del registro
    def isRegisterEmpty(self, register):
        return True if self.memory[register] is None else False
    
    # Operaciones ALU

    # Operaciones Aritmeticas
    def addOperation(self, value1, value2) -> str:
        return str(int(value1) + int(value2))
         
    
    def resOperation(self, value1, value2) -> int:
        return int(value1) - int(value2)
    
    def mulOperation(self, value1, value2):
        return int(value1) * int(value2)
    
    def divOperation(self, value1, value2):
        return int(value1) // int(value2)

    # Operaciones Logicas

    def andOperation(self, value1, value2) -> bool:
    # Devuelve True si ambos valores son "iguales y verdaderos" (no vacíos ni 0)
        return bool(value1) and bool(value2)

    def orOperation(self, value1, value2) -> bool:
        # Devuelve True si al menos uno de los valores no está vacío ni es 0
        return bool(value1) or bool(value2)

    def xorOperation(self, value1, value2) -> bool:
        # Verdadero si exactamente uno de los dos tiene "valor verdadero"
        return bool(value1) != bool(value2)

    def notOperation(self, value):
        # Invierte el valor lógico de "value"
        return not bool(value)

    def nandOperation(self, value1, value2):
        # Negación del AND
        return not (bool(value1) and bool(value2))

    def norOperation(self, value1, value2):
        # Negación del OR
        return not (bool(value1) or bool(value2))

    def xnorOperation(self, value1, value2):
        # Verdadero si ambos son "verdaderos" o ambos son "falsos"
        return bool(value1) == bool(value2)
    
    def decodeTeLaChoco(self, text):
        handDict = {
            'i(🤚)': '1',
            'i(🤚🤚)': '2',
            'i(🤚🤚🤚)': '3',
            'i(✋🤚)': '4',
            'i(✋)': '5',
            'i(🤚✋)': '6',
            'i(🤚🤚✋)': '7',
            'i(🤚🤚🤚✋)': '8',
            'i(🤚👊)': '9',
            'i(👊)': '0'
        }

        if not isinstance(text, str):
            return text

        clean_text = text.strip()
        result = clean_text

        # Reemplazar todos los patrones por su número
        for k, v in handDict.items():
            result = result.replace(k, v)

        # Si contiene solo dígitos, convertir a int
        return int(result) if result.isdigit() else text



        
