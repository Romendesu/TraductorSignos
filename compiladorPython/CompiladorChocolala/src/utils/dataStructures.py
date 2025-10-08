'''
==================================================
| CREACION DE LAS ESTRUCTURAS DE DATOS EMPLEADAS |
==================================================
'''
class Stack:
    def __init__(self):
        self.__body = []
    
    def __str__(self):
        if self.isEmpty():
            return "[Stack vacío]"
        s = "Stack (top → bottom):\n"
        for elem in reversed(self.__body):
            s += f"| {elem} |\n"
        s += "‾‾‾‾‾‾‾"
        return s
    
    def isEmpty(self):
        return len(self.__body) == 0
    
    def push(self, element):
        self.__body.append(element)
    
    def pop(self):
        return self.__body.pop() if not self.isEmpty() else None
    
    def peek(self):
        return self.__body[-1] if not self.isEmpty() else None

class Queue:
    def __init__(self):
        self.__body = []
    
    def __str__(self):
        if self.isEmpty():
            return "[Queue vacío]"
        return "Queue (head → tail): " + " <- ".join(str(e) for e in self.__body)

    def isEmpty(self):
        return len(self.__body) == 0
    
    def push(self,element):
        self.__body.append(element)
    
    def pop(self):
        return self.__body.pop(0) if not self.isEmpty() else None
    
    def peek(self):
        return self.__body[0] if not self.isEmpty() else None
    
    def __len__(self):
        return len(self.__body)
