import tkinter as tk
from tkinter import messagebox
import ast
import operator
import re


# ============================================================
# CALCOLO SICURO
# ============================================================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Mod: operator.mod
}


def safe_eval(expression):
    """
    Valuta un'espressione matematica in modo controllato.
    Non utilizza eval() direttamente.
    """

    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")
    expression = expression.replace("^", "**")

    try:
        tree = ast.parse(expression, mode="eval")
        return evaluate_node(tree.body)

    except ZeroDivisionError:
        raise

    except Exception:
        raise ValueError("Espressione non valida")


def evaluate_node(node):

    # --------------------------------------------------------
    # Numero
    # --------------------------------------------------------

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

    # --------------------------------------------------------
    # Operazione binaria
    # --------------------------------------------------------

    if isinstance(node, ast.BinOp):

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        operator_type = type(node.op)

        if operator_type not in OPERATORS:
            raise ValueError()

        # Limite dell'esponente
        if operator_type == ast.Pow:

            if abs(right) > 1000:
                raise ValueError(
                    "Esponente troppo grande."
                )

        return OPERATORS[operator_type](left, right)

    # --------------------------------------------------------
    # +numero / -numero
    # --------------------------------------------------------

    if isinstance(node, ast.UnaryOp):

        operator_type = type(node.op)

        if operator_type not in OPERATORS:
            raise ValueError()

        return OPERATORS[operator_type](
            evaluate_node(node.operand)
        )

    raise ValueError()


# ============================================================
# FORMATTAZIONE ITALIANA
# ============================================================

def format_number_italian(number):
    """
    Converte un numero nel formato italiano.

    Esempi:
        1000000      -> 1.000.000
        3140.5       -> 3.140,5
        -2500000.75  -> -2.500.000,75
    """

    number = str(number)

    # Gestione del segno
    sign = ""

    if number.startswith("-"):
        sign = "-"
        number = number[1:]

    # Separazione parte intera e decimale
    if "." in number:

        integer_part, decimal_part = number.split(".", 1)

    else:

        integer_part = number
        decimal_part = None

    # Separatore delle migliaia
    if len(integer_part) > 3:

        groups = []

        while len(integer_part) > 3:

            groups.insert(
                0,
                integer_part[-3:]
            )

            integer_part = integer_part[:-3]

        groups.insert(
            0,
            integer_part
        )

        integer_part = ".".join(groups)

    # Parte decimale
    if decimal_part is not None:

        return (
            sign
            + integer_part
            + ","
            + decimal_part
        )

    return sign + integer_part


def format_expression_italian(expression):
    """
    Formatta i numeri presenti nell'espressione
    usando la notazione italiana.

    Esempi:

        1000000       -> 1.000.000
        3.            -> 3,
        3.14          -> 3,14
        1000000+3.14  -> 1.000.000+3,14
    """

    def replace_number(match):

        number = match.group(0)

        return format_number_italian(number)

    # IMPORTANTE:
    # \d* permette anche zero cifre dopo il punto.
    #
    # Quindi:
    # 3.   viene riconosciuto
    # 3.14 viene riconosciuto

    return re.sub(
        r"-?\d+(?:\.\d*)?",
        replace_number,
        expression
    )


# ============================================================
# APPLICAZIONE
# ============================================================

