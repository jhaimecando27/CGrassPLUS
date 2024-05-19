import redef
from var import ParseTreeNode, parse_tree_root

datatype_check: dict = {
    "tint literal": "int",
    "flora literal": "float",
    "bloom literal": "bool",
    "chard literal": "char",
    "string literal": "string",
}

conv_to_comp_type: dict = {
    "int": "tint literal",
    "float": "flora literal",
    "bool": "bloom literal",
    "char": "chard literal",
    "string": "string literal",
}

sqnc_types: list = ["tulip", "florist", "stem", "dirt"]

operator: list = ["<", ">" "==", "!=", "<=", ">=", "+", "-", "*", "/", "%"]

errors: list = []


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
        return False

    output.set_output("SemanticAnalyser: No Errors Found.\n")
    return True


def get_initial_data(output: object, node: ParseTreeNode, symbol_table: dict) -> dict:
    global datatype_check, errors
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
    global datatype_check, errors

    if errors:
        return

    if node.symbol == "<program>":
        for child in node.children:
            traverse_tree(child, symbol_table, output)

    elif node.symbol == "garden":
        # Create a new symbol table for the function
        local_symbol_table = symbol_table.copy()

        for child in node.children:
            local_symbol_table = traverse_tree(child, local_symbol_table, output)

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

        for child in body_node.children:
            local_symbol_table = traverse_tree(child, local_symbol_table, output)

        if errors:
            return symbol_table

        # Check return type
        for var in body_node.children[-1].children:
            if var.kind == redef.ID:
                if not local_symbol_table.get(var.symbol):
                    errors.append(f"Semantic Error: {var.symbol} is not declared.")
                    return symbol_table

                if local_symbol_table[var.symbol]["type"] != node.type:
                    errors.append(
                        f"Semantic Error: {var.symbol} is not of type {node.type}."
                    )
                    return symbol_table

    elif node.symbol == "<statement>" and node.kind == "variable":
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
                    if (
                        symbol_table[grandchild.symbol]["type"] != node.type
                        and node.type not in sqnc_types
                    ):
                        errors.append(
                            f"Semantic Error: {grandchild.symbol} is not of type {node.type}."
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

                if data and grandchild.kind is redef.ID:
                    print(eval(" ".join(symbol_table[grandchild.symbol]["data"])))

                # Division by zero
                if (
                    data
                    and data[-1] == "/"
                    and grandchild.symbol == "0"
                    or (
                        grandchild.kind == redef.ID
                        and eval(" ".join(symbol_table[grandchild.symbol]["data"])) == 0
                    )
                ):
                    errors.append("Semantic Error: Division by zero.")
                    return symbol_table

                data.append(grandchild.symbol)

            symbol_table[child.symbol] = {
                "kind": child.kind,
                "type": node.type,
                "data": data if data else None,
                "properties": node.properties,
            }

    elif node.symbol == "<statement>" and node.kind == "assignment":

        if symbol_table.get(node.children[0].symbol) is None:
            errors.append(f"Semantic Error: {node.children[0].symbol} is not declared.")
            return symbol_table

        if (
            "properties" in symbol_table[node.children[0].symbol]
            and symbol_table[node.children[0].symbol]["properties"]["constant"] is True
        ):
            errors.append(f"Semantic Error: {node.children[0].symbol} is a immutabe.")
            return symbol_table

        # data
        data = []
        for child in node.children[1:]:

            if child.kind == redef.ID:

                # Undeclared
                if not symbol_table.get(child.symbol):
                    errors.append(f"Semantic Error: {child.symbol} is not declared.")
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
                "type": redef.TINT_LIT,
                "data": [con_node.children[3].symbol],
                "properties": {"global": False, "constant": False},
            }

        if node.children[0].kind == "while":
            for child in con_node.children:
                if child.kind == redef.ID and not symbol_table.get(child.symbol):
                    errors.append(f"Semantic Error: {child.symbol} is not declared.")
                    return symbol_table

        # Go to iterative body
        traverse_tree(node.children[0].children[1], local_symbol_table, output)

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
        for child in con_node.children:
            if child.kind == redef.ID and not symbol_table.get(child.symbol):
                errors.append(f"Semantic Error: {child.symbol} is not declared.")
                return symbol_table

        # Go to if body
        traverse_tree(node.children[0].children[1], local_symbol_table, output)

    elif node.symbol == "<statement>" and node.kind == "i/o":
        data = []
        if node.children[0].symbol == "mint":
            for child in node.children[1:]:

                if child.kind == redef.ID:

                    # Undeclared
                    if not symbol_table.get(child.symbol):
                        errors.append(
                            f"Semantic Error: {child.symbol} is not declared."
                        )
                        return symbol_table

                print("HERE" + symbol_table[child.symbol]["data"])
                # Division by zero
                if data and data[-1] == "/" and (child.symbol == "0"):
                    errors.append("Semantic Error: Division by zero.")
                    return symbol_table
                data.append(child.symbol)

    return symbol_table


def pretty(d, indent=0):
    for key, value in d.items():
        print(" " * indent + "- " + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print("  " * (indent + 1) + "- " + str(value))
