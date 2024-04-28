import grammar as g
from var import add_parse_tree_node, parse_tree_root

errors: list[list[str]] = []
line_number: int = 1
index: int = 0
tokens: list[str] = []
lexemes: list[str] = []
output: object = None


def is_syntax_valid(output_instance: object, lexer_output: object) -> bool:
    """
    Check if the syntax of the code is valid
    :param output_instance: object: The output will be displayed in output/error
    :param lexer_output: object: The output from the lexical analyser (tokens: list, lexemes: list)
    :return: bool: True if the syntax is valid, False otherwise
    """
    global index, errors, line_number, tokens, lexemes, output
    output = output_instance

    avoid = ["<space>", "<--", "-->", "?"]
    lexer_output = [x for x in lexer_output if x[1] not in avoid]

    lexer_output.append(("EOF", "EOF"))

    tokens, lexemes = zip(*lexer_output)
    _check_syntax()

    if errors:
        for error in errors:
            output_instance.set_output(
                f"SyntaxAnalyser: Line {line_number} :  {error[1]} But found {error[0]}\n"
            )
        output_instance.set_output("SyntaxAnalyser: Error Found.\n")
        errors.clear()
        index = 0
        line_number = 1
        return False

    output_instance.set_output("SyntaxAnalyser: No Errors Found.\n")
    index = 0
    line_number = 1
    return True


def _is_match(_continue: bool, expected: str, node: classmethod = None) -> bool:
    """
    Check if the expected token matches the current token
    :param _continue: bool: Continue checking even if the token does not match
    :param expected: str: The expected token
    :param node: classmethod: The current node in the parse tree
    :return: bool: True if the token matches the expected token, False otherwise
    """
    global index, lexemes, tokens, errors, line_number, output

    if errors:
        return False

    while lexemes[index] == "<newline>":
        print(f"Skipping {lexemes[index]}")
        line_number += 1
        index += 1

    if g.FIRST_SET.get(expected) is not None or g.FOLLOW_SET.get(expected) is not None:
        print(f"Checking {lexemes[index]} with {expected}")
        if (
            lexemes[index] in g.FIRST_SET[expected]
            or tokens[index] in g.FIRST_SET[expected]
        ):
            print(f"Matched {lexemes[index]} with {expected}")
            # output.set_output(f"Matched {lexemes[index]} with {expected}\n")
            return True

        elif "EPSILON" in g.FIRST_SET[expected]:
            print(f"Skipping {expected} : {lexemes[index]}")
            # output.set_output(f"Skipping {expected} : {lexemes[index]}\n")
            return False

        if _continue:
            print(f"Skipping {expected}")
            # output.set_output(f"Skipping {expected}\n")
            return False

        print(f"Syntax Error: {expected} not found : {expected}")
        errors.append((lexemes[index], f"Syntax Error: Expecting {g.FIRST_SET[expected]} but found "))
        return False

    if tokens[index] == expected:
        print(f"Matched {lexemes[index]} with {expected}")
        # output.set_output(f"Matched {lexemes[index]} with {expected}\n")
        add_parse_tree_node(node, expected)
        return True
    elif lexemes[index] == expected:
        print(f"Matched {lexemes[index]} with {expected}")
        # output.set_output(f"Matched {lexemes[index]} with {expected}\n")
        add_parse_tree_node(node, expected)
        return True

    if _continue:
        print(f"Skipping {expected}")
        # output.set_output(f"Skipping {expected}\n")
        return False

    print(f"Syntax Error: Expecting {expected} : But found {lexemes[index]}")
    errors.append((lexemes[index], f"Syntax Error: Expecting {expected}"))
    return False

