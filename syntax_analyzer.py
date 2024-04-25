import grammar as g
from var import add_parse_tree_node, parse_tree_root

errors: list[list[str]] = []
line_number: int = 1
index: int = 0
tokens: list[str] = []
lexemes: list[str] = []
output: object = None


def is_syntax_valid(output_instance: object, lexer_output: object) -> bool:
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


def _find_future(expected: str) -> True:
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


def _get_error(expected: str) -> None:
    global index, lexemes, errors

    if g.FIRST_SET.get(expected):
        if "EPSILON" in g.FIRST_SET[expected]:
            return
        else:
            print(f"Syntax Error: {expected} not found")
            errors.append((lexemes[index], f"Syntax Error: {expected} not found"))

    elif lexemes[index] != expected:
        print(f"Syntax Error: {expected} not found")
        errors.append((lexemes[index], f"Syntax Error: {expected} not found"))

    return


# 1: program
def _check_syntax() -> None:
    node = parse_tree_root
    global index

    if _is_match(False, "seed", node):
        index += 1

    # 2
    if _is_match(True, "<global>"):
        global_node = add_parse_tree_node(node, "<global>")
        _global(global_node, node)

    # ----- GARDEN: START ----- #

    if _is_match(False, "garden", node):
        index += 1

    if _is_match(False, "(", node):
        index += 1

    if _is_match(False, ")", node):
        index += 1

    if _is_match(False, "(", node):
        index += 1

    if _is_match(True, "<statement>"):
        statement_node = add_parse_tree_node(node, "<statement>")
        _statement(statement_node, node)

    if _is_match(False, ")", node):
        index += 1

    if _is_match(False, ";", node):
        index += 1

    # ----- GARDEN: END ----- #

    if _is_match(True, "<function>"):
        function_node = add_parse_tree_node(node, "<function>")
        _function(function_node, node)

    if _is_match(False, "plant", node):
        index += 1

    return


# 2
def _global(node: classmethod, prev_node: classmethod) -> None:
    global index

    add_parse_tree_node(node, lexemes[index])
    index += 1

    # 4
    if _is_match(True, "<constant>"):
        constant_node = add_parse_tree_node(node, "<constant>")
        _constant(constant_node, node)

    # 16-21
    if _is_match(True, "<insert-variable>"):
        insert_variable_node = add_parse_tree_node(node, "<insert-variable>")
        _insert_variable(insert_variable_node, node)

    if _is_match(False, ";", node):
        index += 1

    if _is_match(True, "<global>"):
        global_node = add_parse_tree_node(prev_node, "<global>")
        _global(global_node, prev_node)

    # 3: EPSILON
    return


# 4
def _constant(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "hard", node):
        index += 1

    # 5: EPSILON
    return


# 6
def _statement(node: classmethod, prev_node: classmethod) -> None:
    global index
    # Note: Have _2D_statement() & _3D_statement(), modifying this method need
    # to be done to both _2D_statement() and _3D_statement() methods

    avoid = [")", ";"]

    if _is_match(True, "<use-tree>") and lexemes[index] == "tree":
        new_node = add_parse_tree_node(node, "<use-tree>")
        _use_tree(new_node, node)

    if _is_match(True, "<filter-statement>"):
        new_node = add_parse_tree_node(node, "<filter-statement>")
        _filter_statement(new_node, node)

    return