class CalculatorApp:

    def __init__(self, root):

        self.root = root

        # ----------------------------------------------------
        # Finestra
        # ----------------------------------------------------

        self.root.title("Calcolatrice")

        self.root.geometry("460x700")
        self.root.minsize(400, 600)

        self.root.configure(
            bg="#121212"
        )

        # ----------------------------------------------------
        # Variabili
        # ----------------------------------------------------

        # Espressione interna.
        #
        # Esempi:
        # 3.14
        # 1000000
        # 1000000+3.14

        self.expression = ""

        self.result_shown = False

        self.history_visible = False

        # ----------------------------------------------------
        # Interfaccia
        # ----------------------------------------------------

        self.create_ui()

        # ----------------------------------------------------
        # Tastiera
        # ----------------------------------------------------

        self.bind_keyboard()

    # ========================================================
    # INTERFACCIA
    # ========================================================

    def create_ui(self):

        # ====================================================
        # HEADER
        # ====================================================

        header = tk.Frame(
            self.root,
            bg="#121212"
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(20, 0)
        )

        # ----------------------------------------------------
        # Contenitore titolo
        # ----------------------------------------------------

        title_container = tk.Frame(
            header,
            bg="#121212"
        )

        title_container.pack(
            side="left"
        )

        # Titolo
        title = tk.Label(
            title_container,
            text="Calcolatrice",
            font=("Segoe UI", 20, "bold"),
            fg="#ffffff",
            bg="#121212"
        )

        title.pack(
            anchor="w"
        )

        # Sottotitolo
        subtitle = tk.Label(
            title_container,
            text="Calcoli semplici. Risultati immediati.",
            font=("Segoe UI", 9),
            fg="#888888",
            bg="#121212"
        )

        subtitle.pack(
            anchor="w",
            pady=(2, 0)
        )

        # ----------------------------------------------------
        # Pulsante cronologia
        # ----------------------------------------------------

        self.history_button = tk.Button(
            header,
            text="🕘",
            font=("Segoe UI Emoji", 14),
            fg="#ffffff",
            bg="#1e1e1e",
            activebackground="#333333",
            activeforeground="#ffffff",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.toggle_history
        )

        self.history_button.pack(
            side="right",
            ipadx=8,
            ipady=5
        )

        # ====================================================
        # DISPLAY
        # ====================================================

        display_frame = tk.Frame(
            self.root,
            bg="#121212"
        )

        display_frame.pack(
            fill="x",
            padx=25,
            pady=(25, 15)
        )

        display_background = tk.Frame(
            display_frame,
            bg="#1e1e1e"
        )

        display_background.pack(
            fill="x"
        )

        self.display = tk.Label(
            display_background,
            text="",
            font=("Segoe UI", 34, "bold"),
            fg="#ffffff",
            bg="#1e1e1e",
            anchor="e",
            padx=15,
            pady=18
        )

        self.display.pack(
            fill="x"
        )

        # ====================================================
        # CRONOLOGIA
        # ====================================================

        self.history_frame = tk.Frame(
            self.root,
            bg="#121212"
        )

        history_title_frame = tk.Frame(
            self.history_frame,
            bg="#121212"
        )

        history_title_frame.pack(
            fill="x"
        )

        history_label = tk.Label(
            history_title_frame,
            text="Cronologia",
            font=("Segoe UI", 10, "bold"),
            fg="#888888",
            bg="#121212"
        )

        history_label.pack(
            side="left"
        )

        clear_history_button = tk.Button(
            history_title_frame,
            text="Cancella",
            font=("Segoe UI", 9),
            fg="#999999",
            bg="#121212",
            activebackground="#121212",
            activeforeground="#ffffff",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.clear_history
        )

        clear_history_button.pack(
            side="right"
        )

        self.history = tk.Listbox(
            self.history_frame,
            height=6,
            bg="#181818",
            fg="#dddddd",
            bd=0,
            highlightthickness=0,
            font=("Segoe UI", 10),
            selectbackground="#333333",
            activestyle="none"
        )

        self.history.pack(
            fill="both",
            expand=True,
            pady=(5, 15)
        )

        # ====================================================
        # PULSANTI
        # ====================================================

        buttons_frame = tk.Frame(
            self.root,
            bg="#121212"
        )

        buttons_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        buttons = [
            ["C", "⌫", "(", ")"],
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "-"],
            ["±", "0", ",", "+"],
            ["%", "xʸ", "="]
        ]

        # ====================================================
        # CREAZIONE PULSANTI
        # ====================================================

        for row, values in enumerate(buttons):

            col = 0

            for value in values:

                # -------------------------------------------
                # Colore
                # -------------------------------------------

                if value == "=":

                    color = "#4c8bf5"

                elif value in [
                    "÷",
                    "×",
                    "-",
                    "+",
                    "%",
                    "xʸ"
                ]:

                    color = "#2b2b2b"

                elif value in [
                    "C",
                    "⌫"
                ]:

                    color = "#3a1f1f"

                else:

                    color = "#202020"

                # -------------------------------------------
                # Larghezza
                # -------------------------------------------

                colspan = 1

                if value == "=":
                    colspan = 2

                # -------------------------------------------
                # Pulsante
                # -------------------------------------------

                button = tk.Button(
                    buttons_frame,
                    text=value,
                    font=("Segoe UI", 16, "bold"),
                    fg="#ffffff",
                    bg=color,
                    activebackground="#444444",
                    activeforeground="#ffffff",
                    bd=0,
                    relief="flat",
                    cursor="hand2",
                    command=lambda v=value:
                    self.button_click(v)
                )

                button.grid(
                    row=row,
                    column=col,
                    columnspan=colspan,
                    sticky="nsew",
                    padx=4,
                    pady=4,
                    ipady=13
                )

                col += colspan

        # ====================================================
        # DIMENSIONAMENTO
        # ====================================================

        for i in range(4):

            buttons_frame.columnconfigure(
                i,
                weight=1,
                uniform="buttons"
            )

        for i in range(len(buttons)):

            buttons_frame.rowconfigure(
                i,
                weight=1
            )

    # ========================================================
    # CRONOLOGIA
    # ========================================================

    def toggle_history(self):

        if self.history_visible:

            self.history_frame.pack_forget()

            self.history_visible = False

        else:

            self.history_frame.pack(
                fill="both",
                expand=True,
                padx=25,
                before=self.root.winfo_children()[-1]
            )

            self.history_visible = True

    def clear_history(self):

        self.history.delete(
            0,
            tk.END
        )

    # ========================================================
    # DISPLAY
    # ========================================================

    def update_display(self):

        formatted_expression = (
            format_expression_italian(
                self.expression
            )
        )

        self.display.config(
            text=formatted_expression
        )

    # ========================================================
    # GESTIONE PULSANTI
    # ========================================================

    def button_click(self, value):

        # ----------------------------------------------------
        # Cancella tutto
        # ----------------------------------------------------

        if value == "C":

            self.clear()

            return

        # ----------------------------------------------------
        # Backspace
        # ----------------------------------------------------

        if value == "⌫":

            self.delete_last()

            return

        # ----------------------------------------------------
        # Calcolo
        # ----------------------------------------------------

        if value == "=":

            self.calculate()

            return

        # ----------------------------------------------------
        # Percentuale
        # ----------------------------------------------------

        if value == "%":

            self.percent()

            return

        # ----------------------------------------------------
        # Esponente
        # ----------------------------------------------------

        if value == "xʸ":

            self.add_operator("^")

            return

        # ----------------------------------------------------
        # Cambio segno
        # ----------------------------------------------------

        if value == "±":

            self.change_sign()

            return

        # ----------------------------------------------------
        # Separatore decimale
        # ----------------------------------------------------

        if value == ",":

            self.add_decimal()

            return

        # ----------------------------------------------------
        # Dopo un risultato
        # ----------------------------------------------------

        if self.result_shown:

            if value in [
                "+",
                "-",
                "×",
                "÷",
                "^"
            ]:

                self.result_shown = False

            else:

                self.expression = ""

                self.result_shown = False

        # ----------------------------------------------------
        # Aggiungi carattere
        # ----------------------------------------------------

        self.expression += value

        self.update_display()

    # ========================================================
    # NUMERO DECIMALE
    # ========================================================

    def add_decimal(self):

        # Trova il numero corrente
        current_number = re.split(
            r"[+\-×÷^()]",
            self.expression
        )[-1]

        # Evita due separatori decimali
        if "." in current_number:
            return

        # Se siamo all'inizio o dopo un operatore,
        # inseriamo 0.
        #
        # Internamente:
        # 0.
        #
        # Visivamente:
        # 0,

        if not current_number:

            self.expression += "0."

        else:

            self.expression += "."

        self.update_display()

    # ========================================================
    # OPERATORI
    # ========================================================

    def add_operator(self, operator_symbol):

        if not self.expression:
            return

        # Evita due operatori consecutivi
        if self.expression[-1] in "+-×÷^":

            self.expression = (
                self.expression[:-1]
                + operator_symbol
            )

        else:

            self.expression += operator_symbol

        self.result_shown = False

        self.update_display()

    # ========================================================
    # CALCOLO
    # ========================================================

    def calculate(self):

        if not self.expression:
            return

        try:

            result = safe_eval(
                self.expression
            )

            # ------------------------------------------------
            # Evita 10.0 e mostra 10
            # ------------------------------------------------

            if (
                isinstance(result, float)
                and result.is_integer()
            ):

                result = int(result)

            # ------------------------------------------------
            # Cronologia
            # ------------------------------------------------

            expression_display = (
                format_expression_italian(
                    self.expression
                )
            )

            result_display = (
                format_number_italian(
                    result
                )
            )

            history_entry = (
                f"{expression_display} = "
                f"{result_display}"
            )

            self.history.insert(
                0,
                history_entry
            )

            if self.history.size() > 20:

                self.history.delete(20)

            # ------------------------------------------------
            # Risultato
            # ------------------------------------------------

            self.expression = str(result)

            self.update_display()

            self.result_shown = True

        except ZeroDivisionError:

            self.show_error(
                "Non puoi dividere per zero."
            )

        except Exception:

            self.show_error(
                "Espressione non valida."
            )

    # ========================================================
    # PERCENTUALE
    # ========================================================

    def percent(self):

        if not self.expression:
            return

        try:

            result = safe_eval(
                self.expression
            )

            result = result / 100

            self.expression = str(result)

            self.update_display()

        except Exception:

            self.show_error(
                "Percentuale non valida."
            )

    # ========================================================
    # CAMBIO SEGNO
    # ========================================================

    def change_sign(self):

        if not self.expression:
            return

        try:

            result = safe_eval(
                self.expression
            )

            result = -result

            self.expression = str(result)

            self.update_display()

        except Exception:

            self.show_error(
                "Operazione non valida."
            )

    # ========================================================
    # CANCELLA TUTTO
    # ========================================================

    def clear(self):

        self.expression = ""

        self.result_shown = False

        self.update_display()

    # ========================================================
    # BACKSPACE
    # ========================================================

    def delete_last(self):

        if self.expression:

            self.expression = (
                self.expression[:-1]
            )

        self.update_display()

    # ========================================================
    # ERRORI
    # ========================================================

    def show_error(self, message):

        messagebox.showerror(
            "Errore",
            message
        )

        self.clear()

    # ========================================================
    # TASTIERA
    # ========================================================

    def bind_keyboard(self):

        self.root.bind_all(
            "<KeyPress>",
            self.keyboard_event
        )

    def keyboard_event(self, event):

        key = event.keysym
        char = event.char
        keycode = event.keycode

        # ====================================================
        # TASTIERINO NUMERICO WINDOWS
        # ====================================================
        #
        # 96  = 0
        # 97  = 1
        # 98  = 2
        # 99  = 3
        # 100 = 4
        # 101 = 5
        # 102 = 6
        # 103 = 7
        # 104 = 8
        # 105 = 9
        #
        # Funziona con Bloc Num attivo e disattivo.
        #
        # ====================================================

        keypad_numbers = {
            96: "0",
            97: "1",
            98: "2",
            99: "3",
            100: "4",
            101: "5",
            102: "6",
            103: "7",
            104: "8",
            105: "9"
        }

        if keycode in keypad_numbers:

            self.button_click(
                keypad_numbers[keycode]
            )

            return "break"

        # ====================================================
        # INVIO
        # ====================================================

        if key in (
            "Return",
            "KP_Enter"
        ):

            self.calculate()

            return "break"

        # ====================================================
        # BACKSPACE
        # ====================================================

        if key == "BackSpace":

            self.delete_last()

            return "break"

        # ====================================================
        # ESC
        # ====================================================

        if key == "Escape":

            self.clear()

            return "break"

        # ====================================================
        # NUMERI TASTIERA NORMALE
        # ====================================================

        if char in "0123456789":

            self.button_click(char)

            return "break"

        # ====================================================
        # DECIMALE
        # ====================================================

        if (
            char in ".,"
            or key == "KP_Decimal"
            or key == "Delete"
            or key == "KP_Delete"
        ):

            self.button_click(",")

            return "break"

        # ====================================================
        # SOMMA
        # ====================================================

        if (
            char == "+"
            or key == "KP_Add"
        ):

            self.button_click("+")

            return "break"

        # ====================================================
        # SOTTRAZIONE
        # ====================================================

        if (
            char == "-"
            or key == "KP_Subtract"
        ):

            self.button_click("-")

            return "break"

        # ====================================================
        # MOLTIPLICAZIONE
        # ====================================================

        if (
            char == "*"
            or key == "KP_Multiply"
        ):

            self.button_click("×")

            return "break"

        # ====================================================
        # DIVISIONE
        # ====================================================

        if (
            char == "/"
            or key == "KP_Divide"
        ):

            self.button_click("÷")

            return "break"

        # ====================================================
        # ESPONENTE
        # ====================================================

        if char == "^":

            self.button_click("xʸ")

            return "break"

        # ====================================================
        # PARENTESI APERTA
        # ====================================================

        if char == "(":

            self.button_click("(")

            return "break"

        # ====================================================
        # PARENTESI CHIUSA
        # ====================================================

        if char == ")":

            self.button_click(")")

            return "break"

        # ====================================================
        # PERCENTUALE
        # ====================================================

        if char == "%":

            self.button_click("%")

            return "break"


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CalculatorApp(root)

    root.mainloop()
