import tkinter as tk
from tkinter import scrolledtext
import sys
import threading

from var import ParseTreeNode, parse_tree_root
from semantic_analyzer import symbol_table
import redef


translate = {
    "tint": "int",
    "flora": "float",
    "chard": "char",
    "string": "str",
    "bloom": "bool",
    "fern": "for",
    "willow": "while",
}

string = ""
indent = "    "


class StdRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, string)
        self.widget.configure(state="disabled")
        self.widget.see(tk.END)

    def flush(self):
        pass  # Not needed for Tkinter text widget


class CustomInput:
    def __init__(self, parent):
        self.parent = parent
        self.input_value = ""
        self.input_ready = threading.Event()

    def prompt(self, prompt_text=""):
        self.parent.output_text.configure(state="normal")
        self.parent.output_text.insert(tk.END, prompt_text)
        self.parent.output_text.see(tk.END)
        self.parent.output_text.configure(state="disabled")
        self.parent.input_text.set("")
        self.parent.input_frame.pack(expand=True, fill=tk.X)
        self.input_ready.clear()

    def get_input(self, prompt_text=""):
        self.prompt(prompt_text)
        self.input_ready.wait()  # Wait until input is submitted
        self.parent.input_frame.pack_forget()
        self.parent.output_text.configure(state="normal")
        self.parent.output_text.insert(
            tk.END, self.input_value + "\n"
        )  # Display the entered input
        self.parent.output_text.see(tk.END)
        self.parent.output_text.configure(state="disabled")
        return self.input_value

    def submit_input(self):
        self.input_value = self.parent.input_text.get()
        self.input_ready.set()  # Signal that input is ready


class OutputWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Output Window")
        self.geometry("800x600")

        self.output_text = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, bg="black", fg="white"
        )
        self.output_text.pack(expand=True, fill=tk.BOTH)

        # Input Frame
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(fill=tk.X, pady=5)

        self.input_text = tk.StringVar()
        self.input_entry = tk.Entry(self.input_frame, textvariable=self.input_text)
        self.input_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.input_button = tk.Button(
            self.input_frame, text="Enter", command=self.submit_input
        )
        self.input_button.pack(side=tk.RIGHT)

        self.input_frame.pack_forget()
        self.custom_input = CustomInput(self)

    def submit_input(self):
        self.custom_input.submit_input()