# 8-15
def _filter_statement(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 8
    if (_is_match(True, "<constant>") or _is_match(True, "<insert-variable>")) and not _find_future("inpetal"):

        if _is_match(True, "<constant>"):
            new_node = add_parse_tree_node(node, "<constant>")
            _constant(new_node, node)

        if _is_match(True, "<insert-variable>"):
            new_node = add_parse_tree_node(node, "<insert-variable>")
            _insert_variable(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-statement>"):
            new_node = add_parse_tree_node(prev_node, "<filter-statement>")
            _filter_statement(new_node, prev_node)
        return

    # 11
    elif _is_match(True, "#") and lexemes[index + 2] == "(":
        index += 2

        if _is_match(True, "<check-func>"):
            new_node = add_parse_tree_node(node, "<check-func>")
            _check_func(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-statement>"):
            new_node = add_parse_tree_node(prev_node, "<filter-statement>")
            _filter_statement(new_node, node)
        return

    # 9
    elif _is_match(True, "<i/o-statement>") and (_find_future("inpetal") or _find_future("mint")):

        if _is_match(True, "<i/o-statement>"):
            new_node = add_parse_tree_node(node, "<i/o-statement>")
            _i_o_statement(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-statement>"):
            new_node = add_parse_tree_node(prev_node, "<filter-statement>")
            _filter_statement(new_node, node)
        return

    # 10
    elif _is_match(True, "leaf", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<bloom>"):
            new_node = add_parse_tree_node(node, "<bloom>")
            _bloom(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-statement>"):
            new_node = add_parse_tree_node(prev_node, "<filter-statement>")
            _filter_statement(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<eleaf>"):
            new_node = add_parse_tree_node(node, "<eleaf>")
            _eleaf(new_node, node)

        if _is_match(True, "<else>"):
            new_node = add_parse_tree_node(node, "<else>")
            _else(new_node, node)

        if _is_match(True, "<filter-statement>"):
            new_node = add_parse_tree_node(prev_node, "<filter-statement>")
            _filter_statement(new_node, node)
        return

    # 11
    elif _is_match(True, "<assignment>"):

        new_node = add_parse_tree_node(node, "<assignment>")
        _assignment(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-statement>"):
            new_node = add_parse_tree_node(prev_node, "<filter-statement>")
            _filter_statement(new_node, node)
        return

    # 12
    elif _is_match(True, "<iterative>"):
        new_node = add_parse_tree_node(node, "<iterative>")
        _iterative(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-statement>"):
            new_node = add_parse_tree_node(prev_node, "<filter-statement>")
            _filter_statement(new_node, node)
        return

    # 13
    elif _is_match(True, "clear", node):
        index += 1

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-statement>"):
            new_node = add_parse_tree_node(prev_node, "<filter-statement>")
            _filter_statement(new_node, node)
        return

    # 14
    elif _is_match(True, "break", node):
        index += 1

        if _is_match(False, ";", node):
            index += 1
        return

    # 15: EPSILON
    return


# 16-21
def _insert_variable(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 16: tint
    if _is_match(True, "tint", node):
        index += 1

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        # <tint-value>
        if _is_match(True, "<tint-value>"):
            new_node = add_parse_tree_node(node, "<tint-value>")
            _tint_value(new_node, node)

        # <more-tint>
        if _is_match(True, "<more-tint>"):
            new_node = add_parse_tree_node(node, "<more-tint>")
            _more_tint(new_node, node)

        return

    # 17: flora
    elif _is_match(True, "flora", node):
        index += 1

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        # <flora-value>
        if _is_match(True, "<flora-value>"):
            new_node = add_parse_tree_node(node, "<flora-value>")
            _flora_value(new_node, node)

        # <more-flora>
        if _is_match(True, "<more-flora>"):
            new_node = add_parse_tree_node(node, "<more-flora>")
            _more_flora(new_node, node)

        return

    # 18: chard
    elif _is_match(True, "chard", node):
        index += 1

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        # <chard-value>
        if _is_match(True, "<chard-value>"):
            new_node = add_parse_tree_node(node, "<chard-value>")
            _chard_value(new_node, node)

        # <more-chard>
        if _is_match(True, "<more-chard>"):
            new_node = add_parse_tree_node(node, "<more-chard>")
            _more_chard(new_node, node)

        return

    # 19: string
    elif _is_match(True, "string", node):
        index += 1

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        # <string-value>
        if _is_match(False, "<string-value>"):
            new_node = add_parse_tree_node(node, "<string-value>")
            _string_value(new_node, node)

        # <more-string>
        if _is_match(True, "<more-string>"):
            new_node = add_parse_tree_node(node, "<more-string>")
            _more_string(new_node, node)

        return

    # 20: bloom
    elif _is_match(True, "bloom", node):
        index += 1

        if _is_match(False, "#", node):
            index += 2

        # <bloom-value>
        if _is_match(True, "<bloom-value>"):
            new_node = add_parse_tree_node(node, "<bloom-value>")
            _bloom_value(new_node, node)

        # <more-bloom>
        if _is_match(True, "<more-bloom>"):
            new_node = add_parse_tree_node(node, "<more-bloom>")
            _more_bloom(new_node, node)

        return

    # 21: sqnc
    elif _is_match(True, "<sqnc-type>"):
        new_node = add_parse_tree_node(node, "<sqnc-type>")
        _sqnc_type(new_node, node)

        if _is_match(False, "#", node):
            index += 2

        # <sqnc-value>
        if _is_match(True, "<sqnc-value>"):
            new_node = add_parse_tree_node(node, "<sqnc-value>")
            _sqnc_value(new_node, node)

        # <more-sqnc>
        if _is_match(True, "<more-sqnc>"):
            new_node = add_parse_tree_node(node, "<more-sqnc>")
            _more_sqnc(new_node, node)

        return

    return


# 22-25
def _sqnc_type(node: classmethod, prev_node: classmethod) -> None:
    global index
    if _is_match(True, "florist", node):
        index += 1
    elif _is_match(True, "tulip", node):
        index += 1
    elif _is_match(True, "dirt", node):
        index += 1
    elif _is_match(True, "stem", node):
        index += 1
    return


# 26-27
def _tint_value(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 26
    if _is_match(True, "=", node):
        index += 1

        if _is_match(False, "<tint>"):
            new_node = add_parse_tree_node(node, "<tint>")
            _tint(new_node, node)
            return

    # 27: EPSILON
    return


# 28-30
def _tint(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 28
    if _is_match(True, "<tint-literals>"):
        new_node = add_parse_tree_node(node, "<tint-literals>")
        _tint_literals(new_node, node)
        return

    # 29
    elif lexemes[index] == "tint" and lexemes[index + 1] == "(":
        # )
        if _is_match(False, "tint", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<all-type-value>"):
            new_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(new_node, node)

        if _is_match(")", node):
            index += 1

    # 30
    elif _is_match(True, "<arithmetic>") and _find_future("<operator>"):
        new_node = add_parse_tree_node(node, "<arithmetic>")
        _arithmetic(new_node, node)
        return

    # error not found
    errors.append((lexemes[index], f"Syntax Error: Expecting {g.FIRST_SET['<tint>']}"))
    return


# 31-34
def _tint_literals(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 31
    if _is_match(True, "Tint Literal", node):
        index += 1
        return

    # 32
    elif _is_match(True, "#", node):
        add_parse_tree_node(node, lexemes[index + 1])
        index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        return

    # 33
    elif _is_match(True, "lent", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        return

    # 34
    elif _is_match(True, "<supply-dirt>"):
        new_node = add_parse_tree_node(node, "<supply-dirt>")
        _supply_dirt(new_node, node)
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        return

    return


# 35-36
def _flora_value(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 35
    if _is_match(True, "=", node):
        index += 1

        if _is_match(False, "<flora>"):
            new_node = add_parse_tree_node(node, "<flora>")
            _flora(new_node, node)
            return

    # 36: EPSILON
    return


# 37-39
def _flora(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 37
    if (
        _is_match(True, "<flora-literals>")
        and not _find_future("<operator>")
    ):
        new_node = add_parse_tree_node(node, "<flora-literals>")
        _flora_literals(new_node, node)
        return

    # 38
    elif lexemes[index] == "flora" and lexemes[index + 1] == "(":
        # )
        if _is_match(False, "flora", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(False, "<all-type-value>"):
            new_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(new_node, node)

        if _is_match(False, ")", node):
            index += 1

    # 39
    elif _is_match(True, "<arithmetic>"):
        new_node = add_parse_tree_node(node, "<arithmetic>")
        _arithmetic(new_node, node)
        return

    errors.append((lexemes[index], f"Syntax Error: Expecting {g.FIRST_SET['<flora>']}"))
    return


# 40-41
def _arithmetic(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 40
    if _is_match(True, "<flora>"):
        new_node = add_parse_tree_node(node, "<flora>")
        _flora(new_node, node)

        if _is_match(True, "<operate-number>"):
            new_node = add_parse_tree_node(node, "<operate-number>")
            _operate_number(new_node, node)

        return

    # 41
    elif _is_match(True, "(", node):
        index += 1

        if _is_match(True, "<flora>"):
            new_node = add_parse_tree_node(node, "<flora>")
            _flora(new_node, node)

        if _is_match(True, "<operator>"):
            new_node = add_parse_tree_node(node, "<operator>")
            _operator(new_node, node)

        if _is_match(True, "<arithmetic>"):
            new_node = add_parse_tree_node(node, "<arithmetic>")
            _arithmetic(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(True, "<operate-number>"):
            new_node = add_parse_tree_node(node, "<operate-number>")
            _operate_number(new_node, node)

        return

    return


# 42-43
def _flora_literals(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 42
    if _is_match(True, "Flora Literal", node):
        index += 1
        return

    # 43
    elif _is_match(True, "<tint-literals>"):
        new_node = add_parse_tree_node(node, "<tint-literals>")
        _tint_literals(new_node, node)

        return

    return


# 44-45
def _operate_number(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 44
    if _is_match(True, "<operator>"):
        new_node = add_parse_tree_node(node, "<operator>")
        _operator(new_node, node)

        if _is_match(True, "<arithmetic>"):
            new_node = add_parse_tree_node(node, "<arithmetic>")
            _arithmetic(new_node, node)

    # 45: EPSILON
    return


# 46-52
def _operator(node: classmethod, prev_node: classmethod) -> None:
    global index
    if _is_match(True, lexemes[index], node):
        index += 1
    return


# 53-54
def _chard_value(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 53
    if _is_match(True, "=", node):
        index += 1

        if _is_match(False, "<chard>"):
            new_node = add_parse_tree_node(node, "<chard>")
            _chard(new_node, node)
            return

    # 54: EPSILON
    return


# 55-56
def _chard(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 55
    if _is_match(True, "<chard-literals>"):
        new_node = add_parse_tree_node(node, "<chard-literals>")
        _chard_literals(new_node, node)

        return

    # 56
    elif _is_match(True, "chard", node):
        index += 1

        if _is_match(False, "(", node):
            index += 2

        if _is_match(True, "<all-type-value>"):
            new_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        return

    errors.append((lexemes[index], f"Syntax Error: Expecting {g.FIRST_SET['<chard>']}"))
    return


# 57-59
def _chard_literals(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 57
    if _is_match(True, "Chard Literal", node):
        index += 1

    # 58
    elif _is_match(True, "#", node):
        index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

    # 59
    elif _is_match(True, "<supply-dirt>"):
        new_node = add_parse_tree_node(node, "<supply-dirt>")
        _supply_dirt(new_node, node)

        if _is_match(False, "(", node):
            index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        if _is_match(False, ")", node):
            index += 1


# 60-61
def _string_value(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 60
    if _is_match(True, "=", node):
        index += 1

        if _is_match(False, "<string>"):
            new_node = add_parse_tree_node(node, "<string>")
            _string(new_node, node)
            return

    # 61: EPSILON
    return


# 62-63
def _string(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 61
    if _is_match(True, "<string-literals>"):
        new_node = add_parse_tree_node(node, "<string-literals>")
        _string_literals(new_node, node)

        if _is_match(True, "<concatenate>"):
            new_node = add_parse_tree_node(node, "<concatenate>")
            _concatenate(new_node, node)

        return

    # 63
    elif _is_match(True, "string", node):
        index += 1

        if _is_match(False, "(", node):
            # )
            index += 1

        if _is_match(True, "<string-literals>"):
            new_node = add_parse_tree_node(node, "<string-literals>")
            _string_literals(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(True, "<concatenate>"):
            new_node = add_parse_tree_node(node, "<concatenate>")
            _concatenate(new_node, node)

        return

    errors.append((lexemes[index], f"Syntax Error: Expecting {g.FIRST_SET['<string>']}"))
    return


# 64-66
def _string_literals(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 64
    if _is_match(True, "String Literal", node):
        index += 1

    # 65
    if _is_match(True, "#", node):
        index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        if _is_match(True, "<start-end-step>"):
            new_node = add_parse_tree_node(node, "<start-end-step>")
            _start_end_step(new_node, node)

    # 66
    if _is_match(True, "<supply-dirt>", node):
        new_node = add_parse_tree_node(node, "<supply-dirt>")
        _supply_dirt(new_node, node)

        if _is_match(False, "(", node):
            # )
            index += 1

        if _is_match(True, "#", node):
            index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        if _is_match(True, ")", node):
            index += 1


# 67-68
def _concatenate(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<indexing>"):
        new_node = add_parse_tree_node(node, "<indexing>")
        _indexing(new_node, node)

        if _is_match(False, "+", node):
            index += 1

        if _is_match(False, "<string>"):
            new_node = add_parse_tree_node(node, "<string>")
            _string(new_node, node)

        if _is_match(True, "<concatenate>"):
            new_node = add_parse_tree_node(node, "<concatenate>")
            _concatenate(new_node, node)

    # 65: EPSILON
    return


# 69-70
def _bloom_value(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "=", node):
        index += 1

        if _is_match(False, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)
            return

    return


# 71-72
def _insert_condition(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<bloom>"):
        new_node = add_parse_tree_node(node, "<bloom>")
        _bloom(new_node, node)

    if _is_match(True, "<sqnc-bloom>"):
        new_node = add_parse_tree_node(node, "<sqnc-bloom>")
        _sqnc_bloom(new_node, node)

    return


# 73-76
def _bloom(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<bloom-literals>"):
        new_node = add_parse_tree_node(node, "<bloom-literals>")
        _bloom_literals(new_node, node)

        if _is_match(True, "<operate-logic>"):
            new_node = add_parse_tree_node(node, "<operate-logic>")
            _operate_logic(new_node, node)

        return

    elif _is_match(True, "(", node):
        # )
        index += 1

        if _is_match(True, "<bloom-literals>"):
            new_node = add_parse_tree_node(node, "<bloom-literals>")
            _bloom_literals(new_node, node)

        if _is_match(True, "<cond-operator>"):
            new_node = add_parse_tree_node(node, "<cond-operator>")
            _cond_operator(new_node, node)

        if _is_match(True, "<bloom>"):
            new_node = add_parse_tree_node(node, "<bloom>")
            _bloom(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(True, "<operate-logic>"):
            new_node = add_parse_tree_node(node, "<operate-logic>")
            _operate_logic(new_node, node)

        return

    errors.append((lexemes[index], f"Syntax Error: Expecting {g.FIRST_SET['<bloom>']}"))
    return


# 77-78
def _sqnc_bloom(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<sqnc>"):
        new_node = add_parse_tree_node(node, "<sqnc>")
        _sqnc(new_node, node)

        if _is_match(True, "<operate-logic>"):
            new_node = add_parse_tree_node(node, "<operate-logic>")
            _operate_logic(new_node, node)

    elif _is_match(True, "(", node):
        # )
        index += 1

        if _is_match(True, "<sqnc>"):
            new_node = add_parse_tree_node(node, "<sqnc>")
            _sqnc(new_node, node)

        if _is_match(True, "<cond-operator>"):
            new_node = add_parse_tree_node(node, "<cond-operator>")
            _cond_operator(new_node, node)

        if _is_match(True, "<sqnc>"):
            new_node = add_parse_tree_node(node, "<sqnc>")
            _sqnc(new_node, node)

        elif _is_match(True, ")", node):
            index += 1

        if _is_match(True, "<operate-logic>"):
            new_node = add_parse_tree_node(node, "<operate-logic>")
            _operate_logic(new_node, node)

    return


# 79-85
def _bloom_literals(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "Bloom Literal", node):
        index += 1
        return

    elif _is_match(True, "<tint>"):
        new_node = add_parse_tree_node(node, "<tint>")
        _tint(new_node, node)
        return

    elif _is_match(True, "<flora>"):
        new_node = add_parse_tree_node(node, "<flora>")
        _flora(new_node, node)
        return

    elif _is_match(True, "<chard>"):
        new_node = add_parse_tree_node(node, "<chard>")
        _chard(new_node, node)
        return

    elif _is_match(True, "<string>"):
        new_node = add_parse_tree_node(node, "<string>")
        _string(new_node, node)
        return

    elif _is_match(True, "<sqnc>"):
        new_node = add_parse_tree_node(node, "<sqnc>")
        _sqnc(new_node, node)
        return

    elif _is_match(True, "bare", node):
        index += 1
        return

    return


# 86-87
def _operate_logic(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<cond-operator>"):
        new_node = add_parse_tree_node(node, "<cond-operator>")
        _cond_operator(new_node, node)

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

    return


# 88-97
def _cond_operator(node: classmethod, prev_node: classmethod) -> None:
    global index
    if _is_match(True, lexemes[index], node):
        index += 1
    return


# 98-99
def _insert_func(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "(", node):
        index += 1

        if _is_match(True, "<argument>"):
            new_node = add_parse_tree_node(node, "<argument>")
            _argument(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(True, "<instance-grab>"):
            new_node = add_parse_tree_node(node, "<instance-grab>")
            _instance_grab(new_node, node)

        return

    return


# 100-101
def _instance_grab(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 92
    if _is_match(True, ".", node):
        index += 1

        if _is_match(False, "#", node):
            index += 2

    return


# 102-103
def _indexing(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 94
    if _is_match(True, "[", node):
        index += 1

        if _is_match(True, "<insert-index>"):
            new_node = add_parse_tree_node(node, "<insert-index>")
            _insert_index(new_node, node)

        if _is_match(False, "]", node):
            index += 1

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        return

    return


# 104-105
def _insert_index(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 96
    if _is_match(True, "Tint Literal", node):
        index += 1
        return

    # 97
    elif _is_match(True, "Flora Literal", node):
        index += 1
        return

    return


# 106-107
def _more_tint(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 98
    if _is_match(True, ",", node):
        index += 1

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        if _is_match(True, "<tint-value>"):
            new_node = add_parse_tree_node(node, "<tint-value>")
            _tint_value(new_node, node)

        if _is_match(True, "<more-tint>"):
            new_node = add_parse_tree_node(prev_node, "<more-tint>")
            _more_tint(new_node, prev_node)

        return

    # 99: EPSILON
    return


# 108-109
def _more_flora(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, ",", node):
        index += 1

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        if _is_match(True, "<flora-value>"):
            new_node = add_parse_tree_node(node, "<flora-value>")
            _flora_value(new_node, node)

        if _is_match(True, "<more-flora>"):
            new_node = add_parse_tree_node(prev_node, "<more-flora>")
            _more_flora(new_node, prev_node)

        return

    return


# 110-111
def _more_chard(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 102
    if _is_match(True, ",", node):
        index += 1

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        if _is_match(True, "<chard-value>"):
            new_node = add_parse_tree_node(node, "<chard-value>")
            _chard_value(new_node, node)

        if _is_match(True, "<more-chard>"):
            new_node = add_parse_tree_node(prev_node, "<more-chard>")
            _more_chard(new_node, prev_node)

        return

    return


# 112-113
def _more_string(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 104
    if _is_match(True, ",", node):
        index += 1

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        if _is_match(True, "<string-value>"):
            new_node = add_parse_tree_node(node, "<string-value>")
            _string_value(new_node, node)

        if _is_match(True, "<more-string>"):
            new_node = add_parse_tree_node(prev_node, "<more-string>")
            _more_string(new_node, prev_node)

        return

    return


# 114-115
def _more_bloom(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 106
    if _is_match(True, ",", node):
        index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<bloom-value>"):
            new_node = add_parse_tree_node(node, "<bloom-value>")
            _bloom_value(new_node, node)

        if _is_match(True, "<more-bloom>"):
            new_node = add_parse_tree_node(node, "<more-bloom>")
            _more_bloom(new_node, node)

        return

    return


# 116-117
def _sqnc_value(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 108
    if _is_match(True, "=", node):
        index += 1

        if _is_match(False, "<sqnc>"):
            new_node = add_parse_tree_node(node, "<sqnc>")
            _sqnc(new_node, node)
            return

        if _is_match(True, "<concatenate>"):
            new_node = add_parse_tree_node(node, "<concatenate>")
            _concatenate(new_node, node)
            return

    return


# 118-119
def _more_sqnc(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 110
    if _is_match(True, ",", node):
        index += 1

        if _is_match(True, "#", node):
            index += 2

        if _is_match(True, "<sqnc-value>"):
            new_node = add_parse_tree_node(node, "<sqnc-value>")
            _sqnc_value(new_node, node)

        if _is_match(True, "<more-sqnc>"):
            new_node = add_parse_tree_node(node, "<more-sqnc>")
            _more_sqnc(new_node, node)

        return

    return

# 120-121
def _more_data(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, ",", node):
        index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        if _is_match(True, "<start-end-step>"):
            new_node = add_parse_tree_node(node, "<start-end-step>")
            _start_end_step(new_node, node)

        if _is_match(True, "<more-data>"):
            new_node = add_parse_tree_node(node, "<more-data>")
            _more_data(new_node, node)

    return


# 122-123
def _more_id(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, ",", node):
        index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        if _is_match(True, "<more-id>"):
            new_node = add_parse_tree_node(node, "<more-id>")
            _more_id(new_node, node)

    return


# 124-125
def _sqnc(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<sqnc-literals>"):
        new_node = add_parse_tree_node(node, "<sqnc-literals>")
        _sqnc_literals(new_node, node)

    elif _is_match(True, "<sqnc-type>"):
        new_node = add_parse_tree_node(node, "<sqnc-type>")
        _sqnc_type(new_node, node)

        if _is_match(False, "(", node):
            # )
            index += 1

        if _is_match(True, "<all-type-value>"):
            new_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        return


# 126-129
def _sqnc_literals(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<open>"):
        new_node = add_parse_tree_node(node, "<open>")
        _open(new_node, node)

        if _is_match(True, "<sequence>"):
            new_node = add_parse_tree_node(node, "<sequence>")
            _sequence(new_node, node)

        if _is_match(True, "<close>"):
            new_node = add_parse_tree_node(node, "<close>")
            _close(new_node, node)

    elif _is_match(True, "<supply-dirt>"):
        new_node = add_parse_tree_node(node, "<supply-dirt>")
        _supply_dirt(new_node, node)

        if _is_match(False, "(", node):
            # )
            index += 1

            if _is_match(True, "#", node):
                add_parse_tree_node(node, lexemes[index + 1])
                index += 2

            if _is_match(True, "<insert-func>"):
                new_node = add_parse_tree_node(node, "<insert-func>")
                _insert_func(new_node, node)

            if _is_match(True, "<indexing>"):
                new_node = add_parse_tree_node(node, "<indexing>")
                _indexing(new_node, node)

            if _is_match(True, ")", node):
                index += 1

    elif _is_match(True, "#"):
        index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        if _is_match(True, "<start-end-step>"):
            new_node = add_parse_tree_node(node, "<start-end-step>")
            _start_end_step(new_node, node)

        return

    return


# 130-132
def _supply_dirt(node: classmethod, prev_node: classmethod) -> None:
    global index
    if _is_match(True, lexemes[index], node):
        index += 1
    return


# 133-134
def _open(node: classmethod, prev_node: classmethod) -> None:
    global index
    if _is_match(True, lexemes[index], node):
        index += 1
    return


# 135-136
def _dirt(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "String Literal", node):
        index += 1

        if _is_match(False, ":", node):
            index += 1
        return

    return


# 137-138
def _close(node: classmethod, prev_node: classmethod) -> None:
    global index
    if _is_match(True, lexemes[index], node):
        index += 1
    return


# 139-140
def _sequence(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<dirt>"):
        new_node = add_parse_tree_node(node, "<dirt>")
        _dirt(new_node, node)

    if _is_match(True, "<common-data>") and lexemes[index + 1] != ":":
        new_node = add_parse_tree_node(node, "<common-data>")
        _common_data(new_node, node)

        if _is_match(True, "<next-sqnc>"):
            new_node = add_parse_tree_node(node, "<next-sqnc>")
            _next_sqnc(new_node, node)

        return

    elif _is_match(True, "<open>"):
        new_node = add_parse_tree_node(node, "<open>")
        _open(new_node, node)

        if _is_match(True, "<2D-sqnc>"):
            new_node = add_parse_tree_node(node, "<2D-sqnc>")
            _2D_sqnc(new_node, node)

        if _is_match(True, "<close>"):
            new_node = add_parse_tree_node(node, "<close>")
            _close(new_node, node)

        if _is_match(True, "<next_sqnc>"):
            new_node = add_parse_tree_node(node, "<next_sqnc>")
            _next_sqnc(new_node, node)

        return

    return


# 141-145
def _common_data(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<tint>"):
        new_node = add_parse_tree_node(node, "<tint>")
        _tint(new_node, node)
        return

    elif _is_match(True, "<flora>"):
        new_node = add_parse_tree_node(node, "<flora>")
        _flora(new_node, node)
        return

    elif _is_match(True, "<chard>"):
        new_node = add_parse_tree_node(node, "<chard>")
        _chard(new_node, node)
        return

    elif _is_match(True, "<string>"):
        new_node = add_parse_tree_node(node, "<string>")
        _string(new_node, node)
        return

    elif _is_match(True, "<bloom>"):
        new_node = add_parse_tree_node(node, "<bloom>")
        _bloom(new_node, node)
        return

    return


# 146-147
def _next_sqnc(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 134
    if _is_match(True, ",", node):
        index += 1

        if _is_match(False, "<sequence>"):
            new_node = add_parse_tree_node(node, "<sequence>")
            _sequence(new_node, node)

        return

    return


# 148-149
def _2D_sqnc(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<dirt>"):
        new_node = add_parse_tree_node(node, "<dirt>")
        _dirt(new_node, node)

        if _is_match(True, "<common-data>"):
            new_node = add_parse_tree_node(node, "<common-data>")
            _common_data(new_node, node)

            if _is_match(True, "<next-2D-sqnc>"):
                new_node = add_parse_tree_node(node, "<next-2D-sqnc>")
                _next_2D_sqnc(new_node, node)

            return

        # 137
        elif _is_match(True, "<open>"):
            new_node = add_parse_tree_node(node, "<open>")
            _open(new_node, node)

            if _is_match(True, "<dirt>"):
                new_node = add_parse_tree_node(node, "<dirt>")
                _dirt(new_node, node)

            if _is_match(True, "<common-data>"):
                new_node = add_parse_tree_node(node, "<common-data>")
                _common_data(new_node, node)

            if _is_match(True, "<next-3D-sqnc>"):
                new_node = add_parse_tree_node(node, "<next-3D-sqnc>")
                _next_3D_sqnc(new_node, node)

            if _is_match(True, "<close>"):
                new_node = add_parse_tree_node(node, "<close>")
                _close(new_node, node)

            if _is_match(True, "<next-2D-sqnc>"):
                new_node = add_parse_tree_node(node, "<next-2D-sqnc>")
                _next_2D_sqnc(new_node, node)

            return

    return


# 150-151
def _next_2D_sqnc(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 138
    if _is_match(True, ",", node):
        index += 1

        if _is_match(True, "<2D-sqnc>"):
            new_node = add_parse_tree_node(node, "<2D-sqnc>")
            _2D_sqnc(new_node, node)

        return

    return


# 152-153
def _next_3D_sqnc(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 140
    if _is_match(True, ",", node):
        index += 1

        # dirt
        if _is_match(True, "<dirt>"):
            new_node = add_parse_tree_node(node, "<dirt>")
            _dirt(new_node, node)

        if _is_match(True, "<common-data>"):
            new_node = add_parse_tree_node(node, "<common-data>")
            _common_data(new_node, node)

        if _is_match(True, "<next-3D-sqnc>"):
            new_node = add_parse_tree_node(node, "<next-3D-sqnc>")
            _next_3D_sqnc(new_node, node)

        return

    return


# 154-155
def _start_end_step(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 142
    if _is_match(True, "[", node):
        # ]
        index += 1

        if _is_match(True, "<insert_start>"):
            new_node = add_parse_tree_node(node, "<insert_start>")
            _insert_start(new_node, node)

        return

    return


# ]] 156-157
def _insert_start(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "Tint Literal", node):
        index += 1

        if _is_match(False, ":", node):
            index += 1

        if _is_match(True, "<close-start>"):
            new_node = add_parse_tree_node(node, "<close-start>")
            _close_start(new_node, node)

        return

    elif _is_match(True, ":", node):
        index += 1

        if _is_match(True, "<skip-start>"):
            new_node = add_parse_tree_node(node, "<skip-start>")
            _skip_start(new_node, node)

        return

    return


# 158-159
def _close_start(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<close-end>"):
        new_node = add_parse_tree_node(node, "<close-end>")
        _close_end(new_node, node)
        return

    elif _is_match(True, "Tint Literal", node):
        index += 1

        if _is_match(True, "<close-end>"):
            new_node = add_parse_tree_node(node, "<close-end>")
            _close_end(new_node, node)

        return

    return


# 160-161
def _close_end(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "]", node):
        index += 1

        if _is_match(True, "<2D-start-end-step>"):
            new_node = add_parse_tree_node(node, "<2D-start-end-step>")
            _2D_start_end_step(new_node, node)

        return

    elif _is_match(True, ":", node):
        index += 1

        if _is_match(True, "Tint Literal", node):
            index += 1

        if _is_match(False, "]", node):
            index += 1

        if _is_match(True, "<2D-start-end-step>"):
            new_node = add_parse_tree_node(node, "<2D-start-end-step>")
            _2D_start_end_step(new_node, node)

        return

    return


# 162-163
def _skip_start(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "Tint Literal", node):
        index += 1

        if _is_match(True, "<close-end>"):
            new_node = add_parse_tree_node(node, "<close-end>")
            _close_end(new_node, node)

        if _is_match(True, "<2D-start-end-step>"):
            new_node = add_parse_tree_node(node, "<2D-start-end-step>")
            _2D_start_end_step(new_node, node)

        return

    elif _is_match(True, ":", node):
        index += 1

        if _is_match(True, "Tint Literal", node):
            index += 1

        if _is_match(False, "]", node):
            index += 1

        if _is_match(True, "<2D-start-end-step>"):
            new_node = add_parse_tree_node(node, "<2D-start-end-step>")
            _2D_start_end_step(new_node, node)

        return

    return


# 164-165
def _2D_start_end_step(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 152
    if _is_match(True, "[", node):
        index += 1

        if _is_match(True, "<2D-insert-start>"):
            new_node = add_parse_tree_node(node, "<2D-insert-start>")
            _2D_insert_start(new_node, node)

        return

    # ]] 153: EPSILON
    return


# 166-167
def _2D_insert_start(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "Tint Literal", node):
        index += 1

        if _is_match(False, ":", node):
            index += 1

        if _is_match(True, "<2D-close-start>"):
            new_node = add_parse_tree_node(node, "<2D-close-start>")
            _2D_close_start(new_node, node)

        return

    elif _is_match(True, ":", node):

        if _is_match(True, "<2D-skip-start>"):
            new_node = add_parse_tree_node(node, "<2D-skip-start>")
            _2D_skip_start(new_node, node)

        return

    return


# 168-169
def _2D_close_start(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<2D-close-end>"):
        new_node = add_parse_tree_node(node, "<2D-close-end>")
        _2D_close_end(new_node, node)
        return

    elif _is_match(True, "Tint Literal", node):
        index += 1

        if _is_match(True, "<2D-close-end>"):
            new_node = add_parse_tree_node(node, "<2D-close-end>")
            _2D_close_end(new_node, node)

        return

    return


# 170-171
def _2D_close_end(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "]", node):
        index += 1

        if _is_match(True, "<3D-start-end-step>"):
            new_node = add_parse_tree_node(node, "<3D-start-end-step>")
            _3D_start_end_step(new_node, node)

        return

    elif _is_match(True, ":", node):
        index += 1

        if _is_match(True, "Tint Literal", node):
            index += 1

        if _is_match(False, "]", node):
            index += 1

        if _is_match(True, "<3D-start-end-step>"):
            new_node = add_parse_tree_node(node, "<3D-start-end-step>")
            _3D_start_end_step(new_node, node)

        return

    return


# 172-173
def _2D_skip_start(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "Tint Literal", node):
        index += 1

        if _is_match(True, "<2D-close-end>"):
            new_node = add_parse_tree_node(node, "<2D-close-end>")
            _2D_close_end(new_node, node)

        if _is_match(True, "<3D-start-end-step>"):
            new_node = add_parse_tree_node(node, "<3D-start-end-step>")
            _3D_start_end_step(new_node, node)

        return

    elif _is_match(True, ":", node):
        index += 1

        if _is_match(True, "Tint Literal", node):
            index += 1

        if _is_match(False, "]", node):
            index += 1

        if _is_match(True, "<3D-start-end-step>"):
            new_node = add_parse_tree_node(node, "<3D-start-end-step>")
            _3D_start_end_step(new_node, node)

        return

    return


# 174-175
def _3D_start_end_step(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "[", node):
        # ]
        index += 1

        if _is_match(True, "<3D-insert-start>"):
            new_node = add_parse_tree_node(node, "<3D-insert-start>")
            _3D_insert_start(new_node, node)

        return

    return


# 176-177
def _3D_insert_start(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "Tint Literal", node):
        index += 1

        if _is_match(False, ":", node):
            index += 1

        if _is_match(True, "<3D-close-start>"):
            new_node = add_parse_tree_node(node, "<3D-close-start>")
            _3D_close_start(new_node, node)

        return

    elif _is_match(True, ":", node):
        index += 1

        if _is_match(True, "<3D-skip-start>"):
            new_node = add_parse_tree_node(node, "<3D-skip-start>")
            _3D_skip_start(new_node, node)

        return

    return


# 178-179
def _3D_close_start(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<3D-close-end>"):
        new_node = add_parse_tree_node(node, "<3D-close-end>")
        _3D_close_end(new_node, node)
        return

    elif _is_match(True, "Tint Literal", node):
        index += 1

        if _is_match(True, "<3D-close-end>"):
            new_node = add_parse_tree_node(node, "<3D-close-end>")
            _3D_close_end(new_node, node)

        return

    return


# 180-181
def _3D_close_end(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "]", node):
        index += 1
        return

    elif _is_match(True, ":", node):
        index += 1

        if _is_match(True, "Tint Literal", node):
            index += 1

        if _is_match(False, "]", node):
            index += 1

        return

    return


# 182-183
def _3D_skip_start(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "Tint Literal", node):
        index += 1

        if _is_match(True, "<3D-close-end>"):
            new_node = add_parse_tree_node(node, "<3D-close-end>")
            _3D_close_end(new_node, node)

        return

    elif _is_match(True, ":", node):
        index += 1

        if _is_match(True, "Tint Literal", node):
            index += 1

        if _is_match(False, "]", node):
            index += 1

        return

    return


# 184-188
def _all_type_value(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<common-data>"):
        new_node = add_parse_tree_node(node, "<common-data>")
        _common_data(new_node, node)
        return

    elif _is_match(True, "<insert-condition>"):
        _insert_condition()
        return

    elif _is_match(True, "<sqnc>"):
        _sqnc()
        return

    elif _is_match(True, "#"):
        add_parse_tree_node(node, lexemes[index + 1])
        index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        if _is_match(True, "<start-end-step>"):
            new_node = add_parse_tree_node(node, "<start-end-step>")
            _start_end_step(new_node, node)

        return

    elif _is_match(True, "inpetal", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "String Literal", node):
            index += 1

        if _is_match(False, ")", node):
            index += 1

        return

    return


# 189-190
def _i_o_statement(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<insert-inpetal>") and _find_future("inpetal"):
        new_node = add_parse_tree_node(node, "<insert-inpetal>")
        _insert_inpetal(new_node, node)

        if _is_match(False, "inpetal", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "String Literal", node):
            index += 1

        if _is_match(False, ")", node):
            index += 1

        return

    elif _is_match(True, "mint", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<all-type-value>"):
            new_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        return


# 191-193
def _insert_inpetal(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<common-type>"):
        new_node = add_parse_tree_node(node, "<common-type>")
        _common_type(new_node, node)

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        if _is_match(False, "=", node):
            index += 1

        return

    elif _is_match(True, "<sqnc-type>"):
        new_node = add_parse_tree_node(node, "<sqnc-type>")
        _sqnc_type(new_node, node)

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        if _is_match(False, "=", node):
            index += 1

        return

    elif _is_match(True, "#", node):
        index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        if _is_match(False, "=", node):
            index += 1

        return

    return


# 194-198
def _common_type(node: classmethod, prev_node: classmethod) -> None:
    global index
    if _is_match(True, lexemes[index], node):
        index += 1
    return


# 199-200
def _eleaf(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "eleaf", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-statement>"):
            new_node = add_parse_tree_node(node, "<filter-statement>")
            _filter_statement(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<eleaf>"):
            new_node = add_parse_tree_node(node, "<eleaf>")
            _eleaf(new_node, node)

        return

    return


# 201-202
def _2D_eleaf(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 185
    if _is_match(True, "eleaf", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            new_node = add_parse_tree_node(node, "<filter-2D-state>")
            _filter_2D_state(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 203-204
def _3D_eleaf(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "eleaf", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            new_node = add_parse_tree_node(node, "<filter-3D-state>")
            _filter_3D_state(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 205-206
def _final_eleaf(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "eleaf", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            new_node = add_parse_tree_node(node, "<filter-final-state>")
            _filter_final_state(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 207-208
def _else(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "moss", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-statement>"):
            new_node = add_parse_tree_node(node, "<filter-statement>")
            _filter_statement(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 209-210
def _2D_else(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 195
    if _is_match(True, "moss", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            new_node = add_parse_tree_node(node, "<filter-2D-state>")
            _filter_2D_state(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 211-212
def _3D_else(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 197
    if _is_match(True, "moss", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            new_node = add_parse_tree_node(node, "<filter-3D-state>")
            _filter_3D_state(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 213-214
def _final_else(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 199
    if _is_match(True, "moss", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            new_node = add_parse_tree_node(node, "<filter-final-state>")
            _filter_final_state(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 215-216
def _iterative(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "fern", node):
        index += 1

        if _is_match(False, "(", node):
            print("here")
            index += 1

        if _is_match(True, "<insert-fern>"):
            new_node = add_parse_tree_node(node, "<insert-fern>")
            _insert_fern(new_node, node)

        return

    elif _is_match(True, "willow", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<2D-statement>"):
            new_node = add_parse_tree_node(node, "<2D-statement>")
            _2D_statement(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        return
    return


# 217-218
def _insert_fern(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "tint", node):
        index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(False, "=", node):
            index += 1

        if _is_match(False, "Tint Literal", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        if _is_match(False, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        if _is_match(False, "<assignment-op>"):
            new_node = add_parse_tree_node(node, "<assignment-op>")
            _assignment_op(new_node, node)

        if _is_match(False, "<tint>"):
            new_node = add_parse_tree_node(node, "<tint>")
            _tint(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<2D-statement>"):
            new_node = add_parse_tree_node(node, "<2D-statement>")
            _2D_statement(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        return

    elif _is_match(True, "<all-type-value>"):
        new_node = add_parse_tree_node(node, "<all-type-value>")
        _all_type_value(new_node, node)

        if _is_match(True, "<more-value>"):
            new_node = add_parse_tree_node(node, "<more-value>")
            _more_value(new_node, node)

        if _is_match(False, "at", node):
            index += 1

        if _is_match(True, "<sqnc>"):
            new_node = add_parse_tree_node(node, "<sqnc>")
            _sqnc(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<2D-statement>"):
            new_node = add_parse_tree_node(node, "<2D-statement>")
            _2D_statement(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        return

    return


# 219-220
def _assignment(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "#", node):
        index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        if _is_match(True, "<start-end-step>"):
            new_node = add_parse_tree_node(node, "<start-end-step>")
            _start_end_step(new_node, node)

        if _is_match(True, "<more-id>"):
            new_node = add_parse_tree_node(node, "<more-id>")
            _more_id(new_node, node)

        if _is_match(True, "<assign>"):
            new_node = add_parse_tree_node(node, "<assign>")
            _assign(new_node, node)

    elif _is_match(True, "<common-type>"):
        new_node = add_parse_tree_node(node, "<common-type>")
        _common_type(new_node, node)

        if _is_match(False, "(", node):
            # )
            index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<insert-func>"):
            new_node = add_parse_tree_node(node, "<insert-func>")
            _insert_func(new_node, node)

        if _is_match(True, "<indexing>"):
            new_node = add_parse_tree_node(node, "<indexing>")
            _indexing(new_node, node)

        if _is_match(True, "<start-end-step>"):
            new_node = add_parse_tree_node(node, "<start-end-step>")
            _start_end_step(new_node, node)

        if _is_match(False, ")", node):
            index += 1
    return


# 221-222
def _assign(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<assignment-op>"):
        new_node = add_parse_tree_node(node, "<assignment-op>")
        _assignment_op(new_node, node)

        if _is_match(False, "<all-type-value>"):
            new_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(new_node, node)
    return


# 223-230
def _assignment_op(node: classmethod, prev_node: classmethod) -> None:
    global index
    if _is_match(True, lexemes[index], node):
        index += 1
    return


# 231-232
def _more_value(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, ",", node):
        index += 1

        if _is_match(True, "<all-type-value>"):
            new_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(new_node, node)

        if _is_match(True, "<final-value>"):
            new_node = add_parse_tree_node(node, "<final-value>")
            _final_value(new_node, node)

        return

    return


# 233-234
def _final_value(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, ",", node):
        index += 1

        if _is_match(True, "<all-type-value>"):
            new_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(new_node, node)
        return

    return


# 235-236
def _use_tree(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "tree", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(False, "branch", node):
            index += 1

        if _is_match(True, "<check-branch>"):
            new_node = add_parse_tree_node(node, "<check-branch>")
            _check_branch(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 237-238
def _check_branch(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<all-type-value>"):
        new_node = add_parse_tree_node(node, "<all-type-value>")
        _all_type_value(new_node, node)

        if _is_match(True, "<insert-branch>"):
            new_node = add_parse_tree_node(node, "<insert-branch>")
            _insert_branch(new_node, node)

        if _is_match(True, "<more-branch>"):
            new_node = add_parse_tree_node(node, "<more-branch>")
            _more_branch(new_node, node)

        return

    elif _is_match(True, "_", node):
        index += 1

        if _is_match(False, ":"):
            index += 1

        if _is_match(True, "<filter-statement>"):
            new_node = add_parse_tree_node(node, "<filter-statement>")
            _filter_statement(new_node, node)

        return

    return


# 239-240
def _insert_branch(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, ":", node):
        index += 1

        if _is_match(True, "<filter-statement>"):
            new_node = add_parse_tree_node(node, "<filter-statement>")
            _filter_statement(new_node, node)

        return

    elif _is_match(True, "leaf", node):
        index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-statement>"):
            new_node = add_parse_tree_node(node, "<filter-statement>")
            _filter_statement(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 241-242
def _more_branch(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 223
    if _is_match(True, "branch", node):
        index += 1

        if _is_match(True, "<check-branch>"):
            new_node = add_parse_tree_node(node, "<check-branch>")
            _check_branch(new_node, node)

        return

    return


# 243-244
def _2D_statement(node: classmethod, prev_node: classmethod) -> None:
    global index
    # Note: Have _statement() & _3D_statement(), modifying this method need to
    # be done to both _statement() and _3D_statement() methods

    avoid = [")", ";"]

    if _is_match(True, "<use-2D-tree>") and lexemes[index] == "tree":
        new_node = add_parse_tree_node(node, "<use-2D-tree>")
        _use_2D_tree(new_node, node)

    elif _is_match(True, "<filter-2D-state>"):
        new_node = add_parse_tree_node(node, "<filter-2D-state>")
        _filter_2D_state(new_node, node)

    return


# 245-246
def _use_2D_tree(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "tree", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(False, "branch", node):
            index += 1

        if _is_match(True, "<check-2D-branch>"):
            new_node = add_parse_tree_node(node, "<check-2D-branch>")
            _check_2D_branch(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 247-248
def _check_2D_branch(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<all-type-value>"):
        new_node = add_parse_tree_node(node, "<all-type-value>")
        _all_type_value(new_node, node)

        if _is_match(True, "<insert-2D-branch>"):
            new_node = add_parse_tree_node(node, "<insert-2D-branch>")
            _insert_2D_branch(new_node, node)

        if _is_match(True, "<more-2D-branch>"):
            new_node = add_parse_tree_node(node, "<more-2D-branch>")
            _more_2D_branch(new_node, node)

        return

    elif _is_match(True, "_", node):
        index += 1

        if _is_match(False, ":", node):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            new_node = add_parse_tree_node(node, "<filter-2D-state>")
            _filter_2D_state(new_node, node)

        return

    return


# 249-250
def _insert_2D_branch(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, ":", node):
        index += 1

        if _is_match(True, "<filter-2D-state>"):
            new_node = add_parse_tree_node(node, "<filter-2D-state>")
            _filter_2D_state(new_node, node)

        return

    elif _is_match(True, "leaf", node):
        index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            new_node = add_parse_tree_node(node, "<filter-2D-state>")
            _filter_2D_state(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 251-252
def _more_2D_branch(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 233
    if _is_match(True, "branch", node):
        index += 1

        if _is_match(True, "<check-2D-branch>"):
            new_node = add_parse_tree_node(node, "<check-2D-branch>")
            _check_2D_branch(new_node, node)

        return

    return


# 253-260
def _filter_2D_state(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<constant>") or _is_match(True, "<insert-variable>"):
        if _is_match(True, "<constant>"):
            new_node = add_parse_tree_node(node, "<constant>")
            _constant(new_node, node)

        if _is_match(True, "<insert-variable>"):
            new_node = add_parse_tree_node(node, "<insert-variable>")
            _insert_variable(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            new_node = add_parse_tree_node(prev_node, "<filter-2D-state>")
            _filter_2D_state(new_node, node)

        return

    elif _is_match(True, "<i/o-statement>"):
        new_node = add_parse_tree_node(node, "<i/o-statement>")
        _i_o_statement(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-2D-state"):
            new_node = add_parse_tree_node(prev_node, "<filter-2D-state")
            _filter_2D_state(new_node, node)

    elif _is_match(True, "leaf", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            # )
            index += 1

        if _is_match(True, "<filter-2D-state"):
            new_node = add_parse_tree_node(node, "<filter-2D-state")
            _filter_2D_state(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<2D-eleaf>"):
            new_node = add_parse_tree_node(node, "<2D-eleaf>")
            _2D_eleaf(new_node, node)

        if _is_match(True, "<2D-else>"):
            new_node = add_parse_tree_node(node, "<2D-else>")
            _2D_else(new_node, node)

        if _is_match(True, "<filter-2D-state"):
            new_node = add_parse_tree_node(prev_node, "<filter-2D-state")
            _filter_2D_state(new_node, node)

        return

    elif _is_match(True, "<assignment>"):
        new_node = add_parse_tree_node(node, "<assignment>")
        _assignment(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-2D-state"):
            new_node = add_parse_tree_node(prev_node, "<filter-2D-state")
            _filter_2D_state(new_node, node)

        return

    elif _is_match(True, "<2D-iterative>"):
        new_node = add_parse_tree_node(node, "<2D-iterative>")
        _2D_iterative(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            new_node = add_parse_tree_node(prev_node, "<filter-2D-state>")
            _filter_2D_state(new_node, node)

        return

    elif _is_match(True, "clear", node):
        index += 1

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            new_node = add_parse_tree_node(prev_node, "<filter-2D-state>")
            _filter_2D_state(new_node, node)

        return

    elif _is_match(True, "break", node):
        index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 261-262
def _2D_iterative(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(False, "fern", node):
        index += 1

        if _is_match(False, "(", node):
            # )
            index += 1

        if _is_match(True, "<insert-2D-fern>"):
            new_node = add_parse_tree_node(node, "<insert-2D-fern>")
            _insert_2D_fern(new_node, node)

        return

    elif _is_match(True, "willow", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<3D-statement>"):
            new_node = add_parse_tree_node(node, "<3D-statement>")
            _3D_statement(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        return
    return


# 263-264
def _insert_2D_fern(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "tint", node):
        index += 1

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        if _is_match(False, "=", node):
            index += 1

        if _is_match(False, "Tint Literal", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        if _is_match(False, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(False, "<assignment-op>"):
            new_node = add_parse_tree_node(node, "<assignment-op>")
            _assignment_op(new_node, node)

        if _is_match(False, "<tint>"):
            new_node = add_parse_tree_node(node, "<tint>")
            _tint(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<3D-statement>"):
            new_node = add_parse_tree_node(node, "<3D-statement>")
            _3D_statement(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        return

    elif _is_match(True, "<all-type-value>"):
        new_node = add_parse_tree_node(node, "<all-type-value>")
        _all_type_value(new_node, node)

        if _is_match(True, "<more-value>"):
            new_node = add_parse_tree_node(node, "<more-value>")
            _more_value(new_node, node)

        if _is_match(False, "at", node):
            index += 1

        if _is_match(True, "<sqnc-value>"):
            new_node = add_parse_tree_node(node, "<sqnc-value>")
            _sqnc_value(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<3D-statement>"):
            new_node = add_parse_tree_node(node, "<3D-statement>")
            _2D_statement(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        return

    return


# 265-266
def _3D_statement(node: classmethod, prev_node: classmethod) -> None:
    global index
    # Note: Have _statement() & _2D_statement(), modifying this method need to
    # be done to both _statement() and 2D_statement() methods

    avoid = [")", ";"]

    if _is_match(True, "<use-3D-tree>") and lexemes[index] == "tree":
        new_node = add_parse_tree_node(node, "<use-3D-tree>")
        _use_3D_tree(new_node, node)

    if _is_match(True, "<filter-3D-state>"):
        new_node = add_parse_tree_node(node, "<filter-3D-state>")
        _filter_3D_state(new_node, node)

    return


# 267-268
def _use_3D_tree(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "tree", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(False, "branch", node):
            index += 1

        if _is_match(True, "<check-3D-branch>"):
            new_node = add_parse_tree_node(node, "<check-3D-branch>")
            _check_3D_branch(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 269-270
def _check_3D_branch(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<all-type-value>"):
        new_node = add_parse_tree_node(node, "<all-type-value>")
        _all_type_value(new_node, node)

        if _is_match(True, "<insert-3D-branch>"):
            new_node = add_parse_tree_node(node, "<insert-3D-branch>")
            _insert_3D_branch(new_node, node)

        if _is_match(True, "<more-3D-branch>"):
            new_node = add_parse_tree_node(node, "<more-3D-branch>")
            _more_3D_branch(new_node, node)

        return

    elif _is_match(True, "_", node):
        index += 1

        if _is_match(False, ":", node):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            new_node = add_parse_tree_node(node, "<filter-3D-state>")
            _filter_3D_state(new_node, node)

        return

    return


# 271-272
def _insert_3D_branch(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, ":", node):
        index += 1

        if _is_match(True, "<filter-3D-state>"):
            new_node = add_parse_tree_node(node, "<filter-3D-state>")
            _filter_3D_state(new_node, node)

        return

    elif _is_match(True, "leaf", node):
        index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            new_node = add_parse_tree_node(node, "<filter-3D-state>")
            _filter_3D_state(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 273-274
def _more_3D_branch(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 255
    if _is_match(True, "branch", node):
        index += 1

        if _is_match(True, "<check-3D-branch>"):
            new_node = add_parse_tree_node(node, "<check-3D-branch>")
            _check_3D_branch(new_node, node)

        return

    return


# 275-282
def _filter_3D_state(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<constant>") or _is_match(True, "<insert-variable>"):

        if _is_match(True, "<constant>"):
            new_node = add_parse_tree_node(node, "<constant>")
            _constant(new_node, node)

        if _is_match(True, "<insert-variable>"):
            new_node = add_parse_tree_node(node, "<insert-variable>")
            _insert_variable(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            new_node = add_parse_tree_node(prev_node, "<filter-3D-state>")
            _filter_3D_state(new_node, node)

        return

    elif _is_match(True, "<i/o-statement>"):
        new_node = add_parse_tree_node(node, "<i/o-statement>")
        _i_o_statement(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            new_node = add_parse_tree_node(prev_node, "<filter-3D-state>")
            _filter_3D_state(new_node, node)

    elif _is_match(True, "leaf", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            new_node = add_parse_tree_node(node, "<filter-3D-state>")
            _filter_3D_state(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<3D-eleaf>"):
            new_node = add_parse_tree_node(node, "<3D-eleaf>")
            _3D_eleaf(new_node, node)

        if _is_match(True, "<3D-else>"):
            new_node = add_parse_tree_node(node, "<3D-else>")
            _3D_else(new_node, node)

        if _is_match(True, "<filter-3D-state"):
            new_node = add_parse_tree_node(prev_node, "<filter-3D-state")
            _filter_3D_state(new_node, node)

        return

    elif _is_match(True, "<assignment>", node):
        new_node = add_parse_tree_node(node, "<assignment>")
        _assignment(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            new_node = add_parse_tree_node(node, "<filter-3D-state>")
            _filter_3D_state(new_node, node)

        return

    elif _is_match(True, "<3D-itertive>"):
        new_node = add_parse_tree_node(node, "<3D-itertive>")
        _3D_iterative(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            new_node = add_parse_tree_node(prev_node, "<filter-3D-state>")
            _filter_3D_state(new_node, node)

        return

    elif _is_match(True, "clear", node):
        index += 1

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            new_node = add_parse_tree_node(prev_node, "<filter-3D-state>")
            _filter_3D_state(new_node, node)

        return

    elif _is_match(True, "break", node):
        index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 283-284
def _3D_iterative(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "fern", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<insert-3D-fern>"):
            new_node = add_parse_tree_node(node, "<insert-3D-fern>")
            _insert_3D_fern(new_node, node)

        return

    elif _is_match(True, "willow", node):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<final-statement>"):
            new_node = add_parse_tree_node(node, "<final-statement>")
            _final_statement(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        return

    return


# 285-286
def _insert_3D_fern(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "tint", node):
        index += 1

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        if _is_match(False, "=", node):
            index += 1

        if _is_match(False, "Tint Literal", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<assignment-op>"):
            new_node = add_parse_tree_node(node, "<assignment-op>")
            _assignment_op(new_node, node)

        if _is_match(True, "<tint>"):
            new_node = add_parse_tree_node(node, "<tint>")
            _tint(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<final-statement>"):
            new_node = add_parse_tree_node(node, "<final-statement>")
            _final_statement(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        return

    elif _is_match(True, "<all-type-value>"):
        new_node = add_parse_tree_node(node, "<all-type-value>")
        _all_type_value(new_node, node)

        if _is_match(True, "<more-value>"):
            new_node = add_parse_tree_node(node, "<more-value>")
            _more_value(new_node, node)

        if _is_match(False, "at", node):
            index += 1

        if _is_match(True, "<sqnc-value>"):
            new_node = add_parse_tree_node(node, "<sqnc-value>")
            _sqnc_value(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<final-statement>"):
            new_node = add_parse_tree_node(node, "<final-statement>")
            _final_statement(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        return

    return


# 287-288
def _final_statement(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<use-final-tree>"):
        new_node = add_parse_tree_node(node, "<use-final-tree>")
        _use_final_tree(new_node, node)

        if _is_match(True, "<filter-final-state>"):
            new_node = add_parse_tree_node(node, "<filter-final-state>")
            _filter_final_state(new_node, node)

        if _is_match(True, "<final-statement>"):
            new_node = add_parse_tree_node(node, "<final-statement>")
            _final_statement(new_node, node)

        return
    return


# 289-290
def _use_final_tree(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "tree", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(False, "branch", node):
            index += 1

        if _is_match(True, "<check-final-branch>"):
            new_node = add_parse_tree_node(node, "<check-final-branch>")
            _check_final_branch(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 291-292
def _check_final_branch(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<all-type-value>"):
        new_node = add_parse_tree_node(node, "<all-type-value>")
        _all_type_value(new_node, node)

        if _is_match(True, "<insert-final-branch>"):
            new_node = add_parse_tree_node(node, "<insert-final-branch>")
            _insert_final_branch(new_node, node)

        if _is_match(True, "<more-final-branch>"):
            new_node = add_parse_tree_node(node, "<more-final-branch>")
            _more_final_branch(new_node, node)

        return

    elif _is_match(True, "_", node):
        index += 1

        if _is_match(False, ":", node):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            new_node = add_parse_tree_node(node, "<filter-final-state>")
            _filter_final_state(new_node, node)

        return

    return


# 293-294
def _insert_final_branch(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, ":", node):
        index += 1

        if _is_match(True, "<filter-final-state>"):
            new_node = add_parse_tree_node(node, "<filter-final-state>")
            _filter_final_state(new_node, node)

        return

    elif _is_match(True, "leaf", node):
        index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(node, "<insert-condition>")
            _insert_condition(new_node, node)

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            _filter_final_state()

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 295-296
def _more_final_branch(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "branch", node):
        index += 1

        if _is_match(True, "<check-final-branch>"):
            new_node = add_parse_tree_node(node, "<check-final-branch>")
            _check_final_branch(new_node, node)

        return
    return


# 297-303
def _filter_final_state(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<constant>") or _is_match(True, "<insert-variable>"):

        if _is_match(True, "<constant>"):
            new_node = add_parse_tree_node(node, "<constant>")
            _constant(new_node, node)

        if _is_match(True, "<insert-variable>"):
            new_node = add_parse_tree_node(node, "<insert-variable>")
            _insert_variable(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            new_node = add_parse_tree_node(prev_node, "<filter-final-state>")
            _filter_final_state(new_node, prev_node)

        return

    elif _is_match(True, "<i/o-statement>"):
        new_node = add_parse_tree_node(node, "<i/o-statement>")
        _i_o_statement(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            new_node = add_parse_tree_node(prev_node, "<filter-final-state>")
            _filter_final_state(new_node, prev_node)

    elif _is_match(True, "leaf", node):
        index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<insert-condition>"):
            new_node = add_parse_tree_node(prev_node, "<insert-condition>")
            _insert_condition(new_node, prev_node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            new_node = add_parse_tree_node(node, "<filter-final-state>")
            _filter_final_state(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<final-eleaf>"):
            new_node = add_parse_tree_node(node, "<final-eleaf>")
            _final_eleaf(new_node, node)

        if _is_match(True, "<final-else>"):
            new_node = add_parse_tree_node(node, "<final-else>")
            _final_else(new_node, node)

        if _is_match(True, "<filter-final-state>"):
            new_node = add_parse_tree_node(prev_node, "<filter-final-state>")
            _filter_final_state(new_node, prev_node)

        return

    elif _is_match(True, "<assignment>", node):
        new_node = add_parse_tree_node(node, "<assignment>")
        _assignment(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            new_node = add_parse_tree_node(prev_node, "<filter-final-state>")
            _filter_final_state(new_node, prev_node)

        return

    elif _is_match(True, "clear", node):
        if _is_match(True, ";", node):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            new_node = add_parse_tree_node(prev_node, "<filter-final-state>")
            _filter_final_state(new_node, prev_node)

        return

    elif _is_match(True, "break", node):
        index += 1

        if _is_match(False, ";", node):
            index += 1

        return

    return


# 304-306
def _argument(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<insert-argument>"):
        new_node = add_parse_tree_node(node, "<insert-argument>")
        _insert_argument(new_node, node)
        return

    elif _is_match(True, "<insert**kwargs>", node):
        new_node = add_parse_tree_node(node, "<insert**kwargs>")
        _insert_kwargs(new_node, node)

        return

    return


# 307-309
def _insert_argument(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<all-type-value>"):
        new_node = add_parse_tree_node(node, "<all-type-value>")
        _all_type_value(new_node, node)

        if _is_match(True, "<add-argument>"):
            new_node = add_parse_tree_node(node, "<add-argument>")
            _add_argument(new_node, node)

        return

    elif _is_match(True, "#", node):
        index += 2

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<2D-argument>"):
            new_node = add_parse_tree_node(node, "<2D-argument>")
            _2D_argument(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(True, "<add-argument>"):
            new_node = add_parse_tree_node(node, "<add-argument>")
            _add_argument(new_node, node)

        return

    return


# 310-314
def _insert_kwargs(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "tint", node):
        index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<tint-value"):
            new_node = add_parse_tree_node(node, "<tint-value")
            _tint_value(new_node, node)

        if _is_match(True, "<more**kwargs>"):
            new_node = add_parse_tree_node(node, "<more**kwargs>")
            _more_kwargs(new_node, node)

        return

    elif _is_match(True, "flora", node):
        index += 1

        if _is_match(True, "<flora-value>"):
            new_node = add_parse_tree_node(node, "<flora-value>")
            _flora_value(new_node, node)

        if _is_match(True, "<more**kwargs>"):
            new_node = add_parse_tree_node(node, "<more**kwargs>")
            _more_kwargs(new_node, node)

        return

    elif _is_match(True, "chard", node):
        index += 1

        if _is_match(True, "<chard-value>"):
            new_node = add_parse_tree_node(node, "<chard-value>")
            _chard_value(new_node, node)

        if _is_match(True, "<more**kwargs>"):
            new_node = add_parse_tree_node(node, "<more**kwargs>")
            _more_kwargs(new_node, node)

        return

    elif _is_match(True, "string", node):
        index += 1

        if _is_match(True, "<string-value>"):
            new_node = add_parse_tree_node(node, "<string-value>")
            _string_value(new_node, node)

        if _is_match(True, "<more**kwargs>"):
            new_node = add_parse_tree_node(node, "<more**kwargs>")
            _more_kwargs(new_node, node)

        return

    elif _is_match(True, "bloom", node):
        index += 1

        if _is_match(True, "<bloom-value>"):
            new_node = add_parse_tree_node(node, "<bloom-value>")
            _bloom_value(new_node, node)

        if _is_match(True, "<more**kwargs>"):
            new_node = add_parse_tree_node(node, "<more**kwargs>")
            _more_kwargs(new_node, node)

        return

    return


# 315-316
def _more_kwargs(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 297
    if _is_match(True, ",", node):
        index += 1

        if _is_match(True, "<insert**kwargs>"):
            new_node = add_parse_tree_node(node, "<insert**kwargs>")
            _insert_kwargs(new_node, node)

        if _is_match(True, "<more**kwargs>"):
            new_node = add_parse_tree_node(node, "<more**kwargs>")
            _more_kwargs(new_node, node)
        return

    return


# 317-318
def _add_argument(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 299
    if _is_match(True, ",", node):
        index += 1

        if _is_match(True, "<argument>"):
            new_node = add_parse_tree_node(node, "<argument>")
            _argument(new_node, node)

        return

    return


# 319-320
def _2D_argument(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<all-type-value>"):
        new_node = add_parse_tree_node(node, "<all-type-value>")
        _all_type_value(new_node, node)

        if _is_match(True, "<add-2D-argument>"):
            new_node = add_parse_tree_node(node, "<add-2D-argument>")
            _add_2D_argument(new_node, node)

        return

    elif _is_match(True, "#", node):
        index += 2

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<all-type-value>"):
            new_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(new_node, node)

        if _is_match(True, "<add-3D-argument>"):
            new_node = add_parse_tree_node(node, "<add-3D-argument>")
            _add_3D_argument(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(True, "<add-2D-argument>"):
            new_node = add_parse_tree_node(node, "<add-2D-argument>")
            _add_2D_argument(new_node, node)

        return

    return


# 321-322
def _add_2D_argument(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, ",", node):
        index += 1

        if _is_match(True, "<2D-argument>"):
            new_node = add_parse_tree_node(node, "<2D-argument>")
            _2D_argument(new_node, node)

        return

    return


# 323-324
def _add_3D_argument(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, ",", node):
        index += 1

        if _is_match(True, "<all-type-value>"):
            new_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(new_node, node)

        if _is_match(True, "<add-3D-argument>"):
            new_node = add_parse_tree_node(node, "<add-3D-argument>")
            _add_3D_argument(new_node, node)

        return
    return


# 325-326
def _function(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<common-type>"):
        new_node = add_parse_tree_node(node, "<common-type>")
        _common_type(new_node, node)

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<parameter>"):
            new_node = add_parse_tree_node(node, "<parameter>")
            _parameter(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<statement>"):
            new_node = add_parse_tree_node(node, "<statement>")
            _statement(new_node, node)

        if _is_match(False, "regrow", node):
            index += 1

        if _is_match(True, "<all-type-value>"):
            new_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(new_node, node)

        if _is_match(True, "<add-at>"):
            new_node = add_parse_tree_node(node, "<add-at>")
            _add_at(new_node, node)

        if _is_match(False, ";", node):
            index += 1

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<function>"):
            new_node = add_parse_tree_node(prev_node, "<function>")
            _function(new_node, prev_node)

        return

    elif _is_match(True, "viola", node):
        index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<undefined-param>"):
            new_node = add_parse_tree_node(node, "<undefined-param>")
            _undefined_param(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, "(", node):
            index += 2

        if _is_match(True, "<statement>"):
            new_node = add_parse_tree_node(node, "<statement>")
            _statement(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(False, ";", node):
            index += 1

        if _is_match(True, "<function>"):
            new_node = add_parse_tree_node(prev_node, "<function>")
            _function(new_node, prev_node)

        return
    return


# 328-329
def _add_at(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<more-value>"):
        new_node = add_parse_tree_node(node, "<more-value>")
        _more_value(new_node, node)

        if _is_match(False, "at", node):
            index += 1

        if _is_match(True, "<all-type-value>"):
            new_node = add_parse_tree_node(node, "<all-type-value>")
            _all_type_value(new_node, node)

        return
    return


# 330-334
def _common_variable(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "tint", node):
        index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<tint-value>"):
            new_node = add_parse_tree_node(node, "<tint-value>")
            _tint_value(new_node, node)
        return

    elif _is_match(True, "flora", node):
        index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<flora-value>"):
            new_node = add_parse_tree_node(node, "<flora-value>")
            _flora_value(new_node, node)
        return

    elif _is_match(True, "chard", node):
        index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<chard-value>"):
            new_node = add_parse_tree_node(node, "<chard-value>")
            _chard_value(new_node, node)
        return

    elif _is_match(True, "string", node):
        index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<string-value>"):
            new_node = add_parse_tree_node(node, "<string-value>")
            _string_value(new_node, node)
        return

    elif _is_match(True, "bloom", node):
        index += 1

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<bloom-value>"):
            new_node = add_parse_tree_node(node, "<bloom-value>")
            _bloom_value(new_node, node)
        return
    return


# 335-339
def _parameter(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<undefined-param>") and lexemes[index + 1] == "*#":
        new_node = add_parse_tree_node(node, "<undefined-param>")
        _undefined_param(new_node, node)
        return

    elif _is_match(True, "<common-variable>"):
        new_node = add_parse_tree_node(node, "<common-variable>")
        _common_variable(new_node, node)

        if _is_match(True, "<next-parameter>"):
            new_node = add_parse_tree_node(node, "<next-parameter>")
            _next_parameter(new_node, node)

        return

    elif _is_match(True, "<sqnc-type>"):
        new_node = add_parse_tree_node(node, "<sqnc-type>")
        _sqnc_type(new_node, node)

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<sqnc-value>"):
            new_node = add_parse_tree_node(node, "<sqnc-value>")
            _sqnc_value(new_node, node)

        if _is_match(True, "<next-parameter>"):
            new_node = add_parse_tree_node(node, "<next-parameter>")
            _next_parameter(new_node, node)

        return

    elif _is_match(True, "#", node):
        index += 2

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<2D-parameter>"):
            new_node = add_parse_tree_node(node, "<2D-parameter>")
            _2D_parameter(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(True, "<next-parameter>"):
            new_node = add_parse_tree_node(node, "<next-parameter>")
            _next_parameter(new_node, node)

        return
    return


# 340-342
def _undefined_param(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<common-type>"):
        new_node = add_parse_tree_node(node, "<common-type>")
        _common_type(new_node, node)

        if _is_match(False, "*#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        if _is_match(True, "<add-kwargs>"):
            new_node = add_parse_tree_node(node, "<add-kwargs>")
            _add_kwargs(new_node, node)

    return


# 343-344
def _add_kwargs(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, ",", node):
        index += 1

        if _is_match(False, "**#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        return
    return


# 345-346
def _next_parameter(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 328
    if _is_match(True, ",", node):
        index += 1

        if _is_match(True, "<parameter>"):
            new_node = add_parse_tree_node(node, "<parameter>")
            _parameter(new_node, node)

        return
    return


# 347-350
def _2D_parameter(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<undefined-param>"):
        new_node = add_parse_tree_node(node, "<undefined-param>")
        _undefined_param(new_node, node)
        return

    elif _is_match(True, "<common-variable>"):
        new_node = add_parse_tree_node(node, "<common-variable>")
        _common_variable(new_node, node)

        if _is_match(True, "<next-2D-param>"):
            new_node = add_parse_tree_node(node, "<next-2D-param>")
            _next_2D_param(new_node, node)
        return

    elif _is_match(True, "<sqnc-type>"):
        new_node = add_parse_tree_node(node, "<sqnc-type>")
        _sqnc_type(new_node, node)

        if _is_match(False, "#", node):
            index += 2

        if _is_match(True, "<sqnc-value>"):
            new_node = add_parse_tree_node(node, "<sqnc-value>")
            _sqnc_value(new_node, node)

        if _is_match(True, "<next-2D-param>"):
            new_node = add_parse_tree_node(node, "<next-2D-param>")
            _next_2D_param(new_node, node)
        return

    elif _is_match(True, "#", node):
        index += 2

        if _is_match(False, "(", node):
            index += 1

        if _is_match(True, "<3D-parameter>"):
            new_node = add_parse_tree_node(node, "<3D-parameter>")
            _3D_parameter(new_node, node)

        if _is_match(False, ")", node):
            index += 1

        if _is_match(True, "<next-2D-param>"):
            new_node = add_parse_tree_node(node, "<next-2D-param>")
            _next_2D_param(new_node, node)
        return
    return


# 351-352
def _next_2D_param(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, ",", node):
        index += 1

        if _is_match(True, "<2D-parameter>"):
            new_node = add_parse_tree_node(node, "<2D-parameter>")
            _2D_parameter(new_node, node)

        return
    return


# 353-355
def _3D_parameter(node: classmethod, prev_node: classmethod) -> None:
    global index

    if _is_match(True, "<undefined-param>"):
        new_node = add_parse_tree_node(node, "<undefined-param>")
        _undefined_param(new_node, node)
        return

    elif _is_match(True, "<common-variable>"):
        new_node = add_parse_tree_node(node, "<common-variable>")
        _common_variable(new_node, node)

        if _is_match(True, "<next-3D-param>"):
            new_node = add_parse_tree_node(node, "<next-3D-param>")
            _next_3D_param(new_node, node)
        return

    elif _is_match(True, "<sqnc-type>"):
        new_node = add_parse_tree_node(node, "<sqnc-type>")
        _sqnc_type(new_node, node)

        if _is_match(False, "#", node):
            add_parse_tree_node(node, lexemes[index + 1])
            index += 2

        if _is_match(True, "<sqnc-value>"):
            new_node = add_parse_tree_node(node, "<sqnc-value>")
            _sqnc_value(new_node, node)

        if _is_match(True, "<next-3D-param>"):
            new_node = add_parse_tree_node(node, "<next-3D-param>")
            _next_3D_param(new_node, node)
        return
    return


# 356-357
def _next_3D_param(node: classmethod, prev_node: classmethod) -> None:
    global index

    # 339
    if _is_match(True, ",", node):
        index += 1

        if _is_match(True, "<3D-parameter>"):
            new_node = add_parse_tree_node(node, "<3D-parameter>")
            _3D_parameter(new_node, node)
        return
    return
