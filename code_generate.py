import ast
import sys
from io import StringIO


class GardenNode(ast.AST):
    def __init__(self, body):
        self.body = body


class PrintNode(ast.AST):
    def __init__(self, value):
        self.value = value


class StringDeclarationNode(ast.AST):
    def __init__(self, name, value, data_type):
        self.name = name
        self.value = value
        self.data_type = data_type


def to_python_code(node, indent=0):
    if isinstance(node, GardenNode):
        body_code = "\n".join([to_python_code(child, indent) for child in node.body])
        return f"def garden():\n{body_code}\n\ngarden()"
    elif isinstance(node, PrintNode):
        return f'{" " * indent}print(f"{node.value}")'
    elif isinstance(node, StringDeclarationNode):
        return f'{" " * indent}{node.name}: {node.data_type} = {node.value}'


def generate(input_lines, output_instance):
    # Parse the input code and create AST nodes
    nodes = []
    for line in input_lines:
        line = line.strip("\n")
        if line.startswith("mint"):
            value = (
                line[6:-3].strip().replace("#", "")
            )  # Extract the value from the mint statement, removing last character `)`
            nodes.append(PrintNode(value))
            print(value)
        elif line.startswith(("string", "tint", "floral", "bloom")):
            parts = line.split("=")
            name = parts[0].strip().split(" ")[1][1:]
            value = parts[1].strip()
            # Determine the type based on the line prefix
            if line.startswith("string"):
                type_ = "string"
            elif line.startswith("tint"):
                type_ = "int"
            elif line.startswith("floral"):
                type_ = "float"
            elif line.startswith("bloom"):
                type_ = "bool"
            nodes.append(StringDeclarationNode(name, value, type_))

    # Create the AST node for the garden() function
    garden_node = GardenNode(nodes)

    # Convert to Python code
    python_code = to_python_code(garden_node, indent=4)  # Adding indentation

    print(input_lines)
    print("====")
    print(python_code)
    print("====")
    captured_output = StringIO()
    sys.stdout = captured_output
    exec(python_code)
    sys.stdout = sys.__stdout__
    output_variable = captured_output.getvalue()
    output_instance.set_output(
        f"{output_variable}"
    )
