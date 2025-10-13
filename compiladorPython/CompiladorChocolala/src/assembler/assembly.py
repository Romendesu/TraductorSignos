from utils.dataStructures import Queue
from utils.dataStructures import Stack
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
                        register, value = instruction[1], instruction[2]
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
            elif (instruction[0] == "ADD" or instruction[0] == "SUB"
            or instruction[0] == "MUL" or instruction[0] == "DIV"):
                print("OPERATION TYPE: ALU OPERATION")
                # Paso previo: Velificar que el registro para almacenar este vacio
                if not self.isRegisterEmpty(instruction[-1]):
                    print(f"[ERROR] Saving register is not empty, value = {self.memory[instruction[-1]]}")

                # Paso 1: Introducir valores
                value1, value2, saveReg = instruction[1], instruction[2], instruction[3]
                print(value1, value2)
                
                
                # Paso 2: Verificar valores
                while (value1[0] == "R" or value2[0] == "R"):
                    # Si el primer valor es un registro:
                    if value1[0] == "R" and value2[0] != "R":
                        value1 = self.memory[value1]
                    elif value2[0] == "R" and value2[0] != "R":
                        value2 = self.memory[value2]
                    else:
                        value1, value2 = self.memory[value1], self.memory[value2]
                print(value1, value2)

                # Paso 3: Ingresar en un STACK
                self.operationsStack.push(instruction[0])
                self.operationsStack.push(value1)
                self.operationsStack.push(value2)
                # Paso 4: Procesar operaciones
                t1 = self.memory["T1"] = self.operationsStack.pop()
                t2 = self.memory["T2"] = self.operationsStack.pop()
                operation = self.memory["OPERATION"] = self.operationsStack.pop()
                # Paso 5: REALIZAR OPERACIONES
                match operation:
                    case "ADD":
                        self.memory[saveReg] = self.addOperation(t2, t1) 
                        continue
                    case "SUB":
                        self.memory[saveReg] = self.resOperation(t2, t1)
                        continue
                    case "MUL":
                        self.memory[saveReg] = self.mulOperation(t2, t1)
                        continue
                    case "DIV":
                        self.memory[saveReg] = self.divOperation(t2, t1)
                        continue
                # Paso 6: Limpiar registros temporales
                self.freeRegister("T1")
                self.freeRegister("T2")
                self.freeRegister("OPERATION")

                    
            # Operaciones Logicas
            elif (instruction[0] == "AND" or instruction[0] == "OR" or instruction[0] == "XOR" or instruction[0] == "NAND" or instruction[0] == "NOR" or instruction[0] == "XNOR"):
                print("[INFO] AND OPERATION PROCCESSING")
                # Paso previo: Comprobar que el registro donde se vaya a guardar este vacio
                if not self.isRegisterEmpty(instruction[-1]):
                    print(f"[ERROR] Can't do the operation, register: {instruction[3]} has the value: {self.memory[instruction[3]]}")
                    break
                # Paso 1: Ingresamos en la pila los valores para realizar la operacion
                if instruction[1][0] != "R" and instruction[2][0] != "R":
                    print("No se esta trabajando con registros")
                    self.operationsStack.push("AND")
                    self.operationsStack.push(instruction[1]) 
                    self.operationsStack.push(instruction[2])
                    print(self.operationsStack)
                else:
                    print("Se esta trabajando con registros")
                    if not self.isRegisterEmpty(instruction[1]) and not self.isRegisterEmpty(instruction[2]):
                        self.operationsStack.push("AND")
                        self.operationsStack.push(self.memory[instruction[1]])
                        self.operationsStack.push(self.memory[instruction[2]])
                        print(self.operationsStack)
                    else:
                        break
                    
                
                # Paso 2: Para el flujo normal, almacenamos los valores en registros temporales
                self.memory["T1"] = self.operationsStack.pop()
                self.memory["T2"] = self.operationsStack.pop()
                self.showRegisters()

                # Paso 3: Comprobar que el registro pasado este libre
                if not self.isRegisterEmpty(instruction[-1]):
                    print("[ERROR] Can't do the operation")

            # Operacion no encontrada
            else:
                print(f"[ERROR] Invalid operation, passed argument: {instruction[0]}")
                break
            print("[INFO] Pass to next instruction...")
            self.queue.pop()
        writeMemory(self.memory)
        print(f"[EXIT] Program executed in {time.time() - timeI} seconds.")


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
    def addOperation(self, value1, value2) -> float:
        return float(int(value1) + int(value2))
         
    
    def resOperation(self, value1, value2):
        return None
    
    def mulOperation(self, value1, value2):
        return None
    
    def divOperation(self, value1, value2):
        return None

    # Operaciones Logicas

    def andOperation(self, value1, value2) -> bool:
        return bool(value1 and value2)
    
    def orOperation(self, value1, value2) -> bool:
        return bool(value1 or value2)
    
    def xorOperation(self, value1,value2) -> bool:
        # O un valor, o el otro, pero no los 2
        return bool((not value1 and value2) or (value1 and not value2))
    
    def notOperation(self, value):
        return bool(not value)

    def nandOperation(self, value1, value2):
        return bool(not (value1 and value2))
    
    def norOperation(self, value1, value2):
        return bool(not(value1 or value2))
    
    def xnorOperation(self, value1, value2):
        return bool(not ((not value1 and value2) or (value1 and not value2)))
    
 
    

