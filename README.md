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

Dispatch, for both parsing and execution, is done through dictionaries
mapping opcode strings to handler functions, rather than a long if/elif
chain.

## Usage

```
python vm.py path/to/program.vm
```

## Instruction Set

| Instruction         | Effect                                                        |
| ------------------- | ------------------------------------------------------------- |
| `PUSH n`            | Push integer `n` onto the stack                               |
| `POP`               | Remove the top value from the stack                           |
| `ADD`               | Pop two values, push their sum                                |
| `SUB`               | Pop two values, push the first-pushed minus the second-pushed |
| `PRINT`             | Print the current top of the stack (does not remove it)       |
| `IF_GREATER_THAN n` | Compare top of stack to `n`; see Control Flow below           |
| `JUMP n`            | Jump execution to the matching `LANDING n`                    |
| `LANDING n`         | A named jump target; no effect on its own                     |
| `EXIT`              | Immediately end program execution                             |

## Control Flow

`IF_GREATER_THAN` is always paired with a `JUMP` on the very next line, and
the block that follows the `IF_GREATER_THAN`/`JUMP` pair must end by exiting
(e.g. reaching an `EXIT`, or its own `JUMP`) — otherwise execution will just
fall through into whatever comes after it, including the matching `LANDING`.

- If the condition is **true**, the `JUMP` on the next line is skipped, and
  execution falls into the block immediately following it.
- If the condition is **false**, execution lands on the `JUMP`, which sends
  it to the matching `LANDING n`.

Example:

```
PUSH 3
IF_GREATER_THAN 1
JUMP 1
PUSH 404      # only runs if 3 > 1 is true
LANDING 1
PRINT
EXIT
```

This pairing is a manual convention for now, not something the VM enforces
— an `IF_GREATER_THAN` without a `JUMP` immediately after it will not behave
as a conditional.

## Example

`add.vm`:

```
PUSH 10
PUSH 6
POP

PUSH 6

ADD
PRINT
```

Running `python vm.py add.vm` prints `16`.

## Error Handling

Errors are strict by design: an unrecognized instruction, an operation
attempted on an empty stack (e.g. `ADD` with fewer than two values pushed),
or a `JUMP` with no matching `LANDING`, raises an exception with a message
describing the problem, rather than failing silently or skipping the bad
instruction.

## Status

Actively in development. Not yet implemented, planned next:

- `MUL`, `DIV`
- Variables (`STORE` / `LOAD`)
- Additional comparisons (`EQ`, `LT`, `GREATER_THAN` variants beyond the
  current one)
- Enforcing the `IF_GREATER_THAN` + `JUMP` pairing at parse time, instead of
  relying on the programmer to follow the convention correctly
