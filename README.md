# Bytecode VM

A small stack-based virtual machine, written in Python, that reads a program
written in a custom instruction set from a `.vm` text file and executes it.

Built to understand how real interpreters (Python's own, the JVM) work
under the hood.

## How it works

1. A `.vm` file is read from disk, one instruction per line.
2. Each line is parsed into a tuple, e.g. `PUSH 5` becomes `("PUSH", 5)`.
3. A `while` loop, driven by a program counter, executes each instruction
   in order against an internal stack.

## Usage

```
python vm.py path/to/program.vm
```

## Instruction Set (current)

| Instruction | Effect                                      |
|-------------|----------------------------------------------|
| `PUSH n`    | Push integer `n` onto the stack               |
| `POP`       | Remove the top value from the stack           |
| `ADD`       | Pop two values, push their sum                |
| `PRINT`     | Print the current top of the stack (does not remove it) |

## Example

`add.vm`:
```
PUSH 5
PUSH 3
ADD
PRINT
```

Running `python vm.py add.vm` prints `16`.

## Error Handling

Errors are strict by design: an unrecognized instruction, or an operation
attempted on an empty stack (e.g. `ADD` with fewer than two values pushed),
raises an exception with a message describing the problem, rather than
failing silently or skipping the bad instruction.

## Status

Actively in development. Not yet implemented, planned next:

- `SUB`, `MUL`, `DIV`
- Variables (`STORE` / `LOAD`)
- Control flow (`JUMP`, `JUMP_IF_FALSE`) — required for loops and conditionals
- Comparison operators (`EQ`, `LT`, `GT`)
