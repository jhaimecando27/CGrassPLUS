import redef

symbol_table = {}


def is_semantic_valid(output_instance: object, lexer_output: object) -> bool:
    avoid = ["<space>", "<--", "-->", "?"]
    lexer_output = [x for x in lexer_output if x[1] not in avoid]
    lexer_output.append(("EOF", "EOF"))
    token, lexeme = zip(*lexer_output)
    fern_depth: int = 0
    leaf_depth: int = 0
    willow_depth: int = 0
    print(token)

    datatypes = ["hard", "tint", "flora", "string", "chard", "bloom"]

    # Get all functions
    row: int = 1
    col: int = 0
    while token[col] != "EOF":
        if (
            (token[col] == redef.ID and lexeme[col - 2] in datatypes)
            or lexeme[col] == "garden"
        ) and lexeme[col + 1] == "(":
            key = lexeme[col]
            type = lexeme[col - 2] if lexeme[col] != "garden" else "garden"
            symbol_table[key] = {
                "kind": "function",
                "type": type,
                "location": {"row": row, "col": col + 1},
            }

            # "<name>("
            col += 2
            print(lexeme[col])

            # count parameter
            num_param: int = 0
            while lexeme[col] != ")":
                num_param += 1
                while lexeme[col] != "," and lexeme[col] != ")":
                    col += 1
                    if lexeme[col] == ",":
                        col += 1
                        break
            col += 1

            if lexeme[col] == "(":
                start: int = (row, col)
                temp: int = 1
                col += 1

                # finding end function body
                while temp != 2:
                    if lexeme[col] == "<newline>":
                        row += 1

                    if lexeme[col] == "(":
                        temp -= 1
                    elif lexeme[col] == ")":
                        temp += 1
                    col += 1

                end = (row, col)

                symbol_table[key]["properties"] = {
                    "num_param": num_param,
                    "start": start,
                    "end": end,
                }

        if lexeme[col] == "<newline>":
            row += 1

        col += 1

    col: int = 0
    row: int = 1
    while token[col] != "EOF":

        # Initialize variable
        if (
            token[col] == redef.ID
            and lexeme[col - 2] in datatypes
            and lexeme[col + 1] != "("
        ):
            symbol_table[lexeme[col]] = {
                "kind": redef.ID,
                "type": lexeme[col - 2],
                "properties": "hard" if lexeme[col - 3] == "hard" else None,
                "location": {"row": row, "col": col + 1},
            }

            # TYPE CHECKING: check if assignment variable is initialized
            if lexeme[col + 1] == "=" and token[col + 3] == redef.ID:
                if lexeme[col + 3] in symbol_table:
                    if (
                        symbol_table[lexeme[col]]["type"]
                        == symbol_table[lexeme[col + 3]]["type"]
                    ):
                        col += 4
                        continue
                    else:
                        output_instance.set_output(
                            f"Semantic Error: Type mismatch: '{lexeme[col + 2]}{lexeme[col + 3]}' expected type "
                            + symbol_table[lexeme[col]]["type"]
                            + " but got "
                            + symbol_table[lexeme[col + 3]]["type"]
                            + " at line "
                            + str(row)
                        )
                        return False
                else:
                    output_instance.set_output(
                        f"Semantic Error: Variable '{lexeme[col + 2]}{lexeme[col + 3]}' not initialized at line {row}"
                    )
                    return False

        # TYPE CHECKING: Updating variable
        if (
            token[col] == redef.ID
            and lexeme[col + 1] == "="
            and token[col + 3] == redef.ID
        ):
            if lexeme[col] in symbol_table and lexeme[col + 3] in symbol_table:

                # avoid immutable
                if (
                    symbol_table[lexeme[col]]["properties"] != "hard"
                    and symbol_table[lexeme[col]]["properties"] != "tulip"
                ):
                    if (
                        symbol_table[lexeme[col]]["type"]
                        == symbol_table[lexeme[col + 3]]["type"]
                    ):
                        col += 4
                        continue
                    else:
                        # ERROR - type mismatch
                        output_instance.set_output(
                            f"Semantic Error: Type mismatch: '{lexeme[col + 2]}{lexeme[col + 3]}' expected type "
                            + lexeme[col + 3]
                            + " expected "
                            + symbol_table[lexeme[col]]["type"]
                            + " but got "
                            + symbol_table[lexeme[col + 3]]["type"]
                            + " at line "
                            + str(row)
                        )
                        return False
                else:
                    # ERROR - variable is hard (constant)
                    output_instance.set_output(
                        f"Semantic Error: Cannot update immutable variable '{lexeme[col]}' at line {row}"
                    )
                    return False
            else:
                # ERROR - variable not initialized
                print(symbol_table)
                output_instance.set_output(
                    f"Semantic Error: Variable '{lexeme[col]}' not initialized at line {row}"
                )
                return False

        if lexeme[col] == "leaf":
            leaf_depth += 1

        if lexeme[col] == "fern":
            leaf_depth += 1

        if lexeme[col] == "willow":
            leaf_depth += 1

        # TODO: check num param

        if lexeme[col] == "<newline>":
            row += 1
        col += 1
