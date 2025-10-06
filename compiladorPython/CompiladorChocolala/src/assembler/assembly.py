class VirtualMachine:
    def __init__(program):
        # Pasamos el programa como cola
        self.program = program
        self.register = {"R1":None,"R2":None,"R3":None,"R4":None,"R5":None,"R6":None,
                        "T1":None,"T2":None,"T3":None,"T4":None,"T5":None,"T6":None}
        self.operationsStack = []
        self.resultsStack = []
    

