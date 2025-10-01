class Stack:
    def __init__(self):
        self.__body = []
        self.__stackPtr = 0
    
    def isEmpty(self):
        return len(self.__body) == 0
    
    def push(self, element):
        self.__body.append()