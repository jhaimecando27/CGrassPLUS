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
            return True

        elif "EPSILON" in g.FIRST_SET[expected]:
            print(f"Skipping {expected} : {lexemes[index]}")
            return False

        if _continue:
            print(f"Skipping {expected}")
            return False

        print(f"Syntax Error: {expected} not found : {expected}")
        errors.append(
            (
                lexemes[index],
                f"Syntax Error: Expecting {g.FIRST_SET[expected]} but found ",
            )
        )
        return False

    elif tokens[index] == expected:
        print(f"Matched {lexemes[index]} with {expected}")
        if node is not None:
            data_node = add_parse_tree_node(node, lexemes[index])
            data_node.kind = "data"
            data_node.type = tokens[index]
        index += 1
        return True

    elif lexemes[index] == expected:
        print(f"Matched {lexemes[index]} with {expected}")
        if lexemes[index] == "#":
            if node is not None:
                id = add_parse_tree_node(node, lexemes[index] + lexemes[index + 1])
                id.set_kind(tokens[index + 1])
            index += 2
        else:
            if node is not None:
                add_parse_tree_node(node, expected)
            index += 1
        return True

    if _continue:
        print(f"Skipping {expected}")
        return False

    print(f"Syntax Error: Expecting {expected} : But found {lexemes[index]}")
    errors.append((lexemes[index], f"Syntax Error: Expecting {expected}"))
    return False

def _is_exist(expected: str) -> True:
    """
    Check if the expected token is in the current line
    :param expected: str: The expected token, can be a terminal or non-terminal
    :return: bool: True if the token is in the current line, False otherwise
    """
    global index, lexemes

    if g.FIRST_SET.get(expected) is not None:
        avoid: list[str] = g.FIRST_SET[expected]

        for word in lexemes[index:]:
            if word == "<newline>":
                return False

            if word in avoid:
                break

    else:
        words: list[str] = lexemes[index:]

        for word in words:
            if word == "<newline>":
                return False

            if word == expected:
                break

    return True


# 1
def _program(node: classmethod) -> None:
    global index

    if _is_match(False, "seed", node):
        pass

    if _is_match(True, "<global>"):
        _global(node)

    if _is_match(False, "garden"):
        child_node = add_parse_tree_node(node, "garden")

        if _is_match(False, "("):
            pass

        if _is_match(False, ")"):
            pass

        if _is_match(False, "("):
            pass
        # )

        if _is_match(True, "<statement>"):
            _statement(child_node)

        if _is_match(False, ")"):
            pass

    if _is_match(False, ";"):
        pass

    if _is_match(True, "<function>", node):
        _function(child_node)

    if _is_match(False, "plant", node):
        pass


# #2,#3: <global> -> floral <constant> <insert-variable>; <global> | EPSILON
def _global(node: classmethod) -> None:
    var_node = add_parse_tree_node(node, "<variable>")
    var_node.properties["global"] = True

    if _is_match(True, "floral"):
        pass

    if _is_match(True, "<constant>"):
        _constant(var_node)
        var_node.properties["constant"] = True
    elif lexemes[index] in g.FIRST_SET["<insert-variable>"]:
        var_node.properties["constant"] = False

    if _is_match(True, "<insert-variable>"):
        _insert_variable(var_node)

    if _is_match(True, ";"):
        pass

    if _is_match(True, "<global>", node):
        _global(node)