def to_python_code(node: ParseTreeNode, stmt="") -> str:

    if node.symbol == "<program>":
        for child in node.children:
            stmt += to_python_code(child)

    elif node.symbol in ["garden", "<body>"]:
        stmt += "def garden():\n" if node.symbol == "garden" else ""

        for child in node.children:
            stmt += to_python_code(child)

        if node.symbol == "garden":
            stmt += indent + "pass\n"

    elif node.symbol == "<statement>":

        if node.kind in ["variable", "assignment"]:

            # Initialize or update the variable
            prev_var_node: ParseTreeNode = None
            for var_node in node.children:

                if var_node.symbol == "<argument>":
                    stmt += (
                        indent * prev_var_node.level
                        + prev_var_node.symbol[1:]
                        + to_python_code(var_node)
                        + "\n"
                    )
                    continue

                var_name = var_node.symbol[1:]
                type_cast = translate[var_node.type] if var_node.type else None
                var_op = (
                    node.properties["assignment-op"]
                    if "assignment-op" in node.properties
                    else None
                )

                if symbol_table[var_name] if var_name in symbol_table else None:
                    prev_var_node = var_node
                    continue

                # Set the value of the variable if any
                tmp_val = ""
                for val in var_node.children:
                    if val.symbol in ["<sqnc>", "<index>", "<argument>"]:
                        tmp_val += to_python_code(val)
                        continue
                    tmp_val += val.symbol[1:] if val.kind == redef.ID else val.symbol
                var_val = tmp_val

                # Add the type to the variable if any
                var_val = type_cast + "(" + var_val + ")" if type_cast else var_val

                stmt += (
                    indent * node.level
                    + f"{var_name} {var_op if var_op else '='} {var_val}\n"
                )

        elif node.kind == "i/o":

            if len(node.children) > 2 and node.children[1].symbol == "inpetal":
                var_name = node.children[0].symbol[1:]
                var_type = translate[node.type] if node.type in translate else None
                input_str = node.children[2].symbol

                stmt += (
                    indent * node.level
                    + f"{var_name} = {var_type}(input({input_str}))\n"
                )

            else:

                output_str = ""
                for data in node.children:
                    if data.symbol in ["<sqnc>", "<index>", "<argument>"]:
                        output_str += to_python_code(data)
                        continue
                    elif data.type == redef.STR_LIT:
                        open_braces = data.symbol.count("{")
                        tmp_str = data.symbol.replace("{#", "{")
                        close_braces = data.symbol.count("}")
                        is_formatted = open_braces == close_braces and (
                            open_braces > 0 and close_braces > 0
                        )
                        output_str += "f" + tmp_str if is_formatted else tmp_str
                        continue
                    output_str += (
                        data.symbol[1:] if data.kind == redef.ID else data.symbol
                    )
                stmt += indent * node.level + f"print({output_str})\n"

        elif node.kind == "if":

            is_if = True
            for con_node in node.children:
                # Get the body of the con statement
                if_body = to_python_code(con_node.children[0])

                if con_node.symbol in ["leaf", "eleaf"]:

                    if_con = con_node.children[1]

                    # Get the condition
                    tmp_con = ""
                    for val in if_con.children:
                        if val.symbol == "<sqnc>":
                            tmp_con += to_python_code(val)
                            continue
                        elif val.symbol == "<index>":
                            tmp_con += to_python_code(val)
                            continue
                        tmp_con += (
                            val.symbol[1:] if val.kind == redef.ID else val.symbol
                        )
                    if_con = tmp_con

                    con = "if" if is_if else "elif"
                    stmt += indent * node.level + f"{con} {if_con}:\n{if_body}"

                    # Make sure that the next loop is an elif
                    is_if = False

                else:
                    stmt += indent * node.level + "else:\n"
                    stmt += if_body

        elif node.kind == "iterative":

            iter_node = node.children[0]
            iter_type = iter_node.symbol
            iter_body = to_python_code(iter_node.children[0])
            iter_con = iter_node.children[1]

            if iter_type == "fern":
                if iter_con.children[1].symbol == "at":
                    iter_v1 = iter_con.children[0].symbol[1:]
                    iter_v2 = iter_con.children[2].symbol[1:]

                    iter_con = f"for {iter_v1} in {iter_v2}:\n"
                    stmt += indent * node.level + iter_con
                    stmt += iter_body

                else:
                    iter_v1_type = translate[iter_con.children[0].symbol]
                    iter_v1_name = iter_con.children[1].symbol[1:]
                    iter_v1_val = iter_con.children[3].symbol

                    iter_op = iter_con.children[5].symbol

                    iter_con_val = (
                        iter_con.children[6].symbol[1:]
                        if iter_con.children[6].symbol[0] == "#"
                        else iter_con.children[6].symbol
                    )
                    iter_step = iter_con.children[8].symbol

                    stmt += (
                        indent * node.level
                        + f"{iter_v1_name}: {iter_v1_type} = {iter_v1_val}\n"
                    )
                    stmt += (
                        indent * node.level
                        + f"while {iter_v1_name} {iter_op} {iter_con_val}:\n"
                    )
                    stmt += iter_body
                    stmt += (
                        indent * iter_node.children[0].children[0].level
                        + f"{iter_v1_name} {iter_con.properties['assignment-op']} {iter_step}\n"
                    )
            else:
                iter_v1 = (
                    iter_con.children[0].symbol[1:]
                    if iter_con.children[0].kind == redef.ID
                    else iter_con.children[0].symbol
                )
                iter_op = iter_con.children[1].symbol
                iter_v2 = (
                    iter_con.children[2].symbol[1:]
                    if iter_con.children[2].kind == redef.ID
                    else iter_con.children[2].symbol
                )

                iter_con = f"while {iter_v1} {iter_op} {iter_v2}:\n"
                stmt += indent * node.level + iter_con
                stmt += iter_body

        elif node.kind == "tree":
            tree_con_var = node.children[0].children[0]
            tree_var = (
                tree_con_var.symbol[1:]
                if tree_con_var.kind == redef.ID
                else tree_con_var.symbol
            )

            tree_con = indent * node.level + f"match {tree_var}:\n"
            tree_body = ""

            for branch in node.children[0].children[1:]:
                tree_body += (
                    indent * (node.level + 1) + f"case {branch.children[0].symbol}:\n"
                )
                tree_body += indent * (node.level + 2) + "while True:\n"
                for stmt_nodes in branch.children[1:]:
                    tree_body += indent + to_python_code(stmt_nodes)

            stmt += tree_con + tree_body

        elif node.kind == "regrow":
            # Set the value of the variable if any
            tmp_val = ""
            for val in node.children:
                if val.symbol in ["<sqnc>", "<index>", "<argument>"]:
                    tmp_val += to_python_code(val)
                    continue
                tmp_val += val.symbol[1:] if val.kind == redef.ID else val.symbol
            var_val = tmp_val

            stmt += indent * node.level + f"return {var_val}\n"

        elif node.kind == "break":
            stmt += indent * node.level + "break\n"

    elif node.symbol == "<function>":
        func_name = node.children[0].symbol[1:]
        func_params = to_python_code(node.children[1])
        func_body = to_python_code(node.children[2])

        stmt += f"def {func_name}({func_params}):\n{func_body}"
        stmt += indent + "pass\n"

    elif node.symbol == "<index>":
        stmt += "["

        for val in node.children:
            stmt += val.symbol[1:] if val.kind == redef.ID else val.symbol

        stmt += "]"

    elif node.symbol == "<sqnc>":
        var_val: str = ""
        var_val_lst: list = []

        for val in node.children:
            if val.symbol == "<sqnc>":
                var_val += to_python_code(val)
                continue

            var_val_lst.append(val.symbol[1:] if val.kind == redef.ID else val.symbol)

        var_val += "".join(var_val_lst)
        stmt += var_val

    elif node.symbol == "<argument>":

        var_tmp = []
        for val in node.children:
            if val.symbol == "<sqnc>":
                var_tmp.append(to_python_code(val))
                continue
            var_tmp.append(val.symbol[1:] if val.kind == redef.ID else val.symbol)

        stmt += "(" + ", ".join(var_tmp) + ")"

    elif node.symbol == "<parameter>":

        tmp_var = []
        for child in node.children:
            has_val = False
            var = child.children[0]
            var_name = var.symbol[1:]

            tmp_val = ""
            for val in var.children:
                has_val = True
                if val.symbol in ["<sqnc>", "<index>", "<argument>"]:
                    tmp_val += to_python_code(val)
                    continue
                tmp_val += val.symbol[1:] if val.kind == redef.ID else val.symbol
            var_val = tmp_val

            var_val = "=" + var_val if has_val else ""
            tmp_var.append(var_name + var_val)

        stmt += ", ".join(tmp_var)

    return stmt


def generate(self, output_instance):
    output_window = OutputWindow(self)

    output_window.output_text.delete("1.0", tk.END)

    print("=" * 10 + "Generating Python code..." + "=" * 10)
    python_code = to_python_code(parse_tree_root)
    python_code += "\n\n# Run the garden function\n"
    python_code += "garden()"
    print(python_code)

    # Redirect stdout and stdin
    sys.stdout = StdRedirector(output_window.output_text)
    sys.stdin = output_window.custom_input

    def run_code():
        try:
            exec(python_code, {"input": output_window.custom_input.get_input})
        except Exception as e:
            output_instance.set_output(f"\nError: {str(e)}")
        finally:
            # Restore stdout and stdin
            sys.stdout = sys.__stdout__
            sys.stdin = sys.__stdin__

    # Run the code in a separate thread to avoid blocking the main thread
    threading.Thread(target=run_code).start()
