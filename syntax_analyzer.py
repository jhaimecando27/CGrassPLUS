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
    _program(parse_tree_root)

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

    if expected in g.FIRST_SET:
        print(f"Checking {lexemes[index]} with {expected}")
        if (
            lexemes[index] in g.FIRST_SET[expected]
            or tokens[index] in g.FIRST_SET[expected]
        ):
            print(f"Matched {lexemes[index]} with {expected}")
            output.set_output(f"Matched {lexemes[index]} with {expected}\n")
            return True

        elif "EPSILON" in g.FIRST_SET[expected]:
            print(f"Skipping {expected} : {lexemes[index]}")
            output.set_output(f"Skipping {expected} : {lexemes[index]}\n")
            return False

        if _continue:
            print(f"Skipping {expected}")
            output.set_output(f"Skipping {expected}\n")
            return False

        print(f"Syntax Error: {expected} not found : {expected}")
        errors.append(
            (
                lexemes[index],
                f"Syntax Error: Expecting {g.FIRST_SET[expected]} but found ",
            )
        )
        return False

    if tokens[index] == expected:
        print(f"Matched {lexemes[index]} with {expected}")
        output.set_output(f"Matched {lexemes[index]} with {expected}\n")
        add_parse_tree_node(node, expected)
        index += 1
        return True

    elif lexemes[index] == expected:
        print(f"Matched {lexemes[index]} with {expected}")
        output.set_output(f"Matched {lexemes[index]} with {expected}\n")
        if lexemes[index] == "#":
            add_parse_tree_node(node, lexemes[index] + lexemes[index + 1])
            index += 2
        else:
            add_parse_tree_node(node, expected)
            index += 1
        return True

    if _continue:
        print(f"Skipping {expected}")
        output.set_output(f"Skipping {expected}\n")
        return False

    print(f"Syntax Error: Expecting {expected} : But found {lexemes[index]}")
    errors.append((lexemes[index], f"Syntax Error: Expecting {expected}"))
    return False


# 1
def _program(node: classmethod) -> None:
    global index

    if _is_match(False, "seed", node):
        pass

    if _is_match(True, "<global>", node):
        child_node = add_parse_tree_node(node, "<global>")
        _global(child_node)

    if _is_match(False, "garden", node):
        pass

    if _is_match(False, "(", node):
        pass

    if _is_match(False, ")", node):
        pass

    if _is_match(False, "(", node):
        pass
    # )

    if _is_match(True, "<statement>", node):
        child_node = add_parse_tree_node(node, "<statement>")
        _statement(child_node)

    if _is_match(False, ")", node):
        pass

    if _is_match(False, ";", node):
        pass

    if _is_match(True, "<function>", node):
        child_node = add_parse_tree_node(node, "<function>")
        _function(child_node)

    if _is_match(False, "plant", node):
        pass


# #2,#3: <global> -> floral <constant> <insert-variable>; <global> | EPSILON
def _global(node: classmethod) -> None:

    if _is_match(True, "floral", node):
        pass

    if _is_match(True, "<constant>", node):
        child_node = add_parse_tree_node(node, "<constant>")
        _constant(child_node)

    if _is_match(True, "<insert-variable>", node):
        child_node = add_parse_tree_node(node, "<insert-variable>")
        _insert_variable(child_node)

    if _is_match(True, ";", node):
        pass

    if _is_match(True, "<global>", node):
        child_node = add_parse_tree_node(node, "<global>")
        _global(child_node)


# #4, #5: <constant> -> hard | EPISLON
def _constant(node: classmethod) -> None:

    if _is_match(True, "hard", node):
        pass


