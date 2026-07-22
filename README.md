# Bytecode VM

A small stack-based virtual machine, written in Python, that reads a program
written in a custom instruction set from a `.vm` text file and executes it.

Built to understand how real interpreters (Python's own, the JVM) work
under the hood.

## How it works

1. A `.vm` file is read from disk, one instruction per line.
2. Each line is parsed into a tuple, e.g. `PUSH 5` becomes `("PUSH", 5)`.
3. A `while` loop, driven by a program counter, executes each instruction
   in order against an internal stack and a dictionary of named variables.

Dispatch, for both parsing and execution, is done through dictionaries
mapping opcode strings to handler functions, rather than an if/elif chain.

## Usage

```
python vm.py path/to/program.vm
```

## Instruction Set (current)

| Instruction         | Effect                                                     |
| ------------------- | ---------------------------------------------------------- |
| `PUSH n`            | Push integer `n` onto the stack                            |
| `POP`               | Remove the top value from the stack                        |
| `ADD`               | Pop two values, push their sum                             |
| `SUB`               | Pop two values, push first-pushed minus second-pushed      |
| `MOD`               | Pop two values, push first-pushed modulo second-pushed     |
| `PRINT`             | Print the current top of the stack (does not remove it)    |
| `STORE name`        | Pop the top of the stack, save it under `name`             |
| `LOAD name`         | Push the value currently saved under `name` onto the stack |
| `IF_GREATER_THAN n` | Pop top of stack; see Control Flow below                   |
| `IF_LESS_THAN n`    | Pop top of stack; see Control Flow below                   |
| `IF_EQUAL n`        | Pop top of stack; see Control Flow below                   |
| `JUMP n`            | Jump execution to the matching `LANDING n`                 |
| `LANDING n`         | A named jump target; no effect on its own                  |
| `EXIT`              | Immediately end program execution                          |

## Control Flow

Every `IF_*` instruction is always paired with a `JUMP` on the very next
line, and the block that follows the pair must end by exiting (e.g. reaching
an `EXIT`, another `JUMP`, or falling into a subsequent block deliberately)
— otherwise execution will just fall through into whatever comes after it,
including the matching `LANDING`.

- If the condition is **true**, the `JUMP` on the next line is skipped, and
  execution falls into the block immediately following it.
- If the condition is **false**, execution lands on the `JUMP`, which sends
  it to the matching `LANDING n`.

`IF_*` instructions pop the value they compare, rather than peeking — the
comparison consumes it, matching how `ADD`/`SUB`/`MOD` also consume their
operands. This keeps the stack from silently accumulating leftover values
across loop iterations.

This pairing is a manual convention for now, not something the VM enforces
— an `IF_*` instruction without a `JUMP` immediately after it will not
behave as a conditional.

## Example: FizzBuzz

The VM can run a full FizzBuzz (1–15) using a loop built from `STORE`/`LOAD`
for the counter, `MOD` for divisibility checks, and `IF_EQUAL`/`JUMP`/
`LANDING` for branching — see `fizzbuzz.vm` in this repo for the full
program. It correctly prints 1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz,
11, Fizz, 13, 14, then both Fizz and Buzz for 15.

## Simple Example

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
a `LOAD` of a variable that was never `STORE`d, or a `JUMP` with no matching
`LANDING`, raises an exception with a message describing the problem, rather
than failing silently or skipping the bad instruction.

## Status

Core interpreter is functional: arithmetic, comparisons, variables, and
jump-based control flow all work, and the VM can run a full FizzBuzz
program correctly. This satisfies the original v1 success criteria.

Known rough edges / not yet done:

- Some execution handlers still print internal debug output (e.g.
  `Storing ...`, `Testing: Just prints the top of stack -> ...`) rather
  than clean, final-output-only printing — needs cleanup.
- `MUL`, `DIV` not yet implemented
- No automated tests yet (planned: `pytest`, at least one test per
  instruction)
- The `IF_*` + `JUMP` pairing convention is not enforced by the parser —
  a malformed pairing currently just produces wrong behavior, not an error
- `JUMP`/`LANDING` resolution is a linear scan through the whole program
  every time a jump executes, rather than resolved once during parsing
