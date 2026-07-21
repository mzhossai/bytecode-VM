
'''
    TODAY:
        Implementing FizzBuzz
            - Count from 1 - 15
            - If value can be divided by 3 with no remainder, print Fizz
            - If value can be divided by 5 with no remainder, print Buzz
            - If both, print FizzBuzz
        
        1) Compute remainders
            Create MOD
                MOD divides two values in the stack
                Pops them from the stack
                Pushes the remainder
            Store/Load
            Create For Loop
                A counter variable
                    When you get to end, update by one
                A comparison with VARIABLES
                A conditional Exit
                A jump back to the top
'''


import sys
from classes import *





filepath = sys.argv[1]

# Open the file and parse through it
# Store every line as a list
with open(filepath, 'r') as prog_file:
    prog_lines = [line.strip() for line in prog_file.readlines()]




opcode_parsing_dict = {
    "PUSH": handle_parsing_push,
    "JUMP": handle_parsing_jump,
    "IF_GREATER_THAN": handle_parsing_if_greater_than,
    "IF_LESS_THAN": handle_parsing_if_less_than,
    "LANDING": handle_parsing_landing,
    "POP": handle_parsing_pop,
    "PRINT": handle_parsing_print,
    "ADD": handle_parsing_add,
    "SUB": handle_parsing_sub,
    "MOD": handle_parsing_mod,
    "IF_EQUAL": handle_parsing_if_equal,
    "STORE": handle_parsing_store,
    "LOAD": handle_parsing_load,
    "EXIT": handle_parsing_exit
}

opcode_execution_dict = {
    "PUSH": handle_execution_push,
    "JUMP": handle_execution_jump,
    "IF_GREATER_THAN": handle_execution_if_greater_than,
    "IF_LESS_THAN": handle_execution_if_less_than,
    "POP": handle_execution_pop,
    "PRINT": handle_execution_print,
    "ADD": handle_execution_add,
    "SUB": handle_execution_sub,
    "MOD": handle_execution_mod,
    "IF_EQUAL": handle_execution_if_equal,
    "STORE": handle_execution_store,
    "LOAD": handle_execution_load,
    "EXIT": handle_execution_exit,
    "LANDING": handle_execution_landing
}



'''              [-------- PROGRAM FILE PARSER --------]              '''

program = []            # Tokenized list of all the instructions in .vm file
token_counter = 0       # Token counter

for line in prog_lines:

    parts = line.split()

    if not parts:
        continue

    opcode = parts[0]

    if opcode not in opcode_parsing_dict:
        raise ValueError(f"Invalid Syntax: {opcode}")

    else:
        opcode_parsing_dict[opcode](program, parts)
        token_counter += 1



'''              [-------- PROGRAM EXECUTION --------]              '''

program_counter = 0
# Create a stack for doing stuff
myStack = Stack()
variables = {}

while program_counter < token_counter:
    
    instruction = program[program_counter]
    opcode = instruction[0]


    if opcode not in opcode_execution_dict:
        raise Exception(f"Invalid Syntax During Execution: {opcode}")

    else:
        program_counter = opcode_execution_dict[opcode](program, instruction, myStack, program_counter, variables)

        