# #4, #5: <constant> -> hard | EPISLON
def _constant(node: classmethod) -> None:

    if _is_match(True, "hard"):
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
    stmt_node = add_parse_tree_node(node, "<statement>")

    if _is_match(True, "<constant>") or _is_match(True, "<insert-variable>"):
        stmt_node.properties["global"] = False

        if _is_match(True, "<constant>"):
            _constant(stmt_node)
            stmt_node.properties["constant"] = True
        elif lexemes[index] in g.FIRST_SET["<insert-variable>"]:
            stmt_node.properties["constant"] = False

        if _is_match(False, "<insert-variable>"):
            _insert_variable(stmt_node)

        if _is_match(False, ";"):
            pass

        if _is_match(True, "<statement>"):
            _statement(node)

    elif _is_match(True, "<i/o-statement>") and (_is_exist("mint") or _is_exist("inpetal")):
        stmt_node.kind = "i/o"
        _i_o_statement(stmt_node)

        if _is_match(False, ";"):
            pass

        if _is_match(True, "<statement>"):
            _statement(node)

    elif _is_match(True, "leaf"):
        stmt_node.kind = "if"
        leaf_node = add_parse_tree_node(stmt_node, "leaf")

        if _is_match(False, "("):
            pass

        if _is_match(False, "<condition>"):
            child_node = add_parse_tree_node(leaf_node, "<condition>")
            _condition(child_node)

        if _is_match(False, ")"):
            pass

        if _is_match(False, "("):
            pass

        if _is_match(False, "<statement>"):
            _statement(leaf_node)

        if _is_match(False, ")"):
            pass

        if _is_match(False, ";"):
            pass

        if _is_match(False, "<eleaf>"):
            _eleaf(stmt_node)

        if _is_match(False, "<else>"):
            _else(stmt_node)

        if _is_match(True, "<statement>"):
            _statement(node)

    elif _is_match(True, "<assignment>"):
        stmt_node.kind = "assignment"
        _assignment(stmt_node)

        if _is_match(False, ";"):
            pass

        if _is_match(True, "<statement>"):
            _statement(node)

    elif _is_match(True, "<iterative>"):
        stmt_node.kind = "iterative"
        _iterative(stmt_node)

        if _is_match(False, ";"):
            pass

        if _is_match(True, "<statement>"):
            _statement(node)

    elif _is_match(True, "tree"):
        tree_node = add_parse_tree_node(stmt_node, "tree")

        if _is_match(False, "("):
            pass

        if _is_match(False, "#", tree_node):
            pass

        if _is_match(True, ")"):
            pass

        if _is_match(False, "("):
            pass

        if _is_match(False, "branch", tree_node):
            pass

        if _is_match(False, "<check-branch>"):
            _check_branch(tree_node)

        if _is_match(False, ")"):
            pass

        if _is_match(False, ";"):
            pass

        if _is_match(True, "<statement>"):
            _statement(node)

    elif _is_match(True, "clear", stmt_node):

        if _is_match(False, ";"):
            pass

        if _is_match(True, "<statement>"):
            _statement(node)

    elif _is_match(True, "break", stmt_node):

        if _is_match(False, ";"):
            pass

        if _is_match(True, "<statement>"):
            _statement(node)


