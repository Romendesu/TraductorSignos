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
                match instruction[0]:
                    case "ADD":
                        sum1, sum2, reg = instruction[1], instruction[2], instruction[3]
                        # Logica de la suma
                        # Emplea funciones para definir la logica de la suma
                        continue
                    case "SUB":
                        sub1, sub2, reg = instruction[1], instruction[2], instruction[3]
                        # Logica de la resta
                        # Emplea funciones para definir la logica de la resta
                        continue
                    case "MUL":
                        mul1, mul2, reg = instruction[1], instruction[2], instruction[3]
                        # Logica de la multiplicacion
                        # Emplea funciones para definir la logica de la multiplicacion
                        continue
                    case "DIV":
                        div1, div2, reg = instruction[1], instruction[2], instruction[3]
                        # Logica de la division
                        # Emplea funciones para definir la logica de la division

                    
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
    def addOperation(self, r1,r2,rs):
        return None
    
    def resOperation(self, r1,r2,rs):
        return None
    
    def mulOperation(self, r1,r2,rs):
        return None
    
    def divOperation(self, r1,r2,rs):
        return None
    # Operaciones Logicas

    def andOperation(self, value1, value2) -> bool:
        return value1 and value2
    
    def orOperation(self, r1,r2,rs):
        return None
    
    def xorOperation(self, r1,r2,rs):
        return None
    
    def notOperation(self, r1):
        return None
    def nandOperation(self, r1,r2,rs):
        return None
    
    def norOperation(self, r1,r2,rs):
        return None
    
    def xnorOperation(self, r1,r2,rs):
        return None
    
 
    

