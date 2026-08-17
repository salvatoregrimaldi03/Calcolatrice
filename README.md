# 🧮 Calcolatrice

A modern desktop calculator built with **Python** and **Tkinter**, designed with a clean dark interface and a focus on simplicity, usability and reliable mathematical operations.

## 👨‍💻 Author

* **Salvatore Grimaldi** - Developer

## 📌 What is it?

**Calcolatrice** is a desktop calculator application developed in Python and designed for Windows PCs.

The application provides a simple and modern graphical interface for performing common mathematical calculations while supporting both standard keyboard input and numeric keypad input.

The project was created with the goal of building a lightweight desktop application that is easy to use, maintain and extend.

### Main features

* Basic arithmetic operations (`+`, `−`, `×`, `÷`)
* Parentheses for complex expressions
* Percentage calculations
* Sign inversion (`±`)
* Arbitrary exponentiation (`xʸ`)
* Italian number formatting
* Italian decimal separator using `,`
* Thousands separator using `.`
* Keyboard support
* Numeric keypad support
* Calculation history
* Clear history functionality
* Dark desktop interface
* Safe expression evaluation without directly using `eval()`

## 🖥️ Interface

The application features a dark and minimal interface designed to keep the calculator easy to read and use.

The interface includes:

* Display for the current expression
* Calculator keyboard
* History section accessible through the history button
* Italian number formatting
* Dedicated controls for mathematical operations

## 🚀 How to try it

### Run the application

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/calculator.git
```

Navigate to the project directory:

```bash
cd calculator
```

Run the application:

```bash
python calculator.py
```

> Python 3.x is required.

## ⌨️ Keyboard support

The calculator supports both the standard keyboard and the numeric keypad.

### Standard keyboard

* `0–9` → Numbers
* `+` → Addition
* `-` → Subtraction
* `*` → Multiplication
* `/` → Division
* `,` → Decimal separator
* `^` → Exponentiation
* `(` `)` → Parentheses
* `Enter` → Calculate
* `Backspace` → Delete last character
* `Esc` → Clear

### Numeric keypad

The numeric keypad is supported for both enabled and disabled **Num Lock** states.

## 🇮🇹 Italian number formatting

The calculator uses the Italian number format for the user interface.

Examples:

```text
1000000       → 1.000.000
500000        → 500.000
3,14          → 3,14
1500000,50    → 1.500.000,50
```

Internally, Python continues to use the standard `.` decimal separator for calculations.

## 🧠 Safe expression evaluation

Mathematical expressions are evaluated using Python's `ast` module and a controlled set of operators.

The application does **not** directly rely on Python's `eval()` function to evaluate user input.

This allows the calculator to support mathematical expressions while restricting the operations that can be executed.

## 🛠️ Built With

* [Python](https://www.python.org/) - Programming language
* [Tkinter](https://docs.python.org/3/library/tkinter.html) - Desktop graphical user interface
* [AST](https://docs.python.org/3/library/ast.html) - Controlled mathematical expression parsing

## 📁 Project Structure

```text
calculator/
│
├── calculator.py
├── README.md
└── LICENSE
```

> The project structure may evolve as new features and improvements are introduced.

## 🤝 Contributing

Contributions and improvements are welcome.

If you want to propose a bug fix, new feature or improvement, please open an **Issue** before starting major changes.

All external contributions must be submitted through a **Pull Request**.

The `main` branch is protected to keep the stable version of the project under control.

### Contribution workflow

```text
Fork the repository
        ↓
Create a branch
        ↓
Make your changes
        ↓
Test the application
        ↓
Open a Pull Request
        ↓
Review
        ↓
Merge
```

Please keep Pull Requests focused and clearly describe the changes that have been made.

## 📋 Roadmap

Possible future improvements include:

* Scientific calculator mode
* Memory functions (`MC`, `MR`, `M+`, `M−`)
* Additional mathematical functions
* Improved history panel
* Custom themes
* Application settings
* Windows executable distribution
* Automated tests
* Additional accessibility improvements

## 📌 Project Status

**Finished (open to improvements and suggestions)**

The project is actively being improved and new features may be introduced over time.
