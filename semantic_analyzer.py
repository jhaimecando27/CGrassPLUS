import redef

def is_semantic_valid(output_instance: object, lexer_output: object) -> bool:
    avoid = ["<space>", "<--", "-->", "?"]
    lexer_output = [x for x in lexer_output if x[1] not in avoid]
    lexer_output.append(("EOF", "EOF"))
    token, lexeme = zip(*lexer_output)
    print(token)

    symbol_table = {}

    datatypes = ["hard", "tint", "flora", "string", "chard", "bloom"]

    # Get all functions
    row: int = 1
    col: int = 0
    while token[col] != "EOF":
        print(lexeme[col])
        if (
            token[col] == redef.ID
            and lexeme[col - 2] in datatypes
            and lexeme[col + 1] == "("
        ):
            symbol_table[lexeme[col]] = {
                "kind": "function",
                "type": lexeme[col - 2],
                "properties": None,
                "location": {"row": row, "col": col + 1},
            }
        if lexeme[col] == "<newline>":
            row += 1

        col += 1

    col: int = 0
    row: int = 1
    while token[col] != "EOF":

        # Initialize variable
        if token[col] == redef.ID and lexeme[col - 2] in datatypes:
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
                if symbol_table[lexeme[col]]["properties"] != "hard":
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
                        f"Semantic Error: Cannot update hard variable '{lexeme[col]}' at line {row}"
                    )
                    return False
            else:
                # ERROR - variable not initialized
                print(symbol_table)
                output_instance.set_output(
                    f"Semantic Error: Variable '{lexeme[col]}' not initialized at line {row}"
                )
                return False
        if lexeme[col] == "<newline>":
            row += 1
        col += 1
