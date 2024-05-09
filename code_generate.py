import tkinter as tk
import sys
from io import StringIO
from var import parse_tree_root, print_parse_tree
import redef as rd

string = ""
code = {}


def generate(input_lines, output_instance):
    code = generate_python_code(parse_tree_root)
    code += "garden()\n"
    print(code)

    captured_output = StringIO()
    sys.stdout = captured_output
    exec(code)
    sys.stdout = sys.__stdout__
    outputed_code = captured_output.getvalue()

    # display output in new tk window, not editable
    output_window = tk.Toplevel()
    output_window.title("Output")
    output_window.geometry("400x400")
    output_text = tk.Text(output_window, wrap="word")
    output_text.insert(tk.END, outputed_code)
    output_text.config(state=tk.DISABLED)
    output_text.pack(expand=True, fill="both")


def semantic_analysis(node=parse_tree_root, indent=4):
    global string
    if node.symbol[1:] != "<" and node.symbol[-1] != ">":
        print(" " * node.level * indent + f"{node.symbol}")
    for child in node.children:
        semantic_analysis(child)


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
                if _is_print:
                    return f"{indent}print({data})\n"

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
                        if_stmt += f"{indent}if {con}:\n" + generate_python_code(child.children[1])
                    elif child.symbol == "eleaf":
                        for condition in child.children[0].children:
                            if condition.kind == rd.ID:
                                con = condition.symbol.replace("#", "")
                                continue
                            if condition.type == "tint literal":
                                con += str(condition.symbol)
                                continue
                            con += condition.symbol
                        if_stmt += f"{indent}elif {con}:\n" + generate_python_code(child.children[1])
                    elif child.symbol == "moss":
                        if_stmt += f"{indent}else:\n" + generate_python_code(child.children[0])

                return if_stmt

            if node.kind == "iterative":
                print('test')
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

                        con_stmt += f"{indent}for {var} in range({start}, {end}, {seq}):\n" + generate_python_code(child.children[1])
                    if child.symbol == "willow":
                        # while loop
                        condition = child.children[0].children
                        con = ""
                        con += condition[0].symbol.replace("#", "")
                        con += condition[1].symbol
                        con += condition[2].symbol

                        for new_child in child.children:
                            if new_child.symbol == "<statement>":
                                con_stmt += f"{indent}while {con}:\n" + generate_python_code(new_child)

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
