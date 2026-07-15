'''
Overall Structure:
    - Read a .vm file (file ending with .vm)
        - first make it be able to open test.vm
        - parse the contents of the file

        I wanna store stuff in a stack.
        When should I use a stack.
            Math
            Variable stuff ...maybe
        

Checkpoint:
    Change up the code to be a while loop
    - First store ever instruction in the file into a program[] list
    - Then go through the program[] and do them with a wile loop and if statements (later hashtable)
    

'''

import sys




''' Classes '''

class Stack:
    def __init__(self):
        self.stack = []

    def PUSH(self, value):
        self.stack.append(value)
    
    def POP(self):
        if not self.stack:
            print("Stack Empty")
        return self.stack.pop()
        
    
    def PEEK(self) -> int:
        if not self.stack:
            print("Stack Empty")
        return self.stack[-1]




filepath = sys.argv[1]


# Open the file and parse through it
# Store every line as a list
with open(filepath, 'r') as prog_file:
    prog_lines = [line.strip() for line in prog_file.readlines()]


# Create a stack for doing stuff
myStack = Stack()


# Seperate each item in the list into a list of instructions
program = []
counter = 0

for line in prog_lines:
    parts = line.split()
    opcode = parts[0]

    if opcode == "":
        continue

    elif opcode == "PUSH":
         myStack.PUSH(int(parts[1]))
         counter += 1
    
    elif opcode == "POP":
        myStack.POP()

    elif opcode == "ADD":
        num1 = myStack.POP()

        num2 = myStack.POP()

        myStack.PUSH(num1 + num2)

    elif opcode == "PRINT":
        print(myStack.PEEK())

    else:
        raise ValueError(f"Unknown Instruction: {opcode}")