# #15,#16: <insert-variable> ->
# <common-type> # <common-data> <more-data> |
# <sqnc-type> # <sqnc-value> <more-sqnc>
def _insert_variable(node: classmethod) -> None:
    global index
    node.set_kind("variable")
    node.line_number = line_number

    if _is_match(True, "<common-type>"):
        _common_type(node)
        child_node = add_parse_tree_node(node, lexemes[index] + lexemes[index + 1])

        if _is_match(False, "#"):
            pass

        child_node.set_kind(tokens[index - 1])

        if _is_match(True, "<common-data>"):
            _common_data(child_node)

        if _is_match(True, "<more-data>"):
            _more_data(node)

    elif _is_match(True, "<sqnc-type>"):
        _sqnc_type(node)

        if _is_match(False, "#", node):
            pass

        if _is_match(True, "<sqnc-value>"):
            _sqnc_value(node)

        if _is_match(True, "<more-sqnc>"):
            _more_sqnc(node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-variable>"))


# #17-#21: <common-type> -> tint | flora | chard | string | bloom
def _common_type(node: classmethod) -> None:
    global index

    if _is_match(True, "tint"):
        node.set_type("int")

    elif _is_match(True, "flora"):
        node.set_type("float")

    elif _is_match(True, "chard"):
        node.set_type("char")

    elif _is_match(True, "string"):
        node.set_type("string")

    elif _is_match(True, "bloom"):
        node.set_type("bool")
    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <common-type>"))


# #22,#23: <common-data> -> = <insert-data> | EPSILON
def _common_data(node: classmethod) -> None:

    if _is_match(True, "="):
        if _is_match(False, "<insert-data>"):
            _insert_data(node)


# #24,#25: <insert-data> -> <data> | <open-parenthesis> <insert-operation>
def _insert_data(node: classmethod) -> None:
    global index

    if _is_match(True, "<data>", node):
        _data(node)

    elif _is_match(True, "<open-parenthesis>"):
        _open_parenthesis(node)

        if _is_match(True, "<insert-operation>"):
            _insert_operation(node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-data>"))


# #26,#27: <insert-operation> ->
# <arithmetic> <close-parenthesis> |
# <condition> <close-parenthesis>
def _insert_operation(node: classmethod) -> None:
    global index

    if _is_match(True, "<arithmetic>"):
        _arithmetic(node)

        if _is_match(False, "<close-parenthesis>"):
            pass

    elif _is_match(True, "<condition>"):
        _condition(node)

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
    global index, lexemes

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

        if _is_match(True, "<insert-func>"):
            _insert_func(node)

        if _is_match(True, "<indexing>"):
            _indexing(node)

        if _is_match(True, "<start-end-step>"):
            _start_end_step(node)

        if tokens[index] == "string literal" and _is_match(True, "<concatenate>"):
            _concatenate(node)

        if _is_match(True, "<operate-number>"):
            _operate_number(node)

        if _is_match(True, "<operate-logic>"):
            _operate_logic(node)

    elif _is_match(True, "lent", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)

        if _is_match(False, ")", node):
            pass

        if _is_match(True, "<operate-number>"):
            _operate_number(node)

    elif _is_match(True, "<common-type>"):
        _common_type(node)

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)

        if _is_match(True, "<concatenate>"):
            _concatenate(node)

        if _is_match(True, "<operate-number>"):
            _operate_number(node)

        if _is_match(True, "<operate-logic>"):
            _operate_logic(node)

    elif _is_match(True, "<supply-dirt>"):
        _supply_dirt(node)

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "bare", node):
        pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <data>"))


# #38,#39: <open-parenthesis> -> ( | EPSILON
def _open_parenthesis(node: classmethod) -> None:

    if _is_match(True, "("):
        pass


# )))))


# #40-#41: <close-parenthesis> -> ) | EPSILON
def _close_parenthesis(node: classmethod) -> None:

    if _is_match(True, ")"):
        pass


# #42-#43: <arithmetic> -> <tint> <operate-number> | <flora> <operate-number>
def _arithmetic(node: classmethod) -> None:
    global index

    if _is_match(True, "<tint>"):
        _tint(node)

        if _is_match(True, "<operate-number>"):
            _operate_number(node)

    elif _is_match(True, "<flora>"):
        _flora(node)

        if _is_match(True, "<operate-number>"):
            _operate_number(node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <arithmetic>"))


# #44-#45: <operate-number> -> <operator> <open-parenthesis> <arithmetic> <close-parenthesis> | EPSILON
def _operate_number(node: classmethod) -> None:

    if _is_match(True, "<operator>"):
        is_div = False
        if lexemes[index] == "/":
            is_div = True
        _operator(node)

        if _is_match(True, "<open-parenthesis>"):
            _open_parenthesis(node)

        if is_div and lexemes[index] == "0":
            errors.append((lexemes[index], "Syntax Error: Division by zero"))

        if _is_match(True, "<arithmetic>"):
            _arithmetic(node)

        if _is_match(True, "<close-parenthesis>"):
            _close_parenthesis(node)


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

        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "tint", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "#", node):
        if _is_match(True, "<insert-func>"):
            _insert_func(node)

        if _is_match(True, "<indexing>"):
            _indexing(node)

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

        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "#", node):
        if _is_match(True, "<insert-func>"):
            _insert_func(node)

        if _is_match(True, "<indexing>"):
            _indexing(node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <flora>"))


def _concatenate(node: classmethod) -> None:
    if _is_match(True, "<indexing>"):
        _indexing(node)

        if _is_match(False, "+", node):
            pass

        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)

        if _is_match(True, "<concatenate>"):
            _concatenate(node)


