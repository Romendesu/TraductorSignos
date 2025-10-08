from utils.dataStructures import Queue
from utils.dataStructures import Stack
import time

class VirtualMachine:
    def __init__(self, queue):
        # Pasamos el programa como cola
        self.queue = queue
        self.memory = {"R1":None,"R2":None,"R3":None,"R4":None,"R5":None,"R6":None,
                        "T1":None,"T2":None,"T3":None,"T4":None,"T5":None,"T6":None}
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
                        sum1, sum2, register = register[1], register[2], register[3]
                        # Logica de la suma
                        # Emplea funciones para definir la logica de la suma
                        continue
                    case "SUB":
                        sub1, sub2, register = register[1], register[2], register[3]
                        # Logica de la resta
                        # Emplea funciones para definir la logica de la resta
                        continue
                    case "MUL":
                        mul1, mul2, register = register[1], register[2], register[3]
                        # Logica de la multiplicacion
                        # Emplea funciones para definir la logica de la multiplicacion
                        continue
                    case "DIV":
                        div1, div2, register = register[1], register[2], register[3]
                        # Logica de la division
                        # Emplea funciones para definir la logica de la division
                        continue
                
            
            # Operacion no encontrada
            else:
                print(f"[ERROR] Invalid operation, passed argument: {instruction[0]}")
                break
            print("[INFO] Pass to next instruction...")
            self.queue.pop()

        print(f"[EXIT] Program executed in {time.time() - timeI} seconds.")


    # Funcion para mostrar registros
    def showRegisters(self) -> None:
        print(f"\033[93m{f"{"="*21} MEMORY {"="*21}"}\033[00m")
        for register, value in self.memory.items():
            print(f"\033[93m{f"{register}: {f"\033[91m{"EMPTY"}\033[00m" if value == None else value}"}\033[00m")
        print(f"\033[93m{"="*50}\033[00m")

    # Funcionamiento de PR
    def updateRegister(self, register, value) -> bool:
        # Verificamos que el registro este ocupado
        if (self.memory[register] is not None):
            print(f"\033[91m{f"[ERROR] Can't update register, {register} = {self.memory[register]}"}\033[00m")
            return False
        self.memory[register] = value
        print(f"\033[92m{f"[SUCCESS] Register updated with value: {value}"}\033[00m")
        return True

    # Funcionamiento de FR
    def freeRegister(self, register) -> bool:
        # Comprobamos que el registro se ha usado
        if (self.memory is None):
            print(f"\033[91m{f"[ERROR] Can't free register {register}: The register is not used"}\033[00m")
            return False
        self.memory[register] = None
        print(f"\033[92m{f"[SUCCESS] The register {register} is free"}\033[00m")
        return True


