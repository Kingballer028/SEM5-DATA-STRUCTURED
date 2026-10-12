# ALPHA HAMIDU JALLOH ID5193 SEM5 BIT2101
## Assignment 1
# Stack-Based Arithmetic Expression Evaluator

## Purpose
This project evaluates arithmetic expressions with a stack. It reads `input.txt`
and writes results to `output.txt`.

## Files
- `main.py`: Python program.
- `input.txt`: sample expressions separated by a line of five hyphens.
- `output.txt`: sample results; the program rewrites this file each run.
- `REPORT.docx` and `REPORT.md`: detailed report.

## Requirements
Python 3.10 or newer is recommended. No extra Python packages are needed.

## Run in VS Code
1. Open this project folder using **File → Open Folder**.
2. Open `main.py`.
3. Save your files.
4. Choose **Run Python File**, or use the terminal command `python main.py`.
   On some Windows computers, use `py main.py`.
5. Open `output.txt`.

## Supported
Addition, subtraction, multiplication, division, parentheses, decimal numbers,
and unary signs such as `-6`. The program reports invalid expressions and
division by zero instead of stopping the entire file.

## How it works
1. `tokenize()` separates the expression into tokens.
2. `to_postfix()` uses an operator stack to convert infix notation to postfix.
3. `evaluate_postfix()` uses a value stack to calculate the answer.
4. `process_files()` reads input and writes output.

