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
        self.operationsStack = Stack()
        self.resultsStack = Stack()
        
    def execute(self) -> None:
        timeI = time.time()
        
        for indexInstruction in range(len(self.queue)):
            if self.queue.isEmpty():
                print("\033[96m[INFO] Program finalizated\033[0m")
                break

            # Convertimos la instruccion en una lista
            instruction = (self.queue.peek()).split()

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
                        value = self.decodeTeLaChoco(instruction[2])

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
                for register in instruction:
                    if register == "PRINT":
                        print("MOSTRANDO REGISTROS:")
                    else:
                        print(f"REGISTRO {register}:")
            # Operacion no encontrada
            else:
                print(f"[ERROR] Invalid operation, passed argument: {instruction[0]}")
                break
            print("[INFO] Pass to next instruction...")
            self.queue.pop()
        writeMemory(self.memory)
        print(f"\033[96m[EXIT] Program executed in {time.time() - timeI:.4f} seconds.\033[0m")


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



        
