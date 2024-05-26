import redef
import re
from var import ParseTreeNode


symbol_table = {}

translate = {
    "tint": "int",
    "flora": "float",
    "chard": "char",
    "string": "str",
    "bloom": "bool",
    "florist": "list",
    "tulip": "tuple",
    "stem": "set",
    "dirt": "dict",
    "fern": "for",
    "willow": "while",
    "tint literal": "int",
    "flora literal": "float",
    "chard literal": "char",
    "string literal": "str",
    "bloom literal": "bool",
}

arith_ops = ["+", "-", "*", "/", "%", "(", ")"]
sqnc_ops = ["{", "}", "[", "]"]

errors = []


def semantic_analysis(node: ParseTreeNode, local_table={}) -> bool:

    if node.symbol == "<program>":
        for child in node.children:
            if not semantic_analysis(child):
                return False

        local_table.clear()

    elif node.symbol in ["garden", "<body>"]:
        for child in node.children:
            if not semantic_analysis(child, local_table):
                return False
        local_table.clear()

    elif node.symbol == "<statement>":

        if node.kind in ["variable", "assignment"]:

            # Initialize or update the variable
            for var_node in node.children:

                if var_node.symbol == "<argument>":
                    continue

                # Invalid Variable
                var_name = var_node.symbol[1:]
                var_type = translate[node.type] if node.type else None
                type_cast = translate[var_node.type] if var_node.type else None
                var_is_global = (
                    node.properties["global"] if "global" in node.properties else False
                )
                var_is_const = (
                    node.properties["constant"]
                    if "constant" in node.properties
                    else False
                )

                # Using Undefined variable (if var_type is None)
                if node.kind == "assignment":
                    if var_name not in local_table and var_name not in symbol_table:
                        errors.append(
                            f"Semantic Error: Undefined variable {var_name} at line {node.line_number}.\n"
                        )
                        return False

                    # Update var_type
                    if var_name in symbol_table:
                        var_type = symbol_table[var_name]["type"]
                    elif var_name in local_table:
                        var_type = local_table[var_name]["type"]

                prev_val = None
                for val in var_node.children:

                    # Assigning Invalid Type
                    if (
                        val.symbol not in arith_ops
                        and val.symbol not in sqnc_ops
                        and val.symbol not in ["<sqnc>", "<index>", "<argument>"]
                        and val.type
                        and var_type != translate[val.type]
                        and translate[node.type] not in ["list", "tuple", "set", "dict"]
                    ):
                        if type_cast:
                            if var_type != type_cast:
                                errors.append(
                                    f"Semantic Error: Invalid type for variable {var_name} at line {node.line_number}.\n"
                                )
                                return False
                        else:
                            print(val.symbol, var_type)
                            errors.append(
                                f"Semantic Error: Invalid type for variable {var_name} at line {node.line_number}.\n"
                            )
                            return False

                    # Assigning Undefined variable
                    if val.kind == redef.ID:
                        if (
                            val.symbol[1:] not in local_table
                            and val.symbol[1:] not in symbol_table
                        ):
                            errors.append(
                                f"Semantic Error: Undefined variable {val.symbol} at line {node.line_number}.\n"
                            )
                            return False

                    # <sqnc> node
                    if val.symbol == "<sqnc>":
                        for sqnc_val in val.children:
                            if sqnc_val.kind == redef.ID:

                                # Using Undefined variable
                                if (
                                    sqnc_val.symbol[1:] not in local_table
                                    and val.symbol[1:] not in symbol_table
                                ):
                                    errors.append(
                                        f"Semantic Error: Undefined variable {sqnc_val.symbol} at line {node.line_number}.\n"
                                    )
                                    return False

                    if val.symbol == "{" or val.symbol == "[":
                        # Mismatch opening and closing brackets
                        if (
                            val.symbol == "[" and var_node.children[-1].symbol != "]"
                        ) or (
                            val.symbol == "{" and var_node.children[-1].symbol != "}"
                        ):
                            errors.append(
                                f"Semantic Error: Mismatch opening and closing brackets at line {node.line_number}.\n"
                            )
                            return False

                        # Invalid type for sequence
                        if (
                            val.symbol == "[" and var_type not in ["list", "tuple"]
                        ) or (val.symbol == "{" and var_type not in ["set", "dict"]):
                            errors.append(
                                f"Semantic Error: Invalid type for sequence at line {node.line_number}.\n"
                            )
                            return False

                    # <index> node
                    if val.symbol == "<index>":
                        for index_val in val.children:
                            if index_val.kind == redef.ID:
                                # Using Undefined variable
                                if (
                                    index_val.symbol[1:] not in local_table
                                    and index_val.symbol[1:] not in symbol_table
                                ):
                                    errors.append(
                                        f"Semantic Error: Undefined variable {index_val.symbol} at line {index_node.line_number}.\n"
                                    )
                                    return False

                    # <argument> node
                    if val.symbol == "<argument>":
                        for arg_val in val.children:
                            # Using Undefined Variables
                            if arg_val.kind == redef.ID:
                                if (
                                    arg_val.symbol[1:] not in local_table
                                    and arg_val.symbol[1:] not in symbol_table
                                ):
                                    errors.append(
                                        f"Semantic Error: Undefined variable {arg_val.symbol} at line {node.line_number}.\n"
                                    )
                                    return False

                        # Invalid number of arguments
                        if (
                            len(val.children)
                            != symbol_table[prev_val.symbol[1:]]["param_num"]
                        ):
                            errors.append(
                                f"Semantic Error: Invalid number of arguments for function {var_name} at line {node.line_number}.\n"
                            )
                            return False

                        # Invalid argument type
                        for i, arg in enumerate(val.children):
                            arg_type = (
                                local_table[arg.symbol[1:]]["type"]
                                if arg.kind == redef.ID
                                else translate[arg.type]
                            )
                            func_param_type = symbol_table[prev_val.symbol[1:]][
                                "param"
                            ][i]

                            if arg_type != func_param_type:
                                errors.append(
                                    f"Semantic Error: Invalid type for argument {arg.symbol} at line {node.line_number}.\n"
                                )
                                return False

                    # Updating Constant variable
                    if var_is_const:
                        errors.append(
                            f"Semantic Error: Cannot update constant variable {var_name} at line {node.line_number}.\n"
                        )
                        return False

                    # Update Symbol Table for Global Variables and Local Variables
                    if var_is_global:
                        if var_name not in symbol_table:
                            symbol_table[var_name] = {
                                "type": var_type,
                                "kind": node.kind,
                                "global": True,
                                "constant": var_is_const,
                            }
                    else:
                        local_table[var_name] = {
                            "type": var_type,
                            "kind": node.kind,
                            "constant": var_is_const,
                        }

                    prev_val = val

        elif node.kind == "i/o":
            if len(node.children) > 2 and node.children[1].symbol == "inpetal":
                # No prompt message
                if node.children[2].type != redef.STR_LIT:
                    errors.append(
                        f"Semantic Error: Missing prompt message for input at line {node.line_number}.\n"
                    )
                    return False

                var_name = node.children[0].symbol[1:]
                var_type = translate[node.type] if node.type in translate else None

                # Using Undefined variable
                if var_type is None:
                    if var_name not in local_table and var_name not in symbol_table:
                        errors.append(
                            f"Semantic Error: Undefined variable {var_name} at line {node.line_number}.\n"
                        )
                        return False

                # Store the variable in the local table
                else:
                    local_table[var_name] = {
                        "type": var_type,
                        "kind": node.kind,
                        "constant": False,
                    }

            else:

                for data in node.children:
                    if data.symbol in ["<sqnc>", "<index>"]:
                        # <sqnc> node
                        if data.symbol == "<sqnc>":
                            for sqnc_val in data.children:
                                if sqnc_val.kind == redef.ID:

                                    # Using Undefined variable
                                    if (
                                        sqnc_val.symbol[1:] not in local_table
                                        and val.symbol[1:] not in symbol_table
                                    ):
                                        errors.append(
                                            f"Semantic Error: Undefined variable {sqnc_val.symbol} at line {node.line_number}.\n"
                                        )
                                        return False

                            # Mismatch opening and closing brackets
                            if len(val.children) % 2 != 0:
                                errors.append(
                                    f"Semantic Error: Mismatch opening and closing brackets at line {node.line_number}.\n"
                                )
                                return False

                        # <index> node
                        if data.symbol == "<index>":
                            for index_val in data.children:
                                if index_val.kind == redef.ID:
                                    # Using Undefined variable
                                    if (
                                        index_val.symbol[1:] not in local_table
                                        and index_val.symbol[1:] not in symbol_table
                                    ):
                                        errors.append(
                                            f"Semantic Error: Undefined variable {index_val.symbol} at line {node.line_number}.\n"
                                        )
                                        return False

                    # String Interpolation
                    elif data.type == redef.STR_LIT:
                        open_braces = data.symbol.count("{")
                        tmp_str = data.symbol.replace("{#", "{")
                        close_braces = data.symbol.count("}")
                        # }}}}

                        is_formatted = open_braces == close_braces and (
                            open_braces > 0 and close_braces > 0
                        )

                        if is_formatted:
                            vars = re.findall(r"{(.*?)}", tmp_str)
                            for var in vars:
                                # Check if varaible is defined
                                if var not in local_table and var not in symbol_table:
                                    # Check if variable is valid variable
                                    if [
                                        char for char in var if char not in redef.DELIMi
                                    ]:
                                        errors.append(
                                            f"Semantic Error: Invalid String Interpolation {var} at line {node.line_number}.\n"
                                        )
                                    else:
                                        errors.append(
                                            f"Semantic Error: Undefined variable {var} at line {node.line_number}.\n"
                                        )
                                    return False

        elif node.kind == "if":

            # Max nested
            if node.leaf_level > 3 or node.eleaf_level > 3:
                errors.append(
                    f"Semantic Error: Maximum nested leaf/eleaf statements at line {node.line_number}.\n"
                )
                return False

            for con_node in node.children:
                # Get the body of the con statement
                if not semantic_analysis(con_node.children[0], local_table.copy()):
                    return False

                # Validate the condition
                if con_node.symbol in ["leaf", "eleaf"]:
                    if_con = con_node.children[1]
                    for val in if_con.children:
                        # <sqnc> node
                        if val.symbol == "<sqnc>":
                            for sqnc_val in val.children:
                                if sqnc_val.kind == redef.ID:

                                    # Using Undefined variable
                                    if (
                                        sqnc_val.symbol[1:] not in local_table
                                        and val.symbol[1:] not in symbol_table
                                    ):
                                        errors.append(
                                            f"Semantic Error: Undefined variable {sqnc_val.symbol} at line {node.line_number}.\n"
                                        )
                                        return False

                        if val.symbol == "{" or val.symbol == "[":
                            # Mismatch opening and closing brackets
                            if (
                                val.symbol == "["
                                and var_node.children[-1].symbol != "]"
                            ) or (
                                val.symbol == "{"
                                and var_node.children[-1].symbol != "}"
                            ):
                                errors.append(
                                    f"Semantic Error: Mismatch opening and closing brackets at line {node.line_number}.\n"
                                )
                                return False

                            # Invalid type for sequence
                            if (
                                val.symbol == "[" and var_type not in ["list", "tuple"]
                            ) or (
                                val.symbol == "{" and var_type not in ["set", "dict"]
                            ):
                                errors.append(
                                    f"Semantic Error: Invalid type for sequence at line {node.line_number}.\n"
                                )
                                return False

                        # <index> node
                        if val.symbol == "<index>":
                            for index_val in val.children:
                                if index_val.kind == redef.ID:
                                    # Using Undefined variable
                                    if (
                                        index_val.symbol[1:] not in local_table
                                        and index_val.symbol[1:] not in symbol_table
                                    ):
                                        errors.append(
                                            f"Semantic Error: Undefined variable {index_val.symbol} at line {index_node.line_number}.\n"
                                        )
                                        return False

                        # Undefined Variable
                        if val.kind == redef.ID:
                            if (
                                val.symbol[1:] not in local_table
                                and val.symbol[1:] not in symbol_table
                            ):
                                errors.append(
                                    f"Semantic Error: Undefined variable {val.symbol} at line {node.line_number}.\n"
                                )
                                return False

        elif node.kind == "iterative":

            # Max nested
            if node.fern_level > 3 or node.willow_level > 3:
                errors.append(
                    f"Semantic Error: Maximum nested fern/willow statements at line {node.line_number}.\n"
                )
                return False

            iter_node = node.children[0]
            iter_type = iter_node.symbol
            iter_con = iter_node.children[1]
            iter_local_table = local_table.copy()

            if iter_type == "fern":
                if iter_con.children[1].symbol == "at":
                    iter_v1 = iter_con.children[0].symbol[1:]
                    iter_v2 = iter_con.children[2].symbol[1:]

                    if iter_v1 not in local_table and iter_v1 not in symbol_table:
                        errors.append(
                            f"Semantic Error: Undefined variable {iter_v1} at line {node.line_number}.\n"
                        )
                        return False

                    if iter_v2 not in local_table and iter_v2 not in symbol_table:
                        errors.append(
                            f"Semantic Error: Undefined variable {iter_v2} at line {node.line_number}.\n"
                        )
                        return False

                else:
                    iter_local_table[iter_con.children[1].symbol[1:]] = {
                        "type": translate[iter_con.children[0].symbol],
                        "kind": "variable",
                        "constant": False,
                    }

                    iter_v = iter_con.children[6].symbol[1:]
                    if iter_v[0] == "#":
                        iter_v = iter_v[1:]

                        if (
                            iter_v not in iter_local_table
                            and iter_v not in symbol_table
                        ):
                            errors.append(
                                f"Semantic Error: Undefined variable {iter_v} at line {node.line_number}.\n"
                            )
                            return False

            else:
                iter_v1 = iter_con.children[0]
                iter_v2 = iter_con.children[2]

                if iter_v1.kind == redef.ID:
                    if (
                        iter_v1.symbol[1:] not in local_table
                        and iter_v1.symbol[1:] not in symbol_table
                    ):
                        errors.append(
                            f"Semantic Error: Undefined variable {iter_v1.symbol} at line {node.line_number}.\n"
                        )
                        return False

                if iter_v2.kind == redef.ID:
                    if (
                        iter_v2.symbol[1:] not in local_table
                        and iter_v2.symbol[1:] not in symbol_table
                    ):
                        errors.append(
                            f"Semantic Error: Undefined variable {iter_v2.symbol} at line {node.line_number}.\n"
                        )
                        return False

            if not semantic_analysis(iter_node.children[0], iter_local_table):
                return False

        elif node.kind == "tree":
            tree_con_var = node.children[0].children[0]
            if tree_con_var.kind == redef.ID:
                if (
                    tree_con_var.symbol[1:] not in local_table
                    and tree_con_var.symbol[1:] not in symbol_table
                ):
                    errors.append(
                        f"Semantic Error: Undefined variable {tree_con_var.symbol} at line {node.line_number}.\n"
                    )
                    return False

            for branch in node.children[0].children[1:]:

                have_break = False

                for stmt_nodes in branch.children[1:]:
                    if not semantic_analysis(stmt_nodes, local_table):
                        return False
                    if stmt_nodes.kind == "break":
                        have_break = True

                if not have_break:
                    errors.append(
                        f"Semantic Error: Missing break statement at line {branch.line_number}.\n"
                    )
                    return False

    elif node.symbol == "<function>":
        func_name = node.children[0].symbol[1:]
        func_type = None if node.type not in translate else translate[node.type]

        # add param to local table
        for param in node.children[1].children:
            param_name = param.children[0].symbol[1:]
            param_type = translate[param.type]
            local_table[param_name] = {
                "type": param_type,
                "kind": "variable",
                "constant": False,
            }

        if not semantic_analysis(node.children[2], local_table):
            return False

        # Return type for function
        if func_type is not None and node.children[2].children[-1].kind != "regrow":
            errors.append(
                f"Semantic Error: Missing return type for function {func_name} at line {node.line_number}.\n"
            )
            return False
        local_table.clear()

    return True
