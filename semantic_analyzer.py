import redef
from var import ParseTreeNode, parse_tree_root

datatype_check: dict = {
    "tint literal": "int",
    "flora literal": "float",
    "bloom literal": "bool",
    "chard literal": "char",
    "string literal": "string",
    "tulip": "tuple",
    "florist": "list",
    "dirt": "dict",
    "stem": "set",
}

conv_to_comp_type: dict = {
    "int": "tint literal",
    "float": "flora literal",
    "bool": "bloom literal",
    "char": "chard literal",
    "string": "string literal",
    "tulip": "tulip",
    "florist": "florist",
    "dirt": "dirt",
    "stem": "stem",
}

sqnc_types: list = ["tulip", "florist", "stem", "dirt"]

operator: list = ["<", ">" "==", "!=", "<=", ">=", "+", "-", "*", "/", "%"]

errors: list = []


code: list = []
global_code: list = []


def is_semantic_valid(output: object) -> bool:
    global errors
    errors = []

    symbol_table: dict = {}

    # Get the initial data (global variables and functions)
    symbol_table = get_initial_data(output, parse_tree_root, symbol_table)

    # DEBUG
    print("\n\n" + "=" * 10 + " SYMBOL TABLE (GLOBAL) " + "=" * 10)
    if symbol_table:
        pretty(symbol_table, 0)
    else:
        print("No symbol table created.")

    traverse_tree(parse_tree_root, symbol_table, output)

    if errors:
        print(errors)
        for error in errors:
            output.set_output(error)

        code.clear()
        global_code.clear()
        return False

    code.append("garden()")

    print("\n\n" + "=" * 10 + " CODE " + "=" * 10)
    print("\n".join(code))
    print("=" * 10 + " END CODE " + "=" * 10)

    output.set_output("SemanticAnalyser: No Errors Found.")
    global_code.clear()
    return True


def get_initial_data(output: object, node: ParseTreeNode, symbol_table: dict) -> dict:
    global datatype_check, errors, code, global_code
    # Get the initial data (global variables and functions)

    if errors:
        return symbol_table

    if node.symbol == "<program>":
        for child in node.children:
            get_initial_data(output, child, symbol_table)

    elif node.symbol == "<variable>" and node.properties["global"] is True:

        # variable name
        for child in node.children:

            # data
            data = []
            for grandchild in child.children:

                if grandchild.kind == redef.ID:

                    # Undeclared
                    if not symbol_table.get(grandchild.symbol):
                        errors.append(
                            f"Semantic Error: {grandchild.symbol} is not declared."
                        )
                        return symbol_table

                    # Type mismatch (Variable and Variable)
                    if symbol_table[grandchild.symbol]["type"] != node.type:
                        errors.append(
                            f"Semantic Error: {grandchild.symbol} is not of type {node.type}."
                        )
                        return symbol_table

                # Type mismatch (Variable and Literal)
                elif (
                    grandchild.symbol not in operator
                    and datatype_check[grandchild.type] != node.type
                    and node.type not in sqnc_types
                ):
                    errors.append(
                        f"Semantic Error: {child.symbol} is not of type {node.type}."
                    )
                    return symbol_table
                data.append(grandchild.symbol)

            code.append(
                f"{child.symbol[1:]}:{node.type} = {data[0] if data else 'None'}"
            )
            global_code.append(f"{child.symbol[1:]}")

            symbol_table[child.symbol] = {
                "kind": child.kind,
                "type": node.type,
                "data": data if data else None,
                "properties": node.properties,
            }

    elif node.symbol == "<function>":
        # count the number of parameters
        parms = {}
        num_parameters = 0
        param_node = node.children[1]

        # <variable>
        for grandchild in param_node.children:
            num_parameters += 1

            # variable name
            for greatgrandchild in grandchild.children:

                # data
                data = []
                for greatgreatgrandchild in greatgrandchild.children:
                    data.append(greatgreatgrandchild.symbol)

                parms[greatgrandchild.symbol] = {
                    "kind": grandchild.kind,
                    "type": grandchild.type,
                    "data": data if data else None,
                    "properties": {"global": False, "constant": False},
                }

        symbol_table[node.children[0].symbol] = {
            "kind": "function",
            "type": node.type,
            "line_number": node.line_number,
            "num_parameters": num_parameters,
            "parameters": parms if parms else None,
        }

    return symbol_table


