import tkinter as tk
from tkinter import scrolledtext
import sys
import threading

from io import StringIO
from var import parse_tree_root, print_parse_tree
import redef as rd

string = ""
code = {}


class StdRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, string)
        self.widget.configure(state='disabled')
        self.widget.see(tk.END)

    def flush(self):
        pass  # Not needed for Tkinter text widget


class CustomInput:
    def __init__(self, parent):
        self.parent = parent
        self.input_value = ""
        self.input_ready = threading.Event()

    def prompt(self, prompt_text=""):
        self.parent.output_text.configure(state='normal')
        self.parent.output_text.insert(tk.END, prompt_text)
        self.parent.output_text.see(tk.END)
        self.parent.output_text.configure(state='disabled')
        self.parent.input_text.set("")
        self.parent.input_entry.pack()
        self.parent.input_button.pack()
        self.input_ready.clear()

    def get_input(self, prompt_text=""):
        self.prompt(prompt_text)
        self.input_ready.wait()  # Wait until input is submitted
        self.parent.input_entry.pack_forget()
        self.parent.input_button.pack_forget()
        self.parent.output_text.configure(state='normal')
        self.parent.output_text.insert(
            tk.END, self.input_value + "\n"
        )  # Display the entered input
        self.parent.output_text.see(tk.END)
        self.parent.output_text.configure(state='disabled')
        return self.input_value

    def submit_input(self):
        self.input_value = self.parent.input_text.get()
        self.input_ready.set()  # Signal that input is ready


class OutputWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Output Window")
        self.geometry("800x600")

        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.output_text.pack(expand=True, fill=tk.BOTH)

        self.input_text = tk.StringVar()
        self.input_entry = tk.Entry(self, textvariable=self.input_text)
        self.input_button = tk.Button(self, text="Submit", command=self.submit_input)

        self.custom_input = CustomInput(self)

    def submit_input(self):
        self.custom_input.submit_input()


def generate(self, input_lines, output_instance):
    code = generate_python_code(parse_tree_root)
    code += "garden()\n"

    output_window = OutputWindow(self)

    output_window.output_text.delete("1.0", tk.END)

    # Redirect stdout and stdin
    sys.stdout = StdRedirector(output_window.output_text)
    sys.stdin = output_window.custom_input

    def run_code():
        try:
            exec(code, {"input": output_window.custom_input.get_input})
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Restore stdout and stdin
            sys.stdout = sys.__stdout__
            sys.stdin = sys.__stdin__

    # Run the code in a separate thread to avoid blocking the main thread
    threading.Thread(target=run_code).start()


def generate_python_code(node):
    indent = "    " * node.level  # Adjust indentation based on the node's level
    if node.symbol in [
        "seed",
        "plant",
    ]:  # Skip generating code for "seed" and "plant" nodes
        return ""
    elif node.kind is not None:
        if node.symbol == "<statement>":
            var = ""
            if node.kind == "variable":
                for variable in node.children:
                    if variable.kind == rd.ID:
                        var = variable.symbol[1:] + ":" + node.type
                        if variable.children:
                            var += "="
                            for child in variable.children:
                                var += child.symbol
                return f"{indent}{var}\n"

            if node.kind == "i/o":
                _is_print = False
                data = None
                for child in node.children:
                    if child.symbol == "mint":
                        _is_print = True
                        continue
                    if child.kind == "data" or child.kind == rd.ID:
                        data = child.symbol.replace("#", "")
                        if child.type == "string literal":
                            data = f"f{data}"
                    if child.kind == rd.ID:
                        var += child.symbol[1:]
                if _is_print:
                    return f"{indent}print({data})\n"
                else:
                    return f"{indent}{var}:{node.type} = input({data})\n"
            if node.kind == "if":
                if_stmt = ""
                con = ""
                for child in node.children:
                    print(child)
                    if child.symbol == "leaf":
                        for condition in child.children[0].children:
                            if condition.kind == rd.ID:
                                con = condition.symbol.replace("#", "")
                                continue
                            if condition.type == "tint literal":
                                con += str(condition.symbol)
                                continue
                            con += condition.symbol
                        if_stmt += f"{indent}if {con}:\n" + generate_python_code(
                            child.children[1]
                        )
                    elif child.symbol == "eleaf":
                        for condition in child.children[0].children:
                            if condition.kind == rd.ID:
                                con = condition.symbol.replace("#", "")
                                continue
                            if condition.type == "tint literal":
                                con += str(condition.symbol)
                                continue
                            con += condition.symbol
                        if_stmt += f"{indent}elif {con}:\n" + generate_python_code(
                            child.children[1]
                        )
                    elif child.symbol == "moss":
                        if_stmt += f"{indent}else:\n" + generate_python_code(
                            child.children[0]
                        )

                return if_stmt

            if node.kind == "iterative":
                print("test")
                con_stmt = ""
                var = ""
                for child in node.children:
                    print(child)
                    if child.symbol == "fern":
                        condition = child.children[0].children
                        var = condition[1].symbol.replace("#", "")
                        start = condition[3].symbol
                        end = condition[7].symbol
                        seq = condition[11].symbol

                        con_stmt += (
                            f"{indent}for {var} in range({start}, {end}, {seq}):\n"
                            + generate_python_code(child.children[1])
                        )
                    if child.symbol == "willow":
                        # while loop
                        condition = child.children[0].children
                        con = ""
                        con += condition[0].symbol.replace("#", "")
                        con += condition[1].symbol
                        con += condition[2].symbol

                        for new_child in child.children:
                            if new_child.symbol == "<statement>":
                                con_stmt += (
                                    f"{indent}while({con}):\n"
                                    + generate_python_code(new_child)
                                )

                return con_stmt

            if node.kind == "assignment":
                var = ""
                for child in node.children:
                    if child.kind == rd.ID:
                        var = child.symbol.replace("#", "")
                    if child.kind == "data":
                        data = child.symbol
                return f"{indent}{var} = {data}\n"

    else:
        code = (
            f"{indent}def {node.symbol}():\n"
            if node.symbol[1:] != "<" and node.symbol[-1] != ">"
            else f"#{node.symbol}\n"
        )
        for child in node.children:
            code += generate_python_code(child)
        return code
