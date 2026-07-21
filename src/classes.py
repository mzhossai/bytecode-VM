import sys


'''              [-------- CLASSES & FUNCTIONS --------]              '''

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
        

# helper functions for parsing
def parsing_with_value(program: list, parts: list):
    program.append((parts[0], int(parts[1])))

def parsing_without_value(program:list, parts:list):
    program.append((parts[0],))



def handle_parsing_push(program: list, parts: list):
    parsing_with_value(program, parts)

def handle_parsing_jump(program: list, parts: list):
    parsing_with_value(program, parts)

def handle_parsing_if_greater_than(program: list, parts: list):
    parsing_with_value(program, parts)

def handle_parsing_if_equal(program: list, parts: list):
    parsing_with_value(program, parts)

def handle_parsing_landing(program: list, parts: list):
    parsing_with_value(program, parts)


def handle_parsing_pop(program: list, parts: list):
    parsing_without_value(program, parts)

def handle_parsing_print(program: list, parts: list):
    parsing_without_value(program, parts)

def handle_parsing_add(program: list, parts: list):
    parsing_without_value(program, parts)

def handle_parsing_sub(program: list, parts: list):
    parsing_without_value(program, parts)

def handle_parsing_mod(program: list, parts: list):
    parsing_without_value(program, parts)

def handle_parsing_store(program: list, parts: list):
    program.append((parts[0], int(parts[1])))

def handle_parsing_load(program: list, parts: list):
    program.append((parts[0], int(parts[1])))

def handle_parsing_exit(program: list, parts: list):
    parsing_without_value(program, parts)





def handle_execution_push(
        program: list,
        instruction: tuple,
        stack: Stack,
        program_counter: int,
        variables: dict
        )-> int:
    stack.PUSH(instruction[1])
    return program_counter + 1

def handle_execution_pop(
        program: list,
        instruction: tuple,
        stack: Stack,
        program_counter: int,
        variables: dict
        ) -> int:
    stack.POP()
    return program_counter + 1

def handle_execution_jump(
        program: list,
        instruction: tuple,
        stack: Stack,
        program_counter: int,
        variables: dict
        ) -> int:
    count = 0
    while count < len(program):
        if program[count][0] == "LANDING" and program[count][1] == instruction[1]:
            return count
        
        count += 1
    raise Exception(f"Landing could not be found for: {instruction[0]}: {instruction[1]}")


def handle_execution_if_greater_than(
        program: list,
        instruction: tuple,
        stack: Stack,
        program_counter: int,
        variables: dict
        ) -> int:
    if stack.PEEK() > instruction[1]:
        return program_counter + 2  # Skip the jump and enter the if block
    else:
        return program_counter + 1  # Jump to the Landing
    

def handle_execution_if_equal(
        program: list,
        instruction: tuple,
        stack: Stack,
        program_counter: int,
        variables: dict
        ) -> int:
    if stack.PEEK() == instruction[1]:
        return program_counter + 2  # Skip the jump and enter the if block
    else:
        return program_counter + 1  # Jump to the Landing

    
def handle_execution_landing(
        program: list,
        instruction: tuple,
        stack: Stack,
        program_counter: int,
        variables: dict
        ) -> int:
    return program_counter + 1


def handle_execution_print(
        program: list,
        instruction: tuple,
        stack: Stack,
        program_counter: int,
        variables: dict
        ) -> int:
    print(f"Testing: Just prints the top of stack -> {stack.PEEK()}")
    return program_counter + 1


def handle_execution_add(
        program: list,
        instruction: tuple,
        stack: Stack,
        program_counter: int,
        variables: dict
        ) -> int:
    value_1 = 0
    value_2 = 0
    if stack.isEmpty():
        raise Exception(f"Stack Empty: Possible excess POP statements | Value 1: {value_1}")
    else:
        value_1 = stack.POP()
    if stack.isEmpty():
        raise Exception(f"Stack Empty: Possible excess POP statements | Value 2: {value_2}")
    else:
        value_2 = stack.POP()
    stack.PUSH(value_1 + value_2)
    return program_counter + 1

def handle_execution_sub(
        program: list,
        instruction: tuple,
        stack: Stack,
        program_counter: int,
        variables: dict
        ) -> int:
    value1 = 0
    value2 = 0
    if stack.isEmpty():
        raise Exception(f"Stack Empty: Possible excess POP statements | Value 1: {value1}")
    else:
        value1 = stack.POP() 
    if stack.isEmpty():
        raise Exception(f"Stack Empty: Possible excess POP statements | Value 2: {value2}")
    else:
        value2 = stack.POP() 
    stack.PUSH(value2 - value1)
    return program_counter + 1


def handle_execution_store(
        program: list,
        instruction: tuple,
        stack: Stack,
        program_counter: int,
        variables: dict
        ) -> int:
    variables[instruction[1]] = stack.POP()
    return program_counter + 1


def handle_execution_load(
        program: list,
        instruction: tuple,
        stack: Stack,
        program_counter: int,
        variables: dict
        ) -> int:
    stack.PUSH(variables[instruction[1]])
    return program_counter + 1


def handle_execution_mod(
        program: list,
        instruction: tuple,
        stack: Stack,
        program_counter: int,
        variables: dict
        ) -> int:
    value1 = 0
    value2 = 0
    if stack.isEmpty():
        raise Exception(f"Stack Empty: Possible excess POP statements | Value 1: {value1}")
    else:
        value1 = stack.POP()
    if stack.isEmpty():
        raise Exception(f"Stack Empty: Possible excess POP statements | Value 2: {value2}")
    else:
        value2 = stack.POP()

    remainder = value2 % value1

    stack.PUSH(remainder)
    return program_counter + 1
    

def handle_execution_exit(
        program: list,
        instruction: tuple,
        stack: Stack,
        program_counter: int,
        variables: dict
        ) -> int:
    print("Exiting Program")
    sys.exit()