def traverse_tree(node: ParseTreeNode, symbol_table: dict, output: object):
    global datatype_check, errors, code, global_code

    if errors:
        return symbol_table

    if node.symbol == "<program>":
        for child in node.children:
            traverse_tree(child, symbol_table, output)

    elif node.symbol == "garden":
        code.append("")
        code.append("def garden() -> None:")
        if global_code:
            code.append("    global " + ", ".join(global_code))
        # Create a new symbol table for the function
        local_symbol_table = symbol_table.copy()

        for child in node.children:
            new_local = traverse_tree(child, local_symbol_table, output)

            if new_local is not None:
                local_symbol_table.update(new_local)

        # DEBUG
        print("\n\n" + "=" * 10 + " SYMBOL TABLE (GARDEN w/ GLOBAL) " + "=" * 10)
        if local_symbol_table:
            pretty(local_symbol_table, 0)
        else:
            print("No symbol table created.")

    elif node.symbol == "<function>":
        # count the number of parameters
        param_node = node.children[1]
        body_node = node.children[2]
        local_symbol_table = symbol_table.copy()
        vars = []

        # <variable>
        for grandchild in param_node.children:

            # variable name
            for greatgrandchild in grandchild.children:

                # data
                data = []
                for greatgreatgrandchild in greatgrandchild.children:
                    data.append(greatgreatgrandchild.symbol)

                local_symbol_table[greatgrandchild.symbol] = {
                    "kind": grandchild.kind,
                    "type": grandchild.type,
                    "data": data if data else None,
                    "properties": {"global": False, "constant": False},
                }
                vars.append(
                    f"{greatgrandchild.symbol[1:]}:{grandchild.type}{' = ' + data[0] if data else ''}"
                )

        if errors:
            return symbol_table

        code.append(
            f"def {node.children[0].symbol[1:]}({', '.join(vars)}) -> {node.type}:"
        )

        for child in body_node.children:
            local_symbol_table = traverse_tree(child, local_symbol_table, output)

        # Check return type
        if node.type != "None":
            tmp = []
            for var in body_node.children[-1].children:
                if var.kind == redef.ID:
                    if local_symbol_table.get(var.symbol) is None:
                        errors.append(f"Semantic Error: {var.symbol} is not declared at line {node.line_number}")
                        return symbol_table

                    if local_symbol_table[var.symbol]["type"] != node.type:
                        errors.append(
                            f"Semantic Error: {var.symbol} is not of type {node.type} at line {node.line_number}"
                        )
                        return symbol_table
                tmp.append(var.symbol[1:] if var.kind == redef.ID else var.symbol)

        if node.type != "None":
            code.append("    " * body_node.level + f"return " + " ".join(tmp))

    elif node.symbol == "<statement>" and node.kind == "variable":
        # variable name
        for child in node.children:

            # data
            data = []
            sqnc = []
            prms = []
            for grandchild in child.children:

                if grandchild.kind == redef.ID:

                    # Undeclared
                    if not symbol_table.get(grandchild.symbol):
                        errors.append(
                            f"Semantic Error: {grandchild.symbol} is not declared at line {node.line_number}"
                        )
                        return symbol_table

                    # Type mismatch (Variable and Variable)
                    if (
                        symbol_table[grandchild.symbol]["type"] != node.type
                        and node.type not in sqnc_types
                    ):
                        errors.append(
                            f"Semantic Error: {grandchild.symbol} is not of type {node.type} at line {node.line_number}"
                        )
                        return symbol_table

                # Type mismatch (Variable and Literal)
                elif (
                    grandchild.type is not None
                    and grandchild.symbol not in operator
                    and datatype_check[grandchild.type] != node.type
                    and node.type not in sqnc_types
                ):
                    errors.append(
                        f"Semantic Error: {child.symbol} is not of type {node.type}."
                    )
                    return symbol_table

                # Parameter mismatch
                elif grandchild.symbol == "<argument>":
                    if symbol_table[child.children[0].symbol]["num_parameters"] != len(
                        grandchild.children
                    ):
                        errors.append(
                            f"Semantic Error: {child.children[0].symbol} requires {symbol_table[child.children[0].symbol]['num_parameters']} parameters."
                        )
                        return symbol_table

                    for i, arg in enumerate(grandchild.children):
                        # parameter type mismatch
                        if (
                            symbol_table[child.children[0].symbol]["parameters"][
                                list(
                                    symbol_table[child.children[0].symbol]["parameters"]
                                )[i]
                            ]["type"]
                            != symbol_table[arg.symbol]["type"]
                        ):
                            expected_type = conv_to_comp_type[
                                symbol_table[child.children[0].symbol]["parameters"][
                                    list(
                                        symbol_table[child.children[0].symbol][
                                            "parameters"
                                        ]
                                    )[i]
                                ]["type"]
                            ]

                            errors.append(
                                f"Semantic Error: {child.children[0].symbol} requires {expected_type} for parameter {i + 1}."
                            )

                            return symbol_table
                        prms.append(
                            arg.symbol[1:] if arg.kind == redef.ID else arg.symbol
                        )
                elif node.type in sqnc_types:
                    sqnc.append(grandchild.symbol)

                # Division by zero
                if (
                    data
                    and data[-1] == "/"
                    and grandchild.symbol == "0"
                    or (
                        grandchild.kind == redef.ID
                        and (
                            "data" in symbol_table[grandchild.symbol]
                            and eval(" ".join(symbol_table[grandchild.symbol]["data"]))
                            == 0
                        )
                    )
                ):
                    errors.append("Semantic Error: Division by zero.")
                    return symbol_table

                data.append(
                    grandchild.symbol[1:]
                    if grandchild.kind == redef.ID
                    else grandchild.symbol
                )

            symbol_table[child.symbol] = {
                "kind": child.kind,
                "type": node.type,
                "data": data if data else None,
                "properties": node.properties,
            }
            prms = ", ".join(prms)

            if data and data[-1] == "<argument>" and node.type not in sqnc_types:
                code.append(
                    "    " * node.level
                    + f"{child.symbol[1:]}:{node.type} = {data[0]}({prms})"
                )
            elif node.type not in sqnc_types:
                code.append(
                    "    " * node.level
                    + f"{child.symbol[1:]}:{node.type} = {' '.join(data) if data else 'None'}"
                )
            elif node.type in sqnc_types:
                # Check if the sequence is correct
                if (
                    (sqnc[0] == "[" and sqnc[-1] == "]")
                    and node.type in ["dirt", "stem"]
                ) or (
                    (sqnc[0] == "{" and sqnc[-1] == "}")
                    and node.type in ["tulip", "florist"]
                ):
                    errors.append(
                        f"Semantic Error: {node.children[0].symbol} requires a {node.type} of values."
                    )

                # Check if the pair is correct
                if (sqnc[0] == "{" and sqnc[-1] != "}") or (
                    sqnc[0] == "[" and sqnc[-1] != "]"
                ):
                    errors.append(
                        f"Semantic Error: {node.children[0].symbol} requires a proper closing bracket at line {node.line_number}"
                    )

                if node.type == "dirt":
                    data = ", ".join(sqnc[1:-1]).replace(", :, ", ":")
                    code.append(
                        "    " * node.level
                        + f"{child.symbol[1:]}:{datatype_check[node.type]}"
                        + f"= {sqnc[0]}{data}{sqnc[-1]}"
                    )
                elif node.type == "stem":
                    data = ", ".join(sqnc[1:-1])
                    code.append(
                        "    " * node.level
                        + f"{child.symbol[1:]}:{datatype_check[node.type]} = set({sqnc[0]}{data}{sqnc[-1]})"
                    )
                else:
                    code.append(
                        "    " * node.level
                        + f"{child.symbol[1:]}:{datatype_check[node.type]} = {sqnc[0]}{', '.join(sqnc[1:-1])}{sqnc[-1]}"
                    )

    elif node.symbol == "<statement>" and node.kind == "assignment":

        if symbol_table.get(node.children[0].symbol) is None:
            errors.append(
                f"Semantic Error: {node.children[0].symbol} is not declared at line {node.line_number}"
            )
            return symbol_table

        if (
            "properties" in symbol_table[node.children[0].symbol]
            and (symbol_table[node.children[0].symbol]["properties"]["constant"] is True
                 or symbol_table[node.children[0].symbol]["type"] == "tulip")
        ):
            errors.append(
                f"Semantic Error: {node.children[0].symbol} is a immutabe at line {node.line_number}"
            )
            return symbol_table

        # data
        data = []
        for child in node.children[1:]:

            if child.kind == redef.ID:

                # Undeclared
                if not symbol_table.get(child.symbol):
                    errors.append(
                        f"Semantic Error: {child.symbol} is not declared at line {node.line_number}"
                    )
                    return symbol_table

                # Type mismatch (Variable and Variable)
                if (
                    symbol_table[child.symbol]["type"]
                    != symbol_table[node.children[0].symbol]["type"]
                ):
                    expected_type = conv_to_comp_type[
                        symbol_table[node.children[0].symbol]["type"]
                    ]
                    errors.append(
                        f"Semantic Error: {child.symbol} is not of type {expected_type}."
                    )
                    return symbol_table

            # Type mismatch (Variable and Literal)
            elif (
                child.symbol not in operator
                and datatype_check[child.type]
                != symbol_table[node.children[0].symbol]["type"]
            ):
                expected_type = conv_to_comp_type[
                    symbol_table[node.children[0].symbol]["type"]
                ]
                errors.append(
                    f"Semantic Error: {child.symbol} is not of type {expected_type}."
                )
                return symbol_table

            # Division by zero
            if data and data[-1] == "/" and child.symbol == "0":
                errors.append("Semantic Error: Division by zero.")
                return symbol_table

            data.append(child.symbol)

            tmp = data[0][1:] if data[0][0] == "#" else data[0]
            print(data[0][1:] if data[0][0] == "#" else data[0])

            code.append(
                "    " * node.level
                + f"{node.children[0].symbol[1:]} {node.properties['assignment-op']} {tmp}"
            )

        if symbol_table[node.children[0].symbol]["kind"] == "function":
            code.append("    " * node.level + f"{node.children[0].symbol[1:]}()")

        symbol_table[node.children[0].symbol]["data"] = data

    elif node.symbol == "<statement>" and node.kind == "iterative":
        # Exceeds the maximum number of nested loops
        if node.level >= 4:
            errors.append("Semantic Error: Exceeds the maximum number of nested loops.")
            return symbol_table

        # Create a new symbol table for the iterative statements
        local_symbol_table = symbol_table.copy()

        # store #i in the symbol table
        con_node = node.children[0].children[0]
        if node.children[0].kind == "for":
            local_symbol_table[con_node.children[1].symbol] = {
                "kind": redef.ID,
                "type": "int",
                "properties": {"global": False, "constant": False},
            }

            # name
            for child in node.children:
                var = []
                print(child.symbol)

                for item in child.children[0].children:
                    var.append(
                        item.symbol[1:] if item.kind == redef.ID else item.symbol
                    )

                iter = var[1]
                start = var[3]
                end = var[7]

                code.append(
                    "    " * node.level + f"for {iter} in range({start}, {end}):"
                )

                for grandchild in child.children[1:]:
                    traverse_tree(grandchild, local_symbol_table, output)

        elif node.children[0].kind == "while":
            var = []
            for child in con_node.children:
                if child.kind == redef.ID and not symbol_table.get(child.symbol):
                    errors.append(f"Semantic Error: {child.symbol} is not declared.")
                    return symbol_table

                var.append(child.symbol[1:] if child.kind == redef.ID else child.symbol)

            iter = var[0]
            op = var[1]
            end = var[2]

            code.append("    " * node.level + f"while {iter} {op} {end}:")
            for child in node.children[0].children[1:]:
                traverse_tree(child, local_symbol_table, output)

    elif node.symbol == "<statement>" and (
        node.kind == "if" or node.kind == "elif" or node.kind == "else"
    ):
        # Exceeds the maximum number of nested loops
        if node.level >= 4:
            errors.append("Semantic Error: Exceeds the maximum number of nested loops.")
            return symbol_table

        # Create a new symbol table for the if statements
        local_symbol_table = symbol_table.copy()

        # store #i in the symbol table
        con_node = node.children[0].children[0]
        con_var = []
        for child in con_node.children:
            if child.kind == redef.ID and not symbol_table.get(child.symbol):
                errors.append(f"Semantic Error: {child.symbol} is not declared.")
                return symbol_table
            con_var.append(child.symbol)

        # name
        for child in node.children:
            var = []
            print(child.symbol)
            if child.symbol == "leaf":
                for item in child.children[0].children:
                    var.append(
                        item.symbol[1:] if item.kind == redef.ID else item.symbol
                    )
                print(var)
                code.append("    " * node.level + f"if {' '.join(var)}:")
                traverse_tree(child.children[1], local_symbol_table, output)
            if child.symbol == "eleaf":
                for item in child.children[0].children:
                    var.append(
                        item.symbol[1:] if item.kind == redef.ID else item.symbol
                    )
                code.append("    " * node.level + f"elif {' '.join(var)}:")
                traverse_tree(child.children[1], local_symbol_table, output)
            if child.symbol == "moss":
                code.append("    " * node.level + "else:")
                traverse_tree(child.children[0], local_symbol_table, output)

    elif node.symbol == "<statement>" and node.kind == "i/o":
        if node.children[0].symbol == "mint":
            data = []
            for child in node.children[1:]:

                if child.kind == redef.ID:

                    # Undeclared
                    if not symbol_table.get(child.symbol):
                        errors.append(
                            f"Semantic Error: {child.symbol} is not declared."
                        )
                        return symbol_table

                # Division by zero
                if (
                    data
                    and data[-1] == "/"
                    and (eval(" ".join(symbol_table[child.symbol]["data"])) == 0)
                ):
                    errors.append("Semantic Error: Division by zero.")
                    return symbol_table

                # f-string
                if child.type == redef.STR_LIT:
                    tmp = "f"
                    pass_it = False
                    var = ""

                    for char in child.symbol:
                        if char == "{":
                            tmp += "{"
                            pass_it = True
                            var = ""
                            continue

                        elif pass_it and char != "}" and char != "#":
                            tmp += char
                            var += char
                            continue

                        elif char == "}":
                            pass_it = False
                            tmp += "}"

                            if not symbol_table.get(var):
                                errors.append(
                                    f"Semantic Error: {var} is not declared at line {node.line_number}"
                                )
                                return symbol_table

                            continue
                        elif not pass_it:
                            tmp += char
                            continue

                        else:
                            var += char

                    child.symbol = tmp

                data.append(
                    child.symbol[1:] if child.kind == redef.ID else child.symbol
                )

            code.append("    " * node.level + f"print({' '.join(data)})")

        # inpetal (input)
        else:
            if node.type is None and not symbol_table.get(node.children[0].symbol):
                errors.append(
                    f"Semantic Error: {node.children[0].symbol} is not declared at line {node.line_number}"
                )
                return symbol_table

            symbol_table[node.children[0].symbol] = {
                "kind": node.kind,
                "type": node.type,
                "data": node.children[2].symbol,
                "properties": node.properties,
            }

            code.append(
                "    " * node.level
                + f"{node.children[0].symbol[1:]}{':' + node.type if node.type else ''} = {node.type}(input({node.children[2].symbol if node.children[2].symbol else ''}))"
            )
    elif node.symbol == "<statement>" and node.kind == "tree":

        if symbol_table.get(node.children[0].children[0].symbol) is None:
            errors.append(
                f"Semantic Error: {node.children[0].children[0].symbol} is not declared at line {node.line_number}"
            )
            return symbol_table

        code.append(
            "    " * node.level + f"match {node.children[0].children[0].symbol[1:]}:"
        )

        for child in node.children[0].children[1:]:
            code.append(
                "    " * node.children[0].level + f"case {child.children[0].symbol}:"
            )
            for grandchild in child.children[1:]:
                traverse_tree(grandchild, symbol_table, output)

    elif node.symbol == "<statement>" and node.kind == "break":
        code.append("    " * node.level + "break")

    return symbol_table


def pretty(d, indent=0):
    for key, value in d.items():
        print(" " * indent + "- " + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print("  " * (indent + 1) + "- " + str(value))