# #6-14: <satement> ->
# <constant> <insert-variable>; <statement> |
# <i/o-statement>; <statement> |
# leaf(<insert-condition>)(<filter-statement>); <eleaf> <else> <statement> |
# <assignment>; <statement> |
# <iterative>; <statement> |
# tree(#identifier)(branch <check-branch>); <statement> |
# clear; <statement> |
# break; <statement> |
# EPSILON
def _statement(node: classmethod) -> None:

    if _is_match(True, "<constant>", node) or _is_match(
        True, "<insert-variable>", node
    ):
        if _is_match(True, "<constant>", node):
            child_node = add_parse_tree_node(node, "<constant>")
            _constant(child_node)

        if _is_match(False, "<insert-variable>", node):
            child_node = add_parse_tree_node(node, "<insert-variable>")
            _insert_variable(child_node)

        if _is_match(False, ";", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

    elif _is_match(True, "<i/o-statement>", node):
        child_node = add_parse_tree_node(node, "<i/o-statement>")
        _i_o_statement(child_node)

        if _is_match(False, ";", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

    elif _is_match(True, "leaf", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(False, "<condition>", node):
            child_node = add_parse_tree_node(node, "<condition>")
            _condition(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(False, "(", node):
            pass

        if _is_match(False, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(False, ";", node):
            pass

        if _is_match(False, "<eleaf>", node):
            child_node = add_parse_tree_node(node, "<eleaf>")
            _eleaf(child_node)

        if _is_match(False, "<else>", node):
            child_node = add_parse_tree_node(node, "<else>")
            _else(child_node)

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

    elif _is_match(True, "<assignment>", node):
        child_node = add_parse_tree_node(node, "<assignment>")
        _assignment(child_node)

        if _is_match(False, ";", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

    elif _is_match(True, "<iterative>", node):
        child_node = add_parse_tree_node(node, "<iterative>")
        _iterative(child_node)

        if _is_match(False, ";", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

    elif _is_match(True, "tree", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(False, "#", node):
            pass

        if _is_match(True, ")", node):
            pass

        if _is_match(False, "branch", node):
            pass

        if _is_match(False, "<check-branch>", node):
            child_node = add_parse_tree_node(node, "<check-branch>")
            _check_branch(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(False, ";", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

    elif _is_match(True, "clear", node):

        if _is_match(False, ";", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

    elif _is_match(True, "break", node):

        if _is_match(False, ";", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)


# #15,#16: <insert-variable> ->
# <common-type> # <common-data> <more-data> |
# <sqnc-type> # <sqnc-value> <more-sqnc>
def _insert_variable(node: classmethod) -> None:
    global index

    if _is_match(True, "<common-type>", node):
        child_node = add_parse_tree_node(node, "<common-type>")
        _common_type(child_node)

        if _is_match(False, "#", node):
            pass

        if _is_match(True, "<common-data>", node):
            child_node = add_parse_tree_node(node, "<common-data>")
            _common_data(child_node)

        if _is_match(True, "<more-data>", node):
            child_node = add_parse_tree_node(node, "<more-data>")
            _more_data(child_node)

    elif _is_match(True, "<sqnc-type>", node):
        child_node = add_parse_tree_node(node, "<sqnc-type>")
        _sqnc_type(child_node)

        if _is_match(False, "#", node):
            pass

        if _is_match(True, "<sqnc-value>", node):
            child_node = add_parse_tree_node(node, "<sqnc-value>")
            _sqnc_value(child_node)

        if _is_match(True, "<more-sqnc>", node):
            child_node = add_parse_tree_node(node, "<more-sqnc>")
            _more_sqnc(child_node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-variable>"))


# #17-#21: <common-type> -> tint | flora | chard | string | bloom
def _common_type(node: classmethod) -> None:
    global index

    if _is_match(True, "tint", node):
        pass

    elif _is_match(True, "flora", node):
        pass

    elif _is_match(True, "chard", node):
        pass

    elif _is_match(True, "string", node):
        pass

    elif _is_match(True, "bloom", node):
        pass
    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <common-type>"))


# #22,#23: <common-data> -> = <insert-data> | EPSILON
def _common_data(node: classmethod) -> None:

    if _is_match(True, "=", node):
        if _is_match(False, "<insert-data>", node):
            child_node = add_parse_tree_node(node, "<insert-data>")
            _insert_data(child_node)


# #24,#25: <insert-data> -> <data> | <open-parenthesis> <insert-operation>
def _insert_data(node: classmethod) -> None:
    global index

    if _is_match(True, "<data>", node):
        child_node = add_parse_tree_node(node, "<data>")
        _data(child_node)

    elif _is_match(True, "<open-parenthesis>", node):
        child_node = add_parse_tree_node(node, "<open-parenthesis>")
        _open_parenthesis(child_node)

        if _is_match(True, "<insert-operation>", node):
            child_node = add_parse_tree_node(node, "<insert-operation>")
            _insert_operation(child_node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-data>"))


# #26,#27: <insert-operation> ->
# <arithmetic> <close-parenthesis> |
# <condition> <close-parenthesis>
def _insert_operation(node: classmethod) -> None:
    global index

    if _is_match(True, "<arithmetic>", node):
        child_node = add_parse_tree_node(node, "<arithmetic>")
        _arithmetic(child_node)

        if _is_match(False, "<close-parenthesis>", node):
            pass

    elif _is_match(True, "<condition>", node):
        child_node = add_parse_tree_node(node, "<condition>")
        _condition(child_node)

        if _is_match(False, "<close-parenthesis>", node):
            pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-operation>"))


# #28-#37: <data> ->
# "tint literal" <operate-number> |
# "flora literal" <operate-number> |
# "chard literal" |
# "string literal" |
# "bloom literal" |
# # <insert-func> <indexing> <start-end-step> <concatenate> <operate-number> <operate-logic> |
# lent(<all-type-value>) <operate-number> |
# <common-type>(<all-type-value>) <concatenate> <operate-number> <operate-logic> |
# <supply-dirt> ( <all-type-value> ) |
# bare
def _data(node: classmethod) -> None:
    global index

    print(lexemes[index + 2])
    if _is_match(True, "tint literal", node):
        pass

    elif _is_match(True, "flora literal", node):
        pass

    elif _is_match(True, "chard literal", node):
        pass

    elif _is_match(True, "string literal", node):
        pass

    elif _is_match(True, "bloom literal", node):
        pass

    elif _is_match(True, "#", node):

        if _is_match(True, "<insert-func>", node):
            child_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(child_node)

        if _is_match(True, "<indexing>", node):
            child_node = add_parse_tree_node(node, "<indexing>")
            _indexing(child_node)

        if _is_match(True, "<start-end-step>", node):
            child_node = add_parse_tree_node(node, "<start-end-step>")
            _start_end_step(child_node)

        if tokens[index] == "string literal" and _is_match(True, "<concatenate>", node):
            child_node = add_parse_tree_node(node, "<concatenate>")
            _concatenate(child_node)

        if _is_match(True, "<operate-number>", node):
            child_node = add_parse_tree_node(node, "<operate-number>")
            _operate_number(child_node)

        if _is_match(True, "<operate-logic>", node):
            child_node = add_parse_tree_node(node, "<operate-logic>")
            _operate_logic(child_node)

    elif _is_match(True, "lent", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(True, "<operate-number>", node):
            child_node = add_parse_tree_node(node, "<operate-number>")
            _operate_number(child_node)

    elif _is_match(True, "<common-type>", node):
        child_node = add_parse_tree_node(node, "<common-type>")
        _common_type(child_node)

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

        if _is_match(True, "<concatenate>", node):
            child_node = add_parse_tree_node(node, "<concatenate>")
            _concatenate(child_node)

        if _is_match(True, "<operate-number>", node):
            child_node = add_parse_tree_node(node, "<operate-number>")
            _operate_number(child_node)

        if _is_match(True, "<operate-logic>", node):
            child_node = add_parse_tree_node(node, "<operate-logic>")
            _operate_logic(child_node)

    elif _is_match(True, "<supply-dirt>", node):
        child_node = add_parse_tree_node(node, "<supply-dirt>")
        _supply_dirt(child_node)

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "bare", node):
        pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <data>"))


# #38,#39: <open-parenthesis> -> ( | EPSILON
def _open_parenthesis(node: classmethod) -> None:

    if _is_match(True, "(", node):
        pass


# )))))


# #40-#41: <close-parenthesis> -> ) | EPSILON
def _close_parenthesis(node: classmethod) -> None:

    if _is_match(True, ")", node):
        pass


# #42-#43: <arithmetic> -> <tint> <operate-number> | <flora> <operate-number>
def _arithmetic(node: classmethod) -> None:
    global index

    if _is_match(True, "<tint>", node):
        child_node = add_parse_tree_node(node, "<tint>")
        _tint(child_node)

        if _is_match(True, "<operate-number>", node):
            child_node = add_parse_tree_node(node, "<operate-number>")
            _operate_number(child_node)

    elif _is_match(True, "<flora>", node):
        child_node = add_parse_tree_node(node, "<flora>")
        _flora(child_node)

        if _is_match(True, "<operate-number>", node):
            child_node = add_parse_tree_node(node, "<operate-number>")
            _operate_number(child_node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <arithmetic>"))


# #44-#45: <operate-number> -> <operator> <open-parenthesis> <arithmetic> <close-parenthesis> | EPSILON
def _operate_number(node: classmethod) -> None:

    if _is_match(True, "<operator>", node):
        child_node = add_parse_tree_node(node, "<operator>")
        _operator(child_node)

        if _is_match(True, "<open-parenthesis>", node):
            child_node = add_parse_tree_node(node, "<open-parenthesis>")
            _open_parenthesis(child_node)

        if _is_match(True, "<arithmetic>", node):
            child_node = add_parse_tree_node(node, "<arithmetic>")
            _arithmetic(child_node)

        if _is_match(True, "<close-parenthesis>", node):
            child_node = add_parse_tree_node(node, "<close-parenthesis>")
            _close_parenthesis(child_node)


# #46-#52: <operator> -> + | - | * | / | % | ** | //
def _operator(node: classmethod) -> None:
    global index

    if _is_match(True, "+", node):
        pass

    elif _is_match(True, "-", node):
        pass

    elif _is_match(True, "*", node):
        pass

    elif _is_match(True, "/", node):
        pass

    elif _is_match(True, "%", node):
        pass

    elif _is_match(True, "**", node):
        pass

    elif _is_match(True, "//", node):
        pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <operator>"))


# 53-#56: <tint> -->
# 'tint literal' |
# lent(<all-type-value>) |
# tint(<all-type-value>) |
# # <insert-func> <indexing> <indexing>
def _tint(node: classmethod) -> None:
    global index

    if _is_match(True, "tint literal", node):
        pass

    elif _is_match(True, "lent", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "tint", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "#", node):
        if _is_match(True, "<insert-func>", node):
            child_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(child_node)

        if _is_match(True, "<indexing>", node):
            child_node = add_parse_tree_node(node, "<indexing>")
            _indexing(child_node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <tint>"))


# #57-#59: <flora> -->
# 'flora literal' |
# flora(<all-type-value>) |
# # <insert-func> <indexing> <indexing>
def _flora(node: classmethod) -> None:
    global index

    if _is_match(True, "flora literal", node):
        pass

    elif _is_match(True, "flora", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "#", node):
        if _is_match(True, "<insert-func>", node):
            child_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(child_node)

        if _is_match(True, "<indexing>", node):
            child_node = add_parse_tree_node(node, "<indexing>")
            _indexing(child_node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <flora>"))


def _concatenate(node: classmethod) -> None:
    if _is_match(True, "<indexing>", node):
        child_node = add_parse_tree_node(node, "<indexing>")
        _indexing(child_node)

        if _is_match(False, "+", node):
            pass

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

        if _is_match(True, "<concatenate>", node):
            child_node = add_parse_tree_node(node, "<concatenate>")
            _concatenate(child_node)

# #60-#61: <condition> ->
# <data> <operate-logic> |
# <sequence> <operate-logic>
def _condition(node: classmethod) -> None:
    global index

    if _is_match(True, "<data>", node):
        child_node = add_parse_tree_node(node, "<data>")
        _data(child_node)

        if _is_match(True, "<operate-logic>", node):
            child_node = add_parse_tree_node(node, "<operate-logic>")
            _operate_logic(child_node)

    elif _is_match(True, "<sequence>", node):
        child_node = add_parse_tree_node(node, "<sequence>")
        _sequence(child_node)

        if _is_match(True, "<operate-logic>", node):
            child_node = add_parse_tree_node(node, "<operate-logic>")
            _operate_logic(child_node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <condition>"))


# #62-#63: <operate-logic> -> <cond-operator> <open-parenthesis> <condition> <close-parenthesis> | EPSILON
def _operate_logic(node: classmethod) -> None:
    global index

    if _is_match(True, "<cond-operator>", node):
        child_node = add_parse_tree_node(node, "<cond-operator>")
        _cond_operator(child_node)
        is_true = False

        if lexemes[index] == "(":
            is_true = True

        if _is_match(True, "<open-parenthesis>", node):
            child_node = add_parse_tree_node(node, "<open-parenthesis>")
            _open_parenthesis(child_node)

        if _is_match(True, "<condition>", node):
            child_node = add_parse_tree_node(node, "<condition>")
            _condition(child_node)

        if is_true and _is_match(True, "<close-parenthesis>", node):
            child_node = add_parse_tree_node(node, "<close-parenthesis>")
            _close_parenthesis(child_node)


# #64-#73: <cond-operator> -> == | != | > | < | >= | <= | =& | =/ | at | nut
def _cond_operator(node: classmethod) -> None:
    global index

    if _is_match(True, "==", node):
        pass

    elif _is_match(True, "!=", node):
        pass

    elif _is_match(True, ">", node):
        pass

    elif _is_match(True, "<", node):
        pass

    elif _is_match(True, ">=", node):
        pass

    elif _is_match(True, "<=", node):
        pass

    elif _is_match(True, "=&", node):
        pass

    elif _is_match(True, "=/", node):
        pass

    elif _is_match(True, "at", node):
        pass

    elif _is_match(True, "nut", node):
        pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <cond-operator>"))


# #74-#76: <supply-dirt> -> getItems | getKeys | getValues
def _supply_dirt(node: classmethod) -> None:
    global index

    if _is_match(True, "getItems", node):
        pass

    elif _is_match(True, "getKeys", node):
        pass

    elif _is_match(True, "getValues", node):
        pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <supply-dirt>"))


# #77-#78: <insert-func> -> (<argument>) <instance-grab> | EPSILON
def _insert_func(node: classmethod) -> None:

    if _is_match(True, "(", node):
        if _is_match(True, "<argument>", node):
            child_node = add_parse_tree_node(node, "<argument>")
            _argument(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(True, "<instance-grab>", node):
            child_node = add_parse_tree_node(node, "<instance-grab>")
            _instance_grab(child_node)


# #79-#80: <instance-grab> -> .# | EPSILON
def _instance_grab(node: classmethod) -> None:

    if _is_match(True, ".", node):
        if _is_match(True, "#", node):
            pass


# #81-#82: <indexing> -> [<insert-index>] <indexing> | EPSILON
def _indexing(node: classmethod) -> None:

    if _is_match(True, "[", node):
        if _is_match(True, "<insert-index>", node):
            child_node = add_parse_tree_node(node, "<insert-index>")
            _insert_index(child_node)

        if _is_match(True, "]", node):
            pass

        if _is_match(True, "<indexing>", node):
            child_node = add_parse_tree_node(node, "<indexing>")
            _indexing(child_node)


# #83-#84: <insert-index> -> 'tint literal' | 'string literal'
def _insert_index(node: classmethod) -> None:
    global index

    if _is_match(True, "tint literal", node):
        pass

    elif _is_match(True, "string literal", node):
        pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-index>"))


# #85-#86: <more-data> -> , <common-data> <more-data> # <common-data> <more-data> | EPSILON
def _more_data(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "<common-data>", node):
            child_node = add_parse_tree_node(node, "<common-data>")
            _common_data(child_node)

        if _is_match(True, "<more-data>", node):
            child_node = add_parse_tree_node(node, "<more-data>")
            _more_data(child_node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<common-data>", node):
            child_node = add_parse_tree_node(node, "<common-data>")
            _common_data(child_node)

        if _is_match(True, "<more-data>", node):
            child_node = add_parse_tree_node(node, "<more-data>")
            _more_data(child_node)


# #87-#90: <sqnc-type> -> florist | tulip | dirt | stem
def _sqnc_type(node: classmethod) -> None:
    global index

    if _is_match(True, "florist", node):
        pass

    elif _is_match(True, "tulip", node):
        pass

    elif _is_match(True, "dirt", node):
        pass

    elif _is_match(True, "stem", node):
        pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <sqnc-type>"))


# #91-#92: <sqnc-value> -> = <sequence> | EPSILON
def _sqnc_value(node: classmethod) -> None:

    if _is_match(True, "=", node):
        if _is_match(True, "<sequence>", node):
            child_node = add_parse_tree_node(node, "<sequence>")
            _sequence(child_node)


# #93-#96: <sequence> ->
# <supply-dirt> ( <all-type-value> ) |
# <sqnc-type> ( <all-type-value> ) |
# # <insert-func> <indexing> <start-end-step>
def _sequence(node: classmethod) -> None:
    global index

    if _is_match(True, "<supply-dirt>", node):
        child_node = add_parse_tree_node(node, "<supply-dirt>")
        _supply_dirt(child_node)

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "<sqnc-type>", node):
        child_node = add_parse_tree_node(node, "<sqnc-type>")
        _sqnc_type(child_node)

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "#", node):
        if _is_match(True, "<insert-func>", node):
            child_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(child_node)

        if _is_match(True, "<indexing>", node):
            child_node = add_parse_tree_node(node, "<indexing>")
            _indexing(child_node)

        if _is_match(True, "<start-end-step>", node):
            child_node = add_parse_tree_node(node, "<start-end-step>")
            _start_end_step(child_node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <sequence>"))


# #97-#98: <open> -> [ | {
def _open(node: classmethod) -> None:
    global index

    if _is_match(True, "[", node):
        pass

    elif _is_match(True, "{", node):
        pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <open>"))


# #99-#100: <dirt> -> 'string literal' : | EPSILON
def _dirt(node: classmethod) -> None:

    if _is_match(True, "string literal", node):
        pass

        if _is_match(True, ":", node):
            pass


# #101-#102: <close> -> ] | }
def _close(node: classmethod) -> None:
    global index

    if _is_match(True, "]", node):
        pass

    elif _is_match(True, "}", node):
        pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <close>"))


# #103-#104: <more-sqnc> -> , <sqnc-type> # <sqnc-value> <more-sqnc> | EPSILON
def _more_sqnc(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "<sqnc-type>", node):
            child_node = add_parse_tree_node(node, "<sqnc-type>")
            _sqnc_type(child_node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<sqnc-value>", node):
            child_node = add_parse_tree_node(node, "<sqnc-value>")
            _sqnc_value(child_node)

        if _is_match(True, "<more-sqnc>", node):
            child_node = add_parse_tree_node(node, "<more-sqnc>")
            _more_sqnc(child_node)


# #105-#106: <insert-sqnc> ->
# <data> <next-sqnc> |
# <open> <insert-sqnc> <close> <next-sqnc>
def _insert_sqnc(node: classmethod) -> None:

    if _is_match(True, "<data>", node):
        child_node = add_parse_tree_node(node, "<data>")
        _data(child_node)

        if _is_match(True, "<next-sqnc>", node):
            child_node = add_parse_tree_node(node, "<next-sqnc>")
            _next_sqnc(child_node)

    elif _is_match(True, "<open>", node):
        child_node = add_parse_tree_node(node, "<open>")
        _open(child_node)

        if _is_match(True, "<insert-sqnc>", node):
            child_node = add_parse_tree_node(node, "<insert-sqnc>")
            _insert_sqnc(child_node)

        if _is_match(True, "<close>", node):
            child_node = add_parse_tree_node(node, "<close>")
            _close(child_node)

        if _is_match(True, "<next-sqnc>", node):
            child_node = add_parse_tree_node(node, "<next-sqnc>")
            _next_sqnc(child_node)


# #107-#108: <next-sqnc> -> , <dirt> <insert-sqnc> | EPSILON
def _next_sqnc(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "<dirt>", node):
            child_node = add_parse_tree_node(node, "<dirt>")
            _dirt(child_node)

        if _is_match(True, "<insert-sqnc>", node):
            child_node = add_parse_tree_node(node, "<insert-sqnc>")
            _insert_sqnc(child_node)


# #109-#110: <start-end-step> -> [ <insert-start> | EPSILON
def _start_end_step(node: classmethod) -> None:

    if _is_match(True, "[", node):
        if _is_match(True, "<insert-start>", node):
            child_node = add_parse_tree_node(node, "<insert-start>")
            _insert_start(child_node)


# ]]
# #111-#112: <insert-start> -> 'tint literal':  <close-start> | : <skip-start>
def _insert_start(node: classmethod) -> None:
    global index

    if _is_match(True, "tint literal", node):
        pass

        if _is_match(True, ":", node):
            pass

        if _is_match(True, "<close-start>", node):
            child_node = add_parse_tree_node(node, "<close-start>")
            _close_start(child_node)

    elif _is_match(True, ":", node):
        pass

        if _is_match(True, "<skip-start>", node):
            child_node = add_parse_tree_node(node, "<skip-start>")
            _skip_start(child_node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-start>"))


# #113-#114: <close-start> -> <close-end> | 'tint literal' <close-end>
def _close_start(node: classmethod) -> None:

    if _is_match(True, "<close-end>", node):
        child_node = add_parse_tree_node(node, "<close-end>")
        _close_end(child_node)

    elif _is_match(True, "tint literal", node):

        if _is_match(True, "<close-end>", node):
            child_node = add_parse_tree_node(node, "<close-end>")
            _close_end(child_node)


# #115-116: <close-end> -> ] <start-end-step> | : 'tint literal' <start-end-step>
def _close_end(node: classmethod) -> None:

    if _is_match(True, "]", node):
        if _is_match(True, "<start-end-step>", node):
            child_node = add_parse_tree_node(node, "<start-end-step>")
            _start_end_step(child_node)

    elif _is_match(True, ":", node):
        if _is_match(True, "tint literal", node):
            if _is_match(True, "<start-end-step>", node):
                child_node = add_parse_tree_node(node, "<start-end-step>")
                _start_end_step(child_node)


# #117-#118: <skip-start> ->
# 'tint literal' <close-end> <start-end-step> |
# : 'tint literal' ] <start-end-step>
def _skip_start(node: classmethod) -> None:

    if _is_match(True, "tint literal", node):
        if _is_match(True, "<close-end>", node):
            child_node = add_parse_tree_node(node, "<close-end>")
            _close_end(child_node)

        if _is_match(True, "<start-end-step>", node):
            child_node = add_parse_tree_node(node, "<start-end-step>")
            _start_end_step(child_node)

    elif _is_match(True, ":", node):
        if _is_match(True, "tint literal", node):
            if _is_match(True, "]", node):
                child_node = add_parse_tree_node(node, "]")
                _close_end(child_node)

            if _is_match(True, "<start-end-step>", node):
                child_node = add_parse_tree_node(node, "<start-end-step>")
                _start_end_step(child_node)


# #119-#121: <all-type-value> ->
# <insert-data> |
# <sequence> |
# inpetal ('string literal')
def _all_type_value(node: classmethod) -> None:
    global index

    if _is_match(True, "<insert-data>", node):
        child_node = add_parse_tree_node(node, "<insert-data>")
        _insert_data(child_node)

    elif _is_match(True, "<sequence>", node):
        child_node = add_parse_tree_node(node, "<sequence>")
        _sequence(child_node)

    elif _is_match(True, "inpetal", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "string literal", node):
            pass

        if _is_match(False, ")", node):
            pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <all-type-value>"))


# #122-#123: <i/o-statement> ->
# <insert-inpetal> inpetal ('string literal') |
# mint(<all-type-value>)
def _i_o_statement(node: classmethod) -> None:
    global index

    if _is_match(True, "<insert-inpetal>", node):
        child_node = add_parse_tree_node(node, "<insert-inpetal>")
        _insert_inpetal(child_node)

        if _is_match(True, "inpetal", node):

            if _is_match(False, "(", node):
                pass

            if _is_match(True, "string literal", node):
                pass

            if _is_match(False, ")", node):
                pass

    elif _is_match(True, "mint", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

        if _is_match(False, ")", node):
            pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <i/o-statement>"))


# #124-#126: <insert-inpetal> ->
# <common-type> # = |
# <sqnc-type> # = |
# # <insert-func> <indexing> <start-end-step> <more-id> <assignment-op>
def _insert_inpetal(node: classmethod) -> None:
    global index

    if _is_match(True, "<common-type>", node):
        child_node = add_parse_tree_node(node, "<common-type>")
        _common_type(child_node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "=", node):
            pass

    elif _is_match(True, "<sqnc-type>", node):
        child_node = add_parse_tree_node(node, "<sqnc-type>")
        _sqnc_type(child_node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "=", node):
            pass

    elif _is_match(True, "#", node):
        if _is_match(True, "<insert-func>", node):
            child_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(child_node)

        if _is_match(True, "<indexing>", node):
            child_node = add_parse_tree_node(node, "<indexing>")
            _indexing(child_node)

        if _is_match(True, "<start-end-step>", node):
            child_node = add_parse_tree_node(node, "<start-end-step>")
            _start_end_step(child_node)

        if _is_match(True, "<more-id>", node):
            child_node = add_parse_tree_node(node, "<more-id>")
            _more_id(child_node)

        if _is_match(True, "<assignment-op>", node):
            child_node = add_parse_tree_node(node, "<assignment-op>")
            _assignment_op(child_node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-inpetal>"))


# #127-#128: <more-id> ->
# , # <insert-func> <indexing> <start-end-step> <more-id> |
# EPSILON
def _more_id(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<insert-func>", node):
            child_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(child_node)

        if _is_match(True, "<indexing>", node):
            child_node = add_parse_tree_node(node, "<indexing>")
            _indexing(child_node)

        if _is_match(True, "<start-end-step>", node):
            child_node = add_parse_tree_node(node, "<start-end-step>")
            _start_end_step(child_node)

        if _is_match(True, "<more-id>", node):
            child_node = add_parse_tree_node(node, "<more-id>")
            _more_id(child_node)


# #129-#130: <eleaf> -> eleaf (<condition>) (<statement>); <eleaf> | EPSILON
def _eleaf(node: classmethod) -> None:

    if _is_match(True, "eleaf", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<condition>", node):
            child_node = add_parse_tree_node(node, "<condition>")
            _condition(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(False, ";", node):
            pass

        if _is_match(True, "<eleaf>", node):
            child_node = add_parse_tree_node(node, "<eleaf>")
            _eleaf(child_node)


# #131-#132: <else> -> moss (<statement>); | EPSILON
def _else(node: classmethod) -> None:

    if _is_match(True, "moss", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(False, ";", node):
            pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <else>"))


# #133-#134: <assignment> -> <insert-inpetal> <all-type-value> | <assign> <insert-assign>
def _assignment(node: classmethod) -> None:
    global index

    if _is_match(True, "<insert-inpetal>", node):
        child_node = add_parse_tree_node(node, "<insert-inpetal>")
        _insert_inpetal(child_node)

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

    elif _is_match(True, "<assign>", node):
        child_node = add_parse_tree_node(node, "<assign>")
        _assign(child_node)

        if _is_match(True, "<insert-assign>", node):
            child_node = add_parse_tree_node(node, "<insert-assign>")
            _insert_assign(child_node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <assignment>"))


# #135-#136: <assign> -> <insert-inpetal> | EPSILON
def _assign(node: classmethod) -> None:

    if _is_match(True, "<insert-inpetal>", node):
        child_node = add_parse_tree_node(node, "<insert-inpetal>")
        _insert_inpetal(child_node)


# #137-#138: <insert-assign> ->
# <common-type> (<all-type-value>) |
# <sqnc-type> (<all-type-value>)
def _insert_assign(node: classmethod) -> None:
    global index

    if _is_match(True, "<common-type>", node):
        child_node = add_parse_tree_node(node, "<common-type>")
        _common_type(child_node)

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "<sqnc-type>", node):
        child_node = add_parse_tree_node(node, "<sqnc-type>")
        _sqnc_type(child_node)

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

        if _is_match(False, ")", node):
            pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-assign>"))


# #139-#146: <assignment-op> -> = | += | -= | *= | /= | %= | **= | //=
def _assignment_op(node: classmethod) -> None:
    global index

    if _is_match(True, "=", node):
        pass

    elif _is_match(True, "+=", node):
        pass

    elif _is_match(True, "-=", node):
        pass

    elif _is_match(True, "*=", node):
        pass

    elif _is_match(True, "/=", node):
        pass

    elif _is_match(True, "%=", node):
        pass

    elif _is_match(True, "**=", node):
        pass

    elif _is_match(True, "//=", node):
        pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <assignment-op>"))


# #147-#148: <iterative> -> fern(<insert-fern> | willow (<condition>)(<statement>)
def _iterative(node: classmethod) -> None:
    global index

    if _is_match(True, "fern", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<insert-fern>", node):
            child_node = add_parse_tree_node(node, "<insert-fern>")
            _insert_fern(child_node)

    elif _is_match(True, "willow", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<condition>", node):
            child_node = add_parse_tree_node(node, "<condition>")
            _condition(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

        if _is_match(False, ")", node):
            pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <iterative>"))


# )))


# #149-#150: <insert-fern> ->
# tint # = 'tint literal'; <condition>; # <assignment-op> <tint>;)(<statement>) |
# <all-type-value> <more-value> at <sequence>;) (<statement>)
def _insert_fern(node: classmethod) -> None:
    global index

    if _is_match(True, "tint", node):

        if _is_match(False, "#", node):
            pass

        if _is_match(True, "=", node):
            pass

        if _is_match(True, "tint literal", node):
            pass

        if _is_match(False, ";", node):
            pass

        if _is_match(True, "<condition>", node):
            child_node = add_parse_tree_node(node, "<condition>")
            _condition(child_node)

        if _is_match(False, ";", node):
            pass

        if _is_match(False, "#", node):
            pass

        if _is_match(True, "<assignment-op>", node):
            child_node = add_parse_tree_node(node, "<assignment-op>")
            _assignment_op(child_node)

        if _is_match(True, "tint", node):
            pass

        if _is_match(False, ";", node):
            pass

        if _is_match(False, ")", node):
            pass

        if _is_match(True, "(", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "<all-type-value>", node):
        child_node = add_parse_tree_node(node, "<all-type-value>")
        _all_type_value(child_node)

        if _is_match(True, "<more-value>", node):
            child_node = add_parse_tree_node(node, "<more-value>")
            _more_value(child_node)

        if _is_match(True, "at", node):
            pass

        if _is_match(False, ";", node):
            pass

        if _is_match(True, "<sequence>", node):
            child_node = add_parse_tree_node(node, "<sequence>")
            _sequence(child_node)

        if _is_match(False, ";", node):
            pass

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

        if _is_match(False, ")", node):
            pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-fern>"))


# #151-#152: <more-value> -> , <all-type-value> <more-value> | EPSILON
def _more_value(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

        if _is_match(True, "<more-value>", node):
            child_node = add_parse_tree_node(node, "<more-value>")
            _more_value(child_node)


# #153-#154: <check-branch> ->
# <all-type-value> <insert-branch> <more-branch> |
# _:<statement>
def _check_branch(node: classmethod) -> None:
    global index

    if _is_match(True, "<all-type-value>", node):
        child_node = add_parse_tree_node(node, "<all-type-value>")
        _all_type_value(child_node)

        if _is_match(True, "<insert-branch>", node):
            child_node = add_parse_tree_node(node, "<insert-branch>")
            _insert_branch(child_node)

        if _is_match(True, "<more-branch>", node):
            child_node = add_parse_tree_node(node, "<more-branch>")
            _more_branch(child_node)

    elif _is_match(True, "_", node):
        if _is_match(True, ":", node):
            if _is_match(True, "<statement>", node):
                child_node = add_parse_tree_node(node, "<statement>")
                _statement(child_node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <check-branch>"))


# #155-#156: <insert-branch> -> : <statement> | leaf ( <condition> ) ( <statement> );
def _insert_branch(node: classmethod) -> None:
    global index

    if _is_match(True, ":", node):
        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

    elif _is_match(True, "leaf", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<condition>", node):
            child_node = add_parse_tree_node(node, "<condition>")
            _condition(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(False, ";", node):
            pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-branch>"))


# #157-#158: <more-branch> -> , branch <check-branch> | EPSILON
def _more_branch(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "branch", node):
            pass

        if _is_match(True, "<check-branch>", node):
            child_node = add_parse_tree_node(node, "<check-branch>")
            _check_branch(child_node)


# #159-#161: <argument> ->
# <insert-argument> |
# <common-type> # <common-data> <more**kwargs> |
# EPSILON
def _argument(node: classmethod) -> None:

    if _is_match(True, "<insert-argument>", node):
        child_node = add_parse_tree_node(node, "<insert-argument>")
        _insert_argument(child_node)

    elif _is_match(True, "<common-type>", node):
        child_node = add_parse_tree_node(node, "<common-type>")
        _common_type(child_node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<common-data>", node):
            child_node = add_parse_tree_node(node, "<common-data>")
            _common_data(child_node)

        if _is_match(True, "<more**kwargs>", node):
            child_node = add_parse_tree_node(node, "<more**kwargs>")
            _more_kwargs(child_node)

    elif _is_match(True, "EPSILON", node):
        pass


# #162-#164: <insert-argument> ->
# <all-type-value> <add-argument> |
# # ( <argument> ) <add-argument> |
# EPSILON
def _insert_argument(node: classmethod) -> None:

    if _is_match(True, "<all-type-value>", node):
        child_node = add_parse_tree_node(node, "<all-type-value>")
        _all_type_value(child_node)

        if _is_match(True, "<add-argument>", node):
            child_node = add_parse_tree_node(node, "<add-argument>")
            _add_argument(child_node)

    elif _is_match(True, "#", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<argument>", node):
            child_node = add_parse_tree_node(node, "<argument>")
            _argument(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(True, "<add-argument>", node):
            child_node = add_parse_tree_node(node, "<add-argument>")
            _add_argument(child_node)


# #165-#166: <add-argument> -> , <argument> | EPSILON
def _add_argument(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "<argument>", node):
            child_node = add_parse_tree_node(node, "<argument>")
            _argument(child_node)


# #167-#168: <more**kwargs> -> , <common-type> # <common-data> <more**kwargs> | EPSILON
def _more_kwargs(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "<common-type>", node):
            child_node = add_parse_tree_node(node, "<common-type>")
            _common_type(child_node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<common-data>", node):
            child_node = add_parse_tree_node(node, "<common-data>")
            _common_data(child_node)

        if _is_match(True, "<more**kwargs>", node):
            child_node = add_parse_tree_node(node, "<more**kwargs>")
            _more_kwargs(child_node)


# #169-#171: <function> ->
# <common-type> # ( <parameter> ) ( <statement> regrow <all-type-value> <add-at> ; ) ; <function> |
# viola # ( <undefined-param> ) ( <statement> ); <function> |
# EPSILON
def _function(node: classmethod) -> None:

    if _is_match(True, "<common-type>", node):
        child_node = add_parse_tree_node(node, "<common-type>")
        _common_type(child_node)

        if _is_match(True, "#", node):
            pass

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<parameter>", node):
            child_node = add_parse_tree_node(node, "<parameter>")
            _parameter(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

        if _is_match(True, "regrow", node):
            pass

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)

        if _is_match(True, "<add-at>", node):
            child_node = add_parse_tree_node(node, "<add-at>")
            _add_at(child_node)

        if _is_match(False, ";", node):
            pass

        if _is_match(False, ")", node):
            pass

        if _is_match(False, ";", node):
            pass

        if _is_match(True, "<function>", node):
            child_node = add_parse_tree_node(node, "<function>")
            _function(child_node)

    elif _is_match(True, "viola", node):

        if _is_match(False, "#", node):
            pass

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<undefined-param>", node):
            child_node = add_parse_tree_node(node, "<undefined-param>")
            _undefined_param(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<statement>", node):
            child_node = add_parse_tree_node(node, "<statement>")
            _statement(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(False, ";", node):
            pass

        if _is_match(True, "<function>", node):
            child_node = add_parse_tree_node(node, "<function>")
            _function(child_node)


# #172-#173: <add-at> -> <more-value> at <all-type-value> | EPSILON
def _add_at(node: classmethod) -> None:

    if _is_match(True, "<more-value>", node):
        child_node = add_parse_tree_node(node, "<more-value>")
        _more_value(child_node)

        if _is_match(True, "at", node):
            pass

        if _is_match(True, "<all-type-value>", node):
            child_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(child_node)


# #174-#178: <parameter> ->
# <undefined-param> |
# <common-type> # <common-data> <next-parameter> |
# <sqnc-type> # <sqnc-value> <next-parameter> |
# # ( <parameter> ) <next-parameter> | EPSILON
def _parameter(node: classmethod) -> None:
    global index

    if _is_match(True, "<undefined-param>", node) and lexemes[index + 1] == "*":
        child_node = add_parse_tree_node(node, "<undefined-param>")
        _undefined_param(child_node)

    elif _is_match(True, "<common-type>", node):
        child_node = add_parse_tree_node(node, "<common-type>")
        _common_type(child_node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<common-data>", node):
            child_node = add_parse_tree_node(node, "<common-data>")
            _common_data(child_node)

        if _is_match(True, "<next-parameter>", node):
            child_node = add_parse_tree_node(node, "<next-parameter>")
            _next_parameter(child_node)

    elif _is_match(True, "<sqnc-type>", node):
        child_node = add_parse_tree_node(node, "<sqnc-type>")
        _sqnc_type(child_node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<sqnc-value>", node):
            child_node = add_parse_tree_node(node, "<sqnc-value>")
            _sqnc_value(child_node)

        if _is_match(True, "<next-parameter>", node):
            child_node = add_parse_tree_node(node, "<next-parameter>")
            _next_parameter(child_node)

    elif _is_match(True, "#", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<parameter>", node):
            child_node = add_parse_tree_node(node, "<parameter>")
            _parameter(child_node)

        if _is_match(False, ")", node):
            pass

        if _is_match(True, "<next-parameter>", node):
            child_node = add_parse_tree_node(node, "<next-parameter>")
            _next_parameter(child_node)


# #179-#180: <undefined-param> -> <common-type> *# <add-kwargs>
def _undefined_param(node: classmethod) -> None:

    if _is_match(False, "<common-type>", node):
        child_node = add_parse_tree_node(node, "<common-type>")
        _common_type(child_node)

        if _is_match(True, "*", node):
            pass

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<add-kwargs>", node):
            child_node = add_parse_tree_node(node, "<add-kwargs>")
            _add_kwargs(child_node)


# #181-#182: <add-kwargs> -> , **# | EPSILON
def _add_kwargs(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "**", node):
            pass

        if _is_match(True, "#", node):
            pass


# #183-#184: <next-parameter> -> , <parameter> | EPSILON
def _next_parameter(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "<parameter>", node):
            child_node = add_parse_tree_node(node, "<parameter>")
            _parameter(child_node)
