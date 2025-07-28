# Compiler
A basic compiler implementation for the PyScal language.

## Compiler Phases

### 1. Lexical Analysis (Tokenizer)

- Reads the entire source file and transforms it into an array of tokens
- Tokens (also called "terminal symbols") form the basic building blocks of the language
- Examples include: keywords (`if`, `else`, `for`, `while`), operators (`=`, `+`, `-`), and delimiters (`{`, `}`, `[`, `]`)

### 2. Syntax Analysis (Parser)

- Validates the syntactical structure of the token stream (output from lexical analysis)
- Constructs a parse tree based on the language grammar
- Ensures the program follows the correct syntax rules
