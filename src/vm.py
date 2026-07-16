'''
    ToDo (loose):
     - Add jump instructions
        - might need to include bp pointers (like assembly)
     - Maybe make it more like assembly; more intuitive
     - Might need to restructure
     - In the PROGRAM FILE PARSER maybe include empty lines
        - to keep track of where the error could be in a .vm file
     - Make sure PRINT can do more, not just whatever's at the top of stack
     - Change how filepath is accessed for .vm files
     
     IMPORTANT maybe
     - Change the if-else chain to a hashmap

'''

import sys




'''              [-------- CLASSES --------]              '''

class Stack:
    def __init__(self):
        self.stack = []

    def PUSH(self, value):
        self.stack.append(value)
    
    def POP(self):
        if self.isEmpty():
            print("Stack Empty")
        return self.stack.pop()
    

    def PEEK(self) -> int:
        if self.isEmpty():
            print("Stack Empty")
        return self.stack[-1]


    def isEmpty(self) -> bool:
        if not self.stack:
            return True
        else:
            return False





filepath = sys.argv[1]

# Open the file and parse through it
# Store every line as a list
with open(filepath, 'r') as prog_file:
    prog_lines = [line.strip() for line in prog_file.readlines()]


# Create a stack for doing stuff
myStack = Stack()





'''              [-------- PROGRAM FILE PARSER --------]              '''

program = []            # Tokenized list of all the instructions in .vm file
token_counter = 0       # Token counter

for line in prog_lines:

    parts = line.split()

    if not parts:
        continue

    opcode = parts[0]

    if opcode == "PUSH":
        program.append((opcode, int(parts[1])))
        token_counter += 1
    
    elif opcode in ("POP", "PRINT", "ADD"):
        program.append((opcode,))
        token_counter += 1

    else:
        raise ValueError(f"Invalid Syntax: {opcode}")




'''              [-------- PROGRAM EXECUTION --------]              '''

program_counter = 0

while program_counter < token_counter:
    
    instruction = program[program_counter]
    opcode = instruction[0]

    if opcode == "PUSH":
        myStack.PUSH(instruction[1])

    elif opcode == "POP":
        myStack.POP()
    
    elif opcode == "PRINT":
        print(f"Testing: Just prints the top of stack -> {myStack.PEEK()}")
    
    elif opcode == "ADD":
        value_1 = 0
        value_2 = 0

        if myStack.isEmpty():
            raise Exception(f"Stack Empty: Possible excess POP statements | Value 1: {value_1}")
        else:
            value_1 = myStack.POP()

        if myStack.isEmpty():
            raise Exception(f"Stack Empty: Possible excess POP statements | Value 2: {value_2}")
        else:
            value_2 = myStack.POP()

        myStack.PUSH(value_1 + value_2)
    
    else:
        raise ValueError(f"Invalid Syntax: {opcode}")
        
    program_counter += 1