# #60-#61: <condition> ->
# <data> <operate-logic> |
# <sequence> <operate-logic>
def _condition(node: classmethod) -> None:
    global index

    if _is_match(True, "<data>"):
        _data(node)

        if _is_match(True, "<operate-logic>"):
            _operate_logic(node)

    elif _is_match(True, "<sequence>"):
        _sequence(node)

        if _is_match(True, "<operate-logic>"):
            _operate_logic(node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <condition>"))


# #62-#63: <operate-logic> -> <cond-operator> <open-parenthesis> <condition> <close-parenthesis> | EPSILON
def _operate_logic(node: classmethod) -> None:
    global index

    if _is_match(True, "<cond-operator>"):
        _cond_operator(node)
        is_true = False

        if lexemes[index] == "(":
            is_true = True

        if _is_match(True, "<open-parenthesis>"):
            _open_parenthesis(node)

        if _is_match(True, "<condition>"):
            _condition(node)

        if is_true and _is_match(True, "<close-parenthesis>"):
            _close_parenthesis(node)


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
        if _is_match(True, "<argument>"):
            _argument(node)

        if _is_match(False, ")", node):
            pass

        if _is_match(True, "<instance-grab>"):
            _instance_grab(node)


# #79-#80: <instance-grab> -> .# | EPSILON
def _instance_grab(node: classmethod) -> None:

    if _is_match(True, ".", node):
        if _is_match(True, "#", node):
            pass


# #81-#82: <indexing> -> [<insert-index>] <indexing> | EPSILON
def _indexing(node: classmethod) -> None:

    if _is_match(True, "[", node):
        if _is_match(True, "<insert-index>"):
            _insert_index(node)

        if _is_match(True, "]", node):
            pass

        if _is_match(True, "<indexing>"):
            _indexing(node)


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

    if _is_match(True, ","):
        if _is_match(True, "<common-data>"):
            _common_data(node)

        if _is_match(True, "<more-data>"):
            _more_data(node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<common-data>"):
            _common_data(node)

        if _is_match(True, "<more-data>"):
            _more_data(node)


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
        if _is_match(True, "<sequence>"):
            _sequence(node)


# #93-#96: <sequence> ->
# <supply-dirt> ( <all-type-value> ) |
# <sqnc-type> ( <all-type-value> ) |
# # <insert-func> <indexing> <start-end-step>
def _sequence(node: classmethod) -> None:
    global index

    if _is_match(True, "<supply-dirt>"):
        _supply_dirt(node)

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "<sqnc-type>"):
        _sqnc_type(node)

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "#", node):
        if _is_match(True, "<insert-func>"):
            _insert_func(node)

        if _is_match(True, "<indexing>"):
            _indexing(node)

        if _is_match(True, "<start-end-step>"):
            _start_end_step(node)

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
        if _is_match(True, "<sqnc-type>"):
            _sqnc_type(node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<sqnc-value>"):
            _sqnc_value(node)

        if _is_match(True, "<more-sqnc>"):
            _more_sqnc(node)


# #105-#106: <insert-sqnc> ->
# <data> <next-sqnc> |
# <open> <insert-sqnc> <close> <next-sqnc>
def _insert_sqnc(node: classmethod) -> None:

    if _is_match(True, "<data>"):
        _data(node)

        if _is_match(True, "<next-sqnc>"):
            _next_sqnc(node)

    elif _is_match(True, "<open>"):
        _open(node)

        if _is_match(True, "<insert-sqnc>"):
            _insert_sqnc(node)

        if _is_match(True, "<close>"):
            _close(node)

        if _is_match(True, "<next-sqnc>"):
            _next_sqnc(node)


# #107-#108: <next-sqnc> -> , <dirt> <insert-sqnc> | EPSILON
def _next_sqnc(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "<dirt>"):
            _dirt(node)

        if _is_match(True, "<insert-sqnc>"):
            _insert_sqnc(node)


# #109-#110: <start-end-step> -> [ <insert-start> | EPSILON
def _start_end_step(node: classmethod) -> None:

    if _is_match(True, "[", node):
        if _is_match(True, "<insert-start>"):
            _insert_start(node)


# ]]
# #111-#112: <insert-start> -> 'tint literal':  <close-start> | : <skip-start>
def _insert_start(node: classmethod) -> None:
    global index

    if _is_match(True, "tint literal", node):
        pass

        if _is_match(True, ":", node):
            pass

        if _is_match(True, "<close-start>"):
            _close_start(node)

    elif _is_match(True, ":", node):
        pass

        if _is_match(True, "<skip-start>"):
            _skip_start(node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-start>"))


# #113-#114: <close-start> -> <close-end> | 'tint literal' <close-end>
def _close_start(node: classmethod) -> None:

    if _is_match(True, "<close-end>"):
        _close_end(node)

    elif _is_match(True, "tint literal", node):

        if _is_match(True, "<close-end>"):
            _close_end(node)


# #115-116: <close-end> -> ] <start-end-step> | : 'tint literal' <start-end-step>
def _close_end(node: classmethod) -> None:

    if _is_match(True, "]", node):
        if _is_match(True, "<start-end-step>"):
            _start_end_step(node)

    elif _is_match(True, ":", node):
        if _is_match(True, "tint literal", node):
            if _is_match(True, "<start-end-step>"):
                _start_end_step(node)


# #117-#118: <skip-start> ->
# 'tint literal' <close-end> <start-end-step> |
# : 'tint literal' ] <start-end-step>
def _skip_start(node: classmethod) -> None:

    if _is_match(True, "tint literal", node):
        if _is_match(True, "<close-end>"):
            _close_end(node)

        if _is_match(True, "<start-end-step>"):
            _start_end_step(node)

    elif _is_match(True, ":", node):
        if _is_match(True, "tint literal", node):
            if _is_match(True, "<close-end>"):
                _close_end(node)

            if _is_match(True, "<start-end-step>"):
                _start_end_step(node)


# #119-#121: <all-type-value> ->
# <insert-data> |
# <sequence> |
# inpetal ('string literal')
def _all_type_value(node: classmethod) -> None:
    global index

    if _is_match(True, "<insert-data>"):
        _insert_data(node)

    elif _is_match(True, "<sequence>"):
        _sequence(node)

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

    if _is_match(True, "<insert-inpetal>"):
        _insert_inpetal(node)

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

        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)

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

    if _is_match(True, "<common-type>"):
        _common_type(node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "=", node):
            pass

    elif _is_match(True, "<sqnc-type>"):
        _sqnc_type(node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "=", node):
            pass

    elif _is_match(True, "#", node):
        if _is_match(True, "<insert-func>"):
            _insert_func(node)

        if _is_match(True, "<indexing>"):
            _indexing(node)

        if _is_match(True, "<start-end-step>"):
            _start_end_step(node)

        if _is_match(True, "<more-id>"):
            _more_id(node)

        if _is_match(True, "<assignment-op>"):
            _assignment_op(node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-inpetal>"))


# #127-#128: <more-id> ->
# , # <insert-func> <indexing> <start-end-step> <more-id> |
# EPSILON
def _more_id(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<insert-func>"):
            _insert_func(node)

        if _is_match(True, "<indexing>"):
            _indexing(node)

        if _is_match(True, "<start-end-step>"):
            _start_end_step(node)

        if _is_match(True, "<more-id>"):
            _more_id(node)


# #129-#130: <eleaf> -> eleaf (<condition>) (<statement>); <eleaf> | EPSILON
def _eleaf(node: classmethod) -> None:

    if _is_match(True, "eleaf"):
        eleaf_node = add_parse_tree_node(node, "eleaf")
        eleaf_node.set_kind("elif")

        if _is_match(False, "("):
            pass

        if _is_match(True, "<condition>"):
            child_node = add_parse_tree_node(eleaf_node, "<condition>")
            _condition(child_node)

        if _is_match(False, ")"):
            pass

        if _is_match(False, "("):
            pass

        if _is_match(True, "<statement>"):
            _statement(eleaf_node)

        if _is_match(False, ")"):
            pass

        if _is_match(False, ";"):
            pass

        if _is_match(True, "<eleaf>"):
            _eleaf(node)


# #131-#132: <else> -> moss (<statement>); | EPSILON
def _else(node: classmethod) -> None:

    if _is_match(True, "moss"):
        moss_node = add_parse_tree_node(node, "moss")
        moss_node.set_kind("else")

        if _is_match(False, "("):
            pass

        if _is_match(True, "<statement>"):
            _statement(moss_node)

        if _is_match(False, ")"):
            pass

        if _is_match(False, ";"):
            pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <else>"))


# #133-#134: <assignment> -> <insert-inpetal> <all-type-value> | <assign> <insert-assign>
def _assignment(node: classmethod) -> None:
    global index

    if _is_match(True, "<insert-inpetal>"):
        _insert_inpetal(node)

        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)

    elif _is_match(True, "<assign>"):
        _assign(node)

        if _is_match(True, "<insert-assign>"):
            _insert_assign(node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <assignment>"))


# #135-#136: <assign> -> <insert-inpetal> | EPSILON
def _assign(node: classmethod) -> None:

    if _is_match(True, "<insert-inpetal>"):
        _insert_inpetal(node)


# #137-#138: <insert-assign> ->
# <common-type> (<all-type-value>) |
# <sqnc-type> (<all-type-value>)
def _insert_assign(node: classmethod) -> None:
    global index

    if _is_match(True, "<common-type>"):
        _common_type(node)

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)

        if _is_match(False, ")", node):
            pass

    elif _is_match(True, "<sqnc-type>"):
        _sqnc_type(node)

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)

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

    if _is_match(True, "fern"):
        fern_node = add_parse_tree_node(node, "fern")
        fern_node.kind = "for"

        if _is_match(False, "("):
            pass

        if _is_match(False, "<insert-fern>"):
            _insert_fern(fern_node)

    elif _is_match(True, "willow"):
        willow_node = add_parse_tree_node(node, "willow")
        willow_node.kind = "while"

        if _is_match(False, "("):
            pass

        if _is_match(True, "<condition>"):
            child_node = add_parse_tree_node(willow_node, "<condition>")
            _condition(child_node)

        if _is_match(False, ")"):
            pass

        if _is_match(False, "("):
            pass

        if _is_match(True, "<statement>"):
            _statement(willow_node)

        if _is_match(False, ")"):
            pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <iterative>"))


# )))


# #149-#150: <insert-fern> ->
# tint # = 'tint literal'; <condition>; # <assignment-op> <tint>;)(<statement>) |
# <all-type-value> <more-value> at <sequence>;) (<statement>)
def _insert_fern(node: classmethod) -> None:
    global index

    if _is_match(True, "tint"):
        child_node = add_parse_tree_node(node, "<condition>")
        add_parse_tree_node(child_node, "tint")

        if _is_match(False, "#", child_node):
            pass

        if _is_match(False, "=", child_node):
            pass

        if _is_match(False, "tint literal", child_node):
            pass

        if _is_match(False, ";", child_node):
            pass

        if _is_match(False, "<condition>"):
            _condition(child_node)

        if _is_match(False, ";", child_node):
            pass

        if _is_match(False, "#", child_node):
            pass

        if _is_match(False, "<assignment-op>"):
            _assignment_op(child_node)

        if _is_match(False, "tint literal", child_node):
            pass

        if _is_match(False, ";", child_node):
            pass

        if _is_match(False, ")"):
            pass

        if _is_match(True, "("):
            pass

        if _is_match(True, "<statement>"):
            _statement(node)

        if _is_match(False, ")"):
            pass

    elif _is_match(True, "<all-type-value>"):
        child_node = add_parse_tree_node(node, "<condition>")
        _all_type_value(child_node)

        if _is_match(True, "<more-value>"):
            _more_value(child_node)

        if _is_match(True, "at", child_node):
            pass

        if _is_match(True, "<sequence>"):
            _sequence(child_node)

        if _is_match(False, ";", child_node):
            pass

        if _is_match(False, "("):
            pass

        if _is_match(True, "<statement>", node):
            _statement(node)

        if _is_match(False, ")"):
            pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-fern>"))


# #151-#152: <more-value> -> , <all-type-value> <more-value> | EPSILON
def _more_value(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)

        if _is_match(True, "<more-value>"):
            _more_value(node)


# #153-#154: <check-branch> ->
# <all-type-value> <insert-branch> <more-branch> |
# _:<statement>
def _check_branch(node: classmethod) -> None:
    global index

    if _is_match(True, "<all-type-value>"):
        _all_type_value(node)

        if _is_match(True, "<insert-branch>"):
            _insert_branch(node)

        if _is_match(True, "<more-branch>"):
            _more_branch(node)

    elif _is_match(True, "_", node):
        if _is_match(True, ":", node):
            if _is_match(True, "<statement>"):
                _statement(node)

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <check-branch>"))


# #155-#156: <insert-branch> -> : <statement> | leaf ( <condition> ) ( <statement> );
def _insert_branch(node: classmethod) -> None:
    global index

    if _is_match(True, ":", node):
        if _is_match(True, "<statement>"):
            _statement(node)

    elif _is_match(True, "leaf", node):
        leaf_node = add_parse_tree_node(node, "leaf")

        if _is_match(False, "("):
            pass

        if _is_match(True, "<condition>"):
            child_node = add_parse_tree_node(leaf_node, "<condition>")
            _condition(child_node)

        if _is_match(False, ")"):
            pass

        if _is_match(False, "("):
            pass

        if _is_match(True, "<statement>"):
            _statement(leaf_node)

        if _is_match(False, ")"):
            pass

        if _is_match(False, ";", leaf_node):
            pass

    else:
        errors.append((lexemes[index], "Syntax Error: Expecting <insert-branch>"))


# #157-#158: <more-branch> -> , branch <check-branch> | EPSILON
def _more_branch(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "branch", node):
            pass

        if _is_match(True, "<check-branch>"):
            _check_branch(node)


# #159-#161: <argument> ->
# <insert-argument> |
# <common-type> # <common-data> <more**kwargs> |
# EPSILON
def _argument(node: classmethod) -> None:

    if _is_match(True, "<insert-argument>"):
        _insert_argument(node)

    elif _is_match(True, "<common-type>"):
        _common_type(node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<common-data>"):
            _common_data(node)

        if _is_match(True, "<more**kwargs>"):
            _more_kwargs(node)

    elif _is_match(True, "EPSILON", node):
        pass


# #162-#164: <insert-argument> ->
# <all-type-value> <add-argument> |
# # ( <argument> ) <add-argument> |
# EPSILON
def _insert_argument(node: classmethod) -> None:

    if _is_match(True, "<all-type-value>"):
        _all_type_value(node)

        if _is_match(True, "<add-argument>"):
            _add_argument(node)

    elif _is_match(True, "#", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<argument>"):
            _argument(node)

        if _is_match(False, ")", node):
            pass

        if _is_match(True, "<add-argument>"):
            _add_argument(node)


# #165-#166: <add-argument> -> , <argument> | EPSILON
def _add_argument(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "<argument>"):
            _argument(node)


# #167-#168: <more**kwargs> -> , <common-type> # <common-data> <more**kwargs> | EPSILON
def _more_kwargs(node: classmethod) -> None:

    if _is_match(True, ",", node):
        if _is_match(True, "<common-type>"):
            _common_type(node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<common-data>"):
            _common_data(node)

        if _is_match(True, "<more**kwargs>"):
            _more_kwargs(node)


# #169-#171: <function> ->
# <common-type> # ( <parameter> ) ( <statement> regrow <all-type-value> <add-at> ; ) ; <function> |
# viola # ( <undefined-param> ) ( <statement> ); <function> |
# EPSILON
def _function(node: classmethod) -> None:
    global index

    func_node = add_parse_tree_node(node, "<function>")

    if _is_match(True, "<common-type>"):
        _common_type(func_node)

        if _is_match(True, "#", func_node):
            pass

        if _is_match(False, "("):
            pass

        if _is_match(True, "<parameter>"):
            child_node = add_parse_tree_node(func_node, "<parameter>")
            _parameter(child_node)

        if _is_match(False, ")"):
            pass

        if _is_match(False, "(", func_node):
            pass

        if _is_match(True, "<statement>"):
            _statement(func_node)

        if _is_match(True, "regrow"):
            pass

        if _is_match(True, "<all-type-value>"):
            _all_type_value(func_node)

        if _is_match(True, "<add-at>"):
            _add_at(node)

        if _is_match(False, ";", func_node):
            pass

        if _is_match(False, ")", func_node):
            pass

        if _is_match(False, ";", func_node):
            pass

        if _is_match(True, "<function>", node):
            _function(node)

    elif _is_match(True, "viola", func_node):

        if _is_match(False, "#", func_node):
            pass

        if _is_match(False, "("):
            pass

        if _is_match(True, "<undefined-param>"):
            child_node = add_parse_tree_node(func_node, "<undefined-param>")
            _undefined_param(child_node)

        if _is_match(False, ")", func_node):
            pass

        if _is_match(False, "(", func_node):
            pass

        if _is_match(True, "<statement>"):
            _statement(func_node)

        if _is_match(False, ")", func_node):
            pass

        if _is_match(False, ";", func_node):
            pass

        if _is_match(True, "<function>"):
            _function(node)


# #172-#173: <add-at> -> <more-value> at <all-type-value> | EPSILON
def _add_at(node: classmethod) -> None:

    if _is_match(True, "<more-value>"):
        _more_value(node)

        if _is_match(True, "at", node):
            pass

        if _is_match(True, "<all-type-value>"):
            _all_type_value(node)


# #174-#178: <parameter> ->
# <undefined-param> |
# <common-type> # <common-data> <next-parameter> |
# <sqnc-type> # <sqnc-value> <next-parameter> |
# # ( <parameter> ) <next-parameter> | EPSILON
def _parameter(node: classmethod) -> None:
    global index

    if _is_match(True, "<undefined-param>") and lexemes[index + 1] == "*":
        _undefined_param(node)

    elif _is_match(True, "<common-type>"):
        _common_type(node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<common-data>"):
            _common_data(node)

        if _is_match(True, "<next-parameter>"):
            _next_parameter(node)

    elif _is_match(True, "<sqnc-type>"):
        _sqnc_type(node)

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<sqnc-value>"):
            _sqnc_value(node)

        if _is_match(True, "<next-parameter>"):
            _next_parameter(node)

    elif _is_match(True, "#", node):

        if _is_match(False, "(", node):
            pass

        if _is_match(True, "<parameter>"):
            _parameter(node)

        if _is_match(False, ")", node):
            pass

        if _is_match(True, "<next-parameter>"):
            _next_parameter(node)


# #179-#180: <undefined-param> -> <common-type> *# <add-kwargs>
def _undefined_param(node: classmethod) -> None:

    if _is_match(False, "<common-type>"):
        _common_type(node)

        if _is_match(True, "*", node):
            pass

        if _is_match(True, "#", node):
            pass

        if _is_match(True, "<add-kwargs>"):
            _add_kwargs(node)


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
        if _is_match(True, "<parameter>"):
            _parameter(node)
