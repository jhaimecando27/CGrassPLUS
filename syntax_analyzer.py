import redef as rd
import grammar as g

errors = []
line_number = 1
index = 0
tokens = []
lexemes = []


def is_syntax_valid(output_instance: object, lexer_output: object) -> bool:
    global index, errors, line_number, tokens, lexemes

    avoid = ["<space>", "<--", "-->", "?"]
    lexer_output = [x for x in lexer_output if x[1] not in avoid]

    lexer_output.append(("EOF", "EOF"))

    print(lexer_output)

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
    return True


def _is_match(_continue: bool, expected: str) -> bool:
    global index, lexemes, tokens, errors, line_number

    if errors:
        return False

    while lexemes[index] == "<newline>":
        print(f"Skipping {lexemes[index]}")
        line_number += 1
        index += 1

    if g.FIRST_SET.get(expected) is not None and g.FOLLOW_SET.get(expected) is not None:
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
        errors.append((lexemes[index], f"Syntax Error: Expecting {g.FIRST_SET[expected]} but found "))
        return False

    if tokens[index] == expected:
        print(f"Matched {lexemes[index]} with {expected}")
        return True
    elif lexemes[index] == expected:
        print(f"Matched {lexemes[index]} with {expected}")
        return True

    if _continue:
        print(f"Skipping {expected}")
        return False

    print(f"Syntax Error: Expecting {expected} : But found {lexemes[index]}")
    errors.append((lexemes[index], f"Syntax Error: Expecting {expected}"))
    return False


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
    global index

    if _is_match(False, "seed"):
        index += 1

    # 2
    if _is_match(True, "<global>"):
        index += 1
        _global()

    # ----- GARDEN: START ----- #

    if _is_match(False, "garden"):
        index += 1

    if _is_match(False, "("):
        index += 1

    if _is_match(False, ")"):
        index += 1

    if _is_match(False, "("):
        index += 1

    if _is_match(True, "<statement>"):
        _statement()

    if _is_match(False, ")"):
        index += 1

    if _is_match(False, ";"):
        index += 1

    # ----- GARDEN: END ----- #

    if _is_match(True, "<function>"):
        _function()

    if _is_match(False, "plant"):
        index += 1

    return


# 2
def _global() -> None:
    global index

    # 4
    if _is_match(True, "<constant>"):
        _constant()

    # 16-21
    if _is_match(True, "<insert-variable>"):
        _insert_variable()

    if _is_match(False, ";"):
        index += 1

    if _is_match(True, "<global>"):
        _global()

    # 3: EPSILON
    return


# 4
def _constant() -> None:
    global index

    if _is_match(True, "hard"):
        index += 1

    # 5: EPSILON
    return


# 6
def _statement() -> None:
    global index
    # Note: Have _2D_statement() & _3D_statement(), modifying this method need
    # to be done to both _2D_statement() and _3D_statement() methods

    while True:
        if _is_match(True, "<use-tree>"):
            _use_tree()

        if _is_match(True, "<filter-statement>"):
            _filter_statement()

        if not _is_match(False, "<statement>"):
            break
        continue

    # 7: EPSILON
    return


# 8-15
def _filter_statement() -> None:
    global index

    # 8
    if _is_match(True, "<constant>") or _is_match(True, "<insert-variable>"):
        _constant()

        if _is_match(True, "<insert-variable>"):
            _insert_variable()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-statement>"):
            _filter_statement()
        return

    # 9
    elif _is_match(True, "<i/o-statement>"):
        _i_o_statement()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-statement>"):
            _filter_statement()
        return

    # 10
    elif _is_match(True, "leaf"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-statement>"):
            _filter_statement()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<eleaf>"):
            _eleaf()

        if _is_match(True, "<else>"):
            _else()

        if _is_match(True, "<filter-statement>"):
            _filter_statement()
        return

    # 11
    elif _is_match(True, "#"):
        index += 2

        if _is_match(True, "<check-func>"):
            _check_func()

        if _is_match(True, "<check-func>"):
            _check_func()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-statement>"):
            _filter_statement()
        return

    # 12
    elif _is_match(True, "<iterative>"):
        _iterative()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-statement>"):
            _filter_statement()
        return

    # 13
    elif _is_match(True, "clear"):
        index += 1

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-statement>"):
            _filter_statement()
        return

    # 14
    elif _is_match(True, "break"):
        index += 1

        if _is_match(False, ";"):
            index += 1
        return

    # 15: EPSILON
    return


# 16-21
def _insert_variable() -> None:
    global index

    # 16: tint
    if _is_match(True, "tint"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        # <tint-value>
        if _is_match(True, "<tint-value>"):
            _tint_value()

        # <more-tint>
        if _is_match(True, "<more-tint>"):
            _more_tint()

        return

    # 17: flora
    elif _is_match(True, "flora"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        # <flora-value>
        if _is_match(True, "<flora-value>"):
            _flora_value()

        # <more-flora>
        if _is_match(True, "<more-flora>"):
            _more_flora()

        return

    # 18: chard
    elif _is_match(True, "chard"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        # <chard-value>
        if _is_match(True, "<chard-value>"):
            _chard_value()

        # <more-chard>
        if _is_match(True, "<more-chard>"):
            _more_chard()

        return

    # 19: string
    elif _is_match(True, "string"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        # <string-value>
        if _is_match(False, "<string-value>"):
            _string_value()

        # <more-string>
        if _is_match(True, "<more-string>"):
            _more_string()

        return

    # 20: bloom
    elif _is_match(True, "bloom"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        # <bloom-value>
        if _is_match(True, "<bloom-value>"):
            _bloom_value()

        # <more-bloom>
        if _is_match(True, "<more-bloom>"):
            _more_bloom()

        return

    # 21: sqnc
    elif _is_match(True, "<sqnc-type>"):
        _sqnc_type()

        if _is_match(False, "#"):
            index += 2

        # <sqnc-value>
        if _is_match(True, "<sqnc-value>"):
            _sqnc_value()

        # <more-sqnc>
        if _is_match(True, "<more-sqnc>"):
            _more_sqnc()

        return

    return


# 22-25
def _sqnc_type() -> None:
    global index
    index += 1
    return


# 26-27
def _tint_value() -> None:
    global index

    # 26
    if _is_match(True, "="):
        index += 1

        if _is_match(True, "<tint>"):
            _tint()
            return

    # 27: EPSILON
    return


# 28-29
def _tint() -> None:
    global index

    # 28
    if (
        _is_match(True, "<tint-literals>")
        and not (
             lexemes[index + 1] not in g.FIRST_SET["<operator>"]
             or lexemes[index + 2] not in g.FIRST_SET["<operator>"]
        )
    ):
        _tint_literals()
        return

    # 29
    elif _is_match(True, "<arithmetic>"):
        _arithmetic()
        return

    return


# 30-33
def _tint_literals() -> None:
    global index

    # 30
    if _is_match(True, "Tint Literal"):
        index += 1
        return

    # 31
    elif _is_match(True, "#"):
        index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        return

    # 32
    elif _is_match(True, "lent"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(False, ")"):
            index += 1

        return

    # 33
    elif _is_match(True, "tint"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(False, ")"):
            index += 1

        return

    return


# 34-35
def _flora_value() -> None:
    global index

    # 34
    if _is_match(True, "="):
        index += 1

        if _is_match(True, "<flora>"):
            _flora()
            return

    # 35: EPSILON
    return


# 36-37
def _flora() -> None:
    global index

    # 36
    if (
        _is_match(True, "<flora-literals>")
        and not (
             lexemes[index + 1] not in g.FIRST_SET["<operator>"]
             or lexemes[index + 2] not in g.FIRST_SET["<operator>"]
        )
    ):
        _flora_literals()
        return

    # 29
    elif _is_match(True, "<arithmetic>"):
        _arithmetic()
        return

    return


# 38-39
def _arithmetic() -> None:
    global index

    # 38
    if _is_match(True, "<numerics>"):
        _numerics()

        if _is_match(True, "<operate-number>"):
            _operate_number()

        return

    elif _is_match(True, "("):
        index += 1

        if _is_match(True, "<numerics>"):
            _numerics()

        if _is_match(True, "<operator>"):
            _operator()

        if _is_match(True, "<arithmetic>"):
            _arithmetic()

        if _is_match(False, ")"):
            index += 1

        if _is_match(True, "<operate-numbers>"):
            _operate_number()

        return

    return


# 40-42
def _flora_literals() -> None:
    global index

    # 40
    if _is_match(True, "Flora Literal"):
        index += 1
        return

    # 41
    elif _is_match(True, "flora"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(False, ")"):
            index += 1

        return

    # 42
    elif _is_match(True, "<tint-literals>"):
        _tint_literals()

        return

    return


# 43-44
def _operate_number() -> None:
    global index

    # 43
    if _is_match(True, "<operator>"):
        _operator()

        if _is_match(True, "<arithmetic>"):
            _arithmetic()

    # 44: EPSILON
    return


# 45-51
def _operator() -> None:
    global index
    index += 1
    return


# 52-53
def _numerics() -> None:
    global index

    # 52
    if _is_match(True, "<tint-literals>"):
        _tint_literals()
        return

    # 53
    elif _is_match(True, "<flora-literals>"):
        _flora_literals()
        return

    return


# 54-55
def _chard_value() -> None:
    global index

    # 54
    if _is_match(True, "="):
        index += 1

        if _is_match(True, "<chard>"):
            _chard()
            return

    # 55: EPSILON
    return


# 56-58
def _chard() -> None:
    global index

    # 56
    if _is_match(True, "Chard Literal"):
        index += 1

        return

    # 57
    elif _is_match(True, "#"):
        index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        return

    # 58
    elif _is_match(True, "chard"):
        index += 1

        if _is_match(False, "("):
            index += 2

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(False, ")"):
            index += 1

        return

    return


# 59-60
def _string_value() -> None:
    global index

    # 59
    if _is_match(True, "="):
        index += 1

        if _is_match(True, "<string>"):
            _string()
            return

    # 60: EPSILON
    return


# 61-63
def _string() -> None:
    global index

    # 61
    if _is_match(True, "String Literal"):
        index += 1

        return

    # 62
    elif _is_match(True, "#"):
        index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(True, "<start-end-step>"):
            _start_end_step()

        return

    # 63
    elif _is_match(True, "string"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(True, "<start-end-step>"):
            _start_end_step()

        if _is_match(False, ")"):
            index += 1

        return

    return


# 64-65
def _concatenate() -> None:
    global index

    if _is_match(True, "<indexing>"):
        _indexing()

        if _is_match(False, "+"):
            index += 1

        if _is_match(True, "<string>"):
            _string()

        if _is_match(True, "<concatenate>"):
            _concatenate()

    # 65: EPSILON
    return


# 66-67
def _bloom_value() -> None:
    global index

    # 66
    if _is_match(True, "="):
        index += 1

        if _is_match(True, "<bloom>"):
            _bloom()
            return

    # 67: EPSILON
    return


# 68-69
def _bloom() -> None:
    global index

    # 68
    if _is_match(True, "<bloom-literals>"):
        _bloom_literals()

        if _is_match(True, "<operate-logic>"):
            _operate_logic()

        return

    # 69
    elif _is_match(True, "("):
        index += 1

        if _is_match(True, "<bloom-literals>"):
            _bloom_literals()

        if _is_match(True, "<cond-operator>"):
            _cond_operator()

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ")"):
            index += 1

        if _is_match(True, "<operate-logic>"):
            _operate_logic()

        return

    return


# 70-77
def _bloom_literals() -> None:
    global index

    # 70
    if _is_match(True, "Bloom Literal"):
        index += 1
        return

    # 71
    elif _is_match(True, "bloom"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(False, ")"):
            index += 1

        return

    # 72
    elif _is_match(True, "<tint>"):
        _tint()
        return

    # 73
    elif _is_match(True, "<flora>"):
        _flora()
        return

    # 74
    elif _is_match(True, "<chard>"):
        _chard()
        return

    # 75
    elif _is_match(True, "<string>"):
        _string()
        return

    # 76
    elif _is_match(True, "<sqnc>"):
        _sqnc()
        return

    # 77
    elif _is_match(True, "bare"):
        index += 1
        return

    return


# 78-79
def _operate_logic() -> None:
    global index

    # 78
    if _is_match(True, "<cond-operator>"):
        _cond_operator()

        if _is_match(True, "<bloom>"):
            _bloom()

    # 79: EPSILON
    return


# 80-89
def _cond_operator() -> None:
    global index
    index += 1
    return


# 90-91
def _insert_func() -> None:
    global index

    # 90
    if _is_match(True, "("):
        index += 1

        if _is_match(True, "<argument>"):
            _argument()

        if _is_match(False, ")"):
            index += 1

        if _is_match(True, "<instance-grab>"):
            _instance_grab()

        return

    # 91: EPSILON
    return


# 92-93
def _instance_grab() -> None:
    global index

    # 92
    if _is_match(True, "."):
        index += 1

        if _is_match(False, "#"):
            index += 2

    # 93: EPSILON
    return


# 94-95
def _indexing() -> None:
    global index

    # 94
    if _is_match(True, "["):
        index += 1

        if _is_match(True, "<insert-index>"):
            _insert_index()

        if _is_match(False, "]"):
            index += 1

        if _is_match(True, "<indexing>"):
            _indexing()

        return

    # 95: EPSILON
    return


# 96-97
def _insert_index() -> None:
    global index

    # 96
    if _is_match(True, "Tint Literal"):
        index += 1
        return

    # 97
    elif _is_match(True, "Flora Literal"):
        index += 1
        return

    return


# 98-99
def _more_tint() -> None:
    global index

    # 98
    if _is_match(True, ","):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<tint-value>"):
            _tint_value()

        if _is_match(True, "<more-tint>"):
            _more_tint()

        return

    # 99: EPSILON
    return


# 100-101
def _more_flora() -> None:
    global index

    # 100
    if _is_match(True, ","):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<flora-value>"):
            _flora_value()

        if _is_match(True, "<more-flora>"):
            _more_flora()

        return

    # 101: EPSILON
    return


# 102-103
def _more_chard() -> None:
    global index

    # 102
    if _is_match(True, ","):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<chard-value>"):
            _chard_value()

        if _is_match(True, "<more-chard>"):
            _more_chard()

        return

    # 103: EPSILON
    return


# 104-105
def _more_string() -> None:
    global index

    # 104
    if _is_match(True, ","):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<string-value>"):
            _string_value()

        if _is_match(True, "<more-string>"):
            _more_string()

        return

    # 105: EPSILON
    return


# 106-107
def _more_bloom() -> None:
    global index

    # 106
    if _is_match(True, ","):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<bloom-value>"):
            _bloom_value()

        if _is_match(True, "<more-bloom>"):
            _more_bloom()

        return

    # 107: EPSILON
    return


# 108-109
def _sqnc_value() -> None:
    global index

    # 108
    if _is_match(True, "="):
        index += 1

        if _is_match(True, "<sqnc>"):
            _sqnc()
            return

        if _is_match(True, "<concatenate>"):
            _concatenate()
            return

    # 109: EPSILON
    return


# 110-111
def _more_sqnc() -> None:
    global index

    # 110
    if _is_match(True, ","):
        index += 1

        if _is_match(True, "#"):
            index += 2

        if _is_match(True, "<sqnc-value>"):
            _sqnc_value()

        if _is_match(True, "<more-sqnc>"):
            _more_sqnc()

        return

    # 111: EPSILON
    return


# 112-113
def _more_id() -> None:
    global index

    if _is_match(True, ","):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(True, "<more-id>"):
            _more_id()

    # 113: EPSILON
    return


# 114-117
def _sqnc() -> None:
    global index

    # 114
    if _is_match(True, "<open>"):
        _open()

        if _is_match(True, "<dirt>"):
            _dirt()

        if _is_match(True, "<sequence>"):
            _sequence()

        if _is_match(False, "<close>"):
            _close()

        return

    # 115
    elif _is_match(True, "<supply-dirt>"):
        _supply_dirt()

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(False, ")"):
            index += 1

        return

    # 116
    elif _is_match(True, "#"):
        index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(True, "<start-end-step>"):
            _start_end_step()

        return

    # 117
    elif _is_match(True, "<sqnc-type>"):
        _sqnc_type()

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(True, "<start-end-step>"):
            _start_end_step()

        if _is_match(False, ")"):
            index += 1

        return

    return


# 118-120
def _supply_dirt() -> None:
    global index
    index += 1
    return


# 121-122
def _open() -> None:
    global index
    index += 1
    return


# 123-124
def _dirt() -> None:
    global index

    # 123
    if _is_match(True, "String Literal"):
        index += 1

        if _is_match(False, ":"):
            index += 1
        return

    # 124: EPSILON
    return


# 125-126
def _close() -> None:
    global index
    index += 1
    return


# 127-128
def _sequence() -> None:
    global index

    # 127
    if _is_match(True, "<common-data>"):
        _common_data()

        if _is_match(True, "<next-sqnc>"):
            _next_sqnc()

        return

    # 128
    elif _is_match(True, "<open>"):
        _open()

        if _is_match(True, "<dirt>"):
            _dirt()

        if _is_match(True, "<2D-sqnc>"):
            _2D_sqnc()

        if _is_match(True, "<close>"):
            _close()

        if _is_match(True, "<next_sqnc>"):
            _next_sqnc()

        return

    return


# 129-133
def _common_data() -> None:
    global index

    # 129
    if _is_match(True, "<tint>"):
        _tint()
        return

    # 130
    elif _is_match(True, "<flora>"):
        _flora()
        return

    # 131
    elif _is_match(True, "<chard>"):
        _chard()
        return

    # 132
    elif _is_match(True, "<string>"):
        _string()
        return

    # 133
    elif _is_match(True, "<bloom>"):
        _bloom()
        return

    return


# 134-135
def _next_sqnc() -> None:
    global index

    # 134
    if _is_match(True, ","):
        index += 1

        if _is_match(False, "<sequence>"):
            _sequence()

        return

    # 135: EPSILON
    return


# 136-137
def _2D_sqnc() -> None:
    global index

    # 136
    if _is_match(True, "<common-data>"):
        _common_data()

        if _is_match(True, "<next-2D-sqnc>"):
            _next_2D_sqnc()

        return

    # 137
    elif _is_match(True, "<open>"):
        _open()

        if _is_match(True, "<dirt>"):
            _dirt()

        if _is_match(True, "<common-data>"):
            _common_data()

        if _is_match(True, "<next-3D-sqnc>"):
            _next_3D_sqnc()

        if _is_match(True, "<close>"):
            _close()

        if _is_match(True, "<next-2D-sqnc>"):
            _next_2D_sqnc()

        return

    return


# 138-139
def _next_2D_sqnc() -> None:
    global index

    # 138
    if _is_match(True, ","):
        index += 1

        if _is_match(True, "<2D-sqnc>"):
            _2D_sqnc()

        return

    # 139: EPSILON
    return


# 140-141
def _next_3D_sqnc() -> None:
    global index

    # 140
    if _is_match(True, ","):
        index += 1

        if _is_match(True, "<common-data>"):
            _common_data()

        if _is_match(True, "<next-3D-sqnc>"):
            _next_3D_sqnc()

        return

    # 141: EPSILON
    return


# 142-143
def _start_end_step() -> None:
    global index

    # 142
    if _is_match(True, "["):
        index += 1

        if _is_match(True, "<insert_start>"):
            _insert_start()

        return

    # 143: EPSILON
    return


# ]] 144-145
def _insert_start() -> None:
    global index

    # 144
    if _is_match(True, "Tint Literal"):
        index += 1

        if _is_match(False, ":"):
            index += 1

        if _is_match(True, "<close-start>"):
            _close_start()

        return

    # 145
    elif _is_match(True, ":"):
        index += 1

        if _is_match(True, "<skip-start>"):
            _skip_start()

        return

    return


# 146-147
def _close_start() -> None:
    global index

    # 146
    if _is_match(True, "<close-end>"):
        _close_end()
        return

    # 147
    elif _is_match(True, "Tint Literal"):
        index += 1

        if _is_match(True, "<close-end>"):
            _close_end()

        return

    return


# 148-149
def _close_end() -> None:
    global index

    # 148
    if _is_match(True, "]"):
        index += 1

        if _is_match(True, "<2D-start-end-step>"):
            _2D_start_end_step()

        return

    # 149
    elif _is_match(True, ":"):
        index += 1

        if _is_match(True, "Tint Literal"):
            index += 1

        if _is_match(False, "]"):
            index += 1

        if _is_match(True, "<2D-start-end-step>"):
            _2D_start_end_step()

        return

    return


# 150-151
def _skip_start() -> None:
    global index

    # 150
    if _is_match(True, "Tint Literal"):
        index += 1

        if _is_match(True, "<close-end>"):
            _close_end()

        if _is_match(True, "<2D-start-end-step>"):
            _2D_start_end_step()

        return

    # 151
    elif _is_match(True, ":"):
        index += 1

        if _is_match(True, "Tint Literal"):
            index += 1

        if _is_match(False, "]"):
            index += 1

        if _is_match(True, "<2D-start-end-step>"):
            _2D_start_end_step()

        return

    return


# 152-153
def _2D_start_end_step() -> None:
    global index

    # 152
    if _is_match(True, "["):
        index += 1

        if _is_match(True, "<2D-insert-start>"):
            _2D_insert_start()

        return

    # ]] 153: EPSILON
    return


# 154-155
def _2D_insert_start() -> None:
    global index

    # 154
    if _is_match(True, "Tint Literal"):
        index += 1

        if _is_match(False, ":"):
            index += 1

        if _is_match(True, "<2D-close-start>"):
            _2D_close_start()

        return

    # 145
    elif _is_match(True, ":"):

        if _is_match(True, "<2D-skip-start>"):
            _2D_skip_start()

        return

    return


# 156-157
def _2D_close_start() -> None:
    global index

    # 156
    if _is_match(True, "<2D-close-end>"):
        _2D_close_end()
        return

    # 157
    elif _is_match(True, "Tint Literal"):
        index += 1

        if _is_match(True, "<2D-close-end>"):
            _2D_close_end()

        return

    return


# 158-159
def _2D_close_end() -> None:
    global index

    # 158
    if _is_match(True, "]"):
        index += 1

        if _is_match(True, "<3D-start-end-step>"):
            _3D_start_end_step()

        return

    # 159
    elif _is_match(True, ":"):
        index += 1

        if _is_match(True, "Tint Literal"):
            index += 1

        if _is_match(False, "]"):
            index += 1

        if _is_match(True, "<3D-start-end-step>"):
            _3D_start_end_step()

        return

    return


# 160-161
def _2D_skip_start() -> None:
    global index

    # 160
    if _is_match(True, "Tint Literal"):
        index += 1

        if _is_match(True, "<2D-close-end>"):
            _2D_close_end()

        if _is_match(True, "<3D-start-end-step>"):
            _3D_start_end_step()

        return

    # 161
    elif _is_match(True, ":"):
        index += 1

        if _is_match(True, "Tint Literal"):
            index += 1

        if _is_match(False, "]"):
            index += 1

        if _is_match(True, "<3D-start-end-step>"):
            _3D_start_end_step()

        return

    return


# 162-163
def _3D_start_end_step() -> None:
    global index

    # 162
    if _is_match(True, "["):
        index += 1

        if _is_match(True, "<3D-insert-start>"):
            _3D_insert_start()

        return

    # 163: EPSILON
    return


# 164-165
def _3D_insert_start() -> None:
    global index

    # 164
    if _is_match(True, "Tint Literal"):
        index += 1

        if _is_match(False, ":"):
            index += 1

        if _is_match(True, "<3D-close-start>"):
            _3D_close_start()

        return

    # 165
    elif _is_match(True, ":"):
        index += 1

        if _is_match(True, "<3D-skip-start>"):
            _3D_skip_start()

        return

    return


# 166-167
def _3D_close_start() -> None:
    global index

    # 166
    if _is_match(True, "<3D-close-end>"):
        _3D_close_end()
        return

    # 167
    elif _is_match(True, "Tint Literal"):
        index += 1

        if _is_match(True, "<3D-close-end>"):
            _3D_close_end()

        return

    return


# 168-169
def _3D_close_end() -> None:
    global index

    # 168
    if _is_match(True, "]"):
        index += 1
        return

    # 169
    elif _is_match(True, ":"):
        index += 1

        if _is_match(True, "Tint Literal"):
            index += 1

        if _is_match(False, "]"):
            index += 1

        return

    return


# 170-171
def _3D_skip_start() -> None:
    global index

    # 170
    if _is_match(True, "Tint Literal"):
        index += 1

        if _is_match(True, "<3D-close-end>"):
            _3D_close_end()

        return

    # 171
    elif _is_match(True, ":"):
        index += 1

        if _is_match(True, "Tint Literal"):
            index += 1

        if _is_match(False, "]"):
            index += 1

        return

    return


# 172-174
def _all_type_value() -> None:
    global index

    # 172
    if _is_match(True, "<common-data>"):
        _common_data()
        return

    # 173
    elif _is_match(True, "<sqnc>"):
        _sqnc()
        return

    # 174
    elif _is_match(True, "inpetal"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "String Literal"):
            index += 1

        if _is_match(False, ")"):
            index += 1

        return

    return


# 175-176
def _i_o_statement() -> None:
    global index

    # 175
    if _is_match(True, "<insert-inpetal>"):
        _insert_inpetal()

        if _is_match(True, "inpetal"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "String Literal"):
            index += 1

        if _is_match(False, ")"):
            index += 1

        return

    # 176
    elif _is_match(True, "mint"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<all-type-value>"):
            _all_type_value()

        if _is_match(False, ")"):
            index += 1

        return


# 177-179
def _insert_inpetal() -> None:
    global index

    # 177
    if _is_match(True, "<common-type>"):
        _common_type()

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(False, "="):
            index += 1

        return

    # 178
    elif _is_match(True, "<sqnc-type>"):
        _sqnc_type()

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(False, "="):
            index += 1

        return

    # 179
    elif _is_match(True, "#"):
        index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(False, "="):
            index += 1

        return

    return


# 180-184
def _common_type() -> None:
    global index
    index += 1
    return


# 185-186
def _eleaf() -> None:
    global index

    # 185
    if _is_match(True, "eleaf"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-statement>"):
            _filter_statement()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<eleaf>"):
            _eleaf()

        return

    # 186: EPSILON
    return


# 187-188
def _2D_eleaf() -> None:
    global index

    # 185
    if _is_match(True, "eleaf"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            _filter_2D_state()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    # 186: EPSILON
    return


# 189-190
def _3D_eleaf() -> None:
    global index

    # 185
    if _is_match(True, "eleaf"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            _filter_3D_state()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    # 186: EPSILON
    return


# 191-192
def _final_eleaf() -> None:
    global index

    # 191
    if _is_match(True, "eleaf"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            _filter_final_state()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    # 192: EPSILON
    return


# 193-194
def _else() -> None:
    global index

    # 193
    if _is_match(True, "moss"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-statement>"):
            _filter_statement()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    # 194: EPSILON
    return


# 195-196
def _2D_else() -> None:
    global index

    # 195
    if _is_match(True, "moss"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            _filter_2D_state()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    # 196: EPSILON
    return


# 197-198
def _3D_else() -> None:
    global index

    # 197
    if _is_match(True, "moss"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            _filter_3D_state()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    # 198: EPSILON
    return


# 199-200
def _final_else() -> None:
    global index

    # 199
    if _is_match(True, "moss"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            _filter_final_state()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    # 200: EPSILON
    return


# 201-202
def _iterative() -> None:
    global index

    # 201
    if _is_match(True, "fern"):
        index += 1

        if _is_match(False, "("):
            print("here")
            index += 1

        if _is_match(True, "<insert-fern>"):
            _insert_fern()

        return

    # 202
    elif _is_match(True, "willow"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<2D-statement>"):
            _2D_statement()

        if _is_match(False, ")"):
            index += 1

        return
    return


# 203-204
def _insert_fern() -> None:
    global index

    # 203
    if _is_match(True, "tint"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(False, "="):
            index += 1

        if _is_match(True, "Tint Literal"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ";"):
            index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<assignment-op>"):
            _assignment_op()

        if _is_match(True, "<flora>"):
            _flora()

        if _is_match(False, ";"):
            index += 1

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<2D-statement>"):
            _2D_statement()

        if _is_match(False, ")"):
            index += 1

        return

    # 204
    elif _is_match(True, "<all-type-value"):
        _all_type_value()

        if _is_match(True, "<more-value>"):
            _more_value()

        if _is_match(False, "at"):
            index += 1

        if _is_match(True, "<sqnc-value>"):
            _sqnc_value()

        if _is_match(False, ";"):
            index += 1

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<2D-statement>"):
            _2D_statement()

        if _is_match(False, ")"):
            index += 1

        return

    return


# 205-212
def _assignment_op() -> None:
    global index
    index += 1
    return


# 213-214
def _more_value() -> None:
    global index

    # 213
    if _is_match(True, ","):
        index += 1

        if _is_match(True, "<all-type-value>"):
            _all_type_value()

        if _is_match(True, "<final-value>"):
            _final_value()

        return

    # 214: EPSILON
    return


# 215-216
def _final_value() -> None:
    global index

    # 215
    if _is_match(True, ","):
        index += 1

        if _is_match(True, "<all-type-value>"):
            _all_type_value()
        return

    # 216: EPSILON
    return


# 217-218
def _use_tree() -> None:
    global index

    # 217
    if _is_match(True, "tree"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "branch"):
            index += 1

        if _is_match(True, "<check-branch>"):
            _check_branch()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    # 218: EPSILON
    return


# 219-220
def _check_branch() -> None:
    global index

    # 219
    if _is_match(True, "<all-type-value>"):
        _all_type_value()

        if _is_match(True, "<insert-branch>"):
            _insert_branch()

        if _is_match(True, "<more-branch>"):
            _more_branch()

        return

    # 220
    elif _is_match(True, "_"):
        index += 1

        if _is_match(False, ":"):
            index += 1

        if _is_match(True, "<filter-statement>"):
            _filter_statement()

        return

    return


# 221-222
def _insert_branch() -> None:
    global index

    # 221
    if _is_match(True, ":"):
        index += 1

        if _is_match(True, "<filter-statement>"):
            _filter_statement()

        return

    # 222
    elif _is_match(True, "leaf"):
        index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-statement>"):
            _filter_statement()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    return


# 223-224
def _more_branch() -> None:
    global index

    # 223
    if _is_match(True, "branch"):
        index += 1

        if _is_match(True, "<check-branch>"):
            _check_branch()

        return

    # 224: EPSILON
    return


# 225-226
def _2D_statement() -> None:
    global index
    # Note: Have _statement() & _3D_statement(), modifying this method need to
    # be done to both _statement() and _3D_statement() methods

    # 225
    while True:
        if _is_match(True, "<use-2D-tree>"):
            _use_2D_tree()

        elif _is_match(True, "<filter-2D-state>"):
            _filter_2D_state()

        elif _is_match(True, "<2D-statement>"):
            break
        continue

    # 226: EPSILON
    return


# 227-228
def _use_2D_tree() -> None:
    global index

    # 227
    if _is_match(True, "tree"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "branch"):
            index += 1

        if _is_match(True, "<check-2D-branch>"):
            _check_2D_branch()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    # 228: EPSILON
    return


# 229-230
def _check_2D_branch() -> None:
    global index

    # 229
    if _is_match(True, "<all-type-value>"):
        _all_type_value()

        if _is_match(True, "<insert-2D-branch>"):
            _insert_2D_branch()

        if _is_match(True, "<more-2D-branch>"):
            _more_2D_branch()

        return

    # 230
    elif _is_match(True, "_"):
        index += 1

        if _is_match(False, ":"):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            _filter_2D_state()

        return

    return


# 231-232
def _insert_2D_branch() -> None:
    global index

    # 231
    if _is_match(True, ":"):
        index += 1

        if _is_match(True, "<filter-2D-state>"):
            _filter_2D_state()

        return

    # 232
    elif _is_match(True, "leaf"):
        index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            _filter_2D_state()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    return


# 233-234
def _more_2D_branch() -> None:
    global index

    # 233
    if _is_match(True, "branch"):
        index += 1

        if _is_match(True, "<check-2D-branch>"):
            _check_2D_branch()

        return

    # 234: EPSILON
    return


# 235-242
def _filter_2D_state() -> None:
    global index

    # 235
    if _is_match(True, "<constant>") or _is_match(True, "<insert-variable>"):
        if _is_match(True, "<constant>"):
            _constant()

        if _is_match(True, "<insert-variable>"):
            _insert_variable()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            _filter_2D_state()

        return
    # 238
    elif _is_match(True, "#") or (_is_match(True, "#") and _is_match(True, "<assignment-op")):
        index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(True, "<more-id>"):
            _more_id()

        if _is_match(False, "<assignment-op>"):
            _assignment_op()

        if _is_match(True, "<all-type-value>"):
            _all_type_value()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            _filter_2D_state()

        return


    # 236
    elif _is_match(True, "<i/o-statement>"):
        if _is_match(True, "<i/o-statement>"):
            _i_o_statement()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-2D-state"):
            _filter_2D_state()

    # 237
    elif _is_match(True, "leaf"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-2D-state"):
            _filter_2D_state()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<2D-eleaf>"):
            _2D_eleaf()

        if _is_match(True, "<2D-else>"):
            _2D_else()

        if _is_match(True, "<filter-2D-state"):
            _filter_2D_state()

        return

    # 239
    elif _is_match(True, "<2D-iterative>"):
        if _is_match(True, "<2D-iterative>"):
            _2D_iterative()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            _filter_2D_state()

        return

    # 240
    elif _is_match(True, "clear"):
        index += 1

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-2D-state>"):
            _filter_2D_state()

        return

    # 241
    elif _is_match(True, "break"):
        index += 1

        if _is_match(False, ";"):
            index += 1

        return

    # 242: EPSILON
    return


# 243-244
def _2D_iterative() -> None:
    global index

    # 243
    if _is_match(False, "fern"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<insert-2D-fern>"):
            _insert_2D_fern()

        return

    # 244
    elif _is_match(True, "willow"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<3D-statement>"):
            _3D_statement()

        if _is_match(False, ")"):
            index += 1

        return
    return


# 245-246
def _insert_2D_fern() -> None:
    global index

    # 245
    if _is_match(True, "tint"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(False, "="):
            index += 1

        if _is_match(False, "Tint Literal"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ";"):
            index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(False, "<assignment-op>"):
            _assignment_op()

        if _is_match(True, "<flora>"):
            _flora()

        if _is_match(False, ";"):
            index += 1

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<3D-statement>"):
            _3D_statement()

        if _is_match(False, ")"):
            index += 1

        return

    # 246
    elif _is_match(True, "<all-type-value"):
        _all_type_value()

        if _is_match(True, "<more-value>"):
            _more_value()

        if _is_match(False, "at"):
            index += 1

        if _is_match(True, "<sqnc-value>"):
            _sqnc_value()

        if _is_match(False, ";"):
            index += 1

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<3D-statement>"):
            _2D_statement()

        if _is_match(False, ")"):
            index += 1

        return

    return


# 247-248
def _3D_statement() -> None:
    global index
    # Note: Have _statement() & _2D_statement(), modifying this method need to
    # be done to both _statement() and 2D_statement() methods

    # 247
    while True:
        if _is_match(True, "<use-3D-tree>"):
            _use_3D_tree()

        if _is_match(True, "<filter-3D-state>"):
            _filter_3D_state()

        if lexemes[index] not in g.FIRST_SET["<3D-statement>"]:
            break
        continue

    # 248: EPSILON
    return


# 249-250
def _use_3D_tree() -> None:
    global index

    # 249
    if _is_match(True, "tree"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "branch"):
            index += 1

        if _is_match(True, "<check-3D-branch>"):
            _check_3D_branch()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    # 250: EPSILON
    return


# 251-252
def _check_3D_branch() -> None:
    global index

    # 251
    if _is_match(True, "<all-type-value>"):
        _all_type_value()

        if _is_match(True, "<insert-3D-branch>"):
            _insert_3D_branch()

        if _is_match(True, "<more-3D-branch>"):
            _more_3D_branch()

        return

    # 252
    elif _is_match(True, "_"):
        index += 1

        if _is_match(False, ":"):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            _filter_3D_state()

        return

    return


# 253-254
def _insert_3D_branch() -> None:
    global index

    # 253
    if _is_match(True, ":"):
        index += 1

        if _is_match(True, "<filter-3D-state>"):
            _filter_3D_state()

        return

    # 254
    elif _is_match(True, "leaf"):
        index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            _filter_3D_state()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    return


# 255-256
def _more_3D_branch() -> None:
    global index

    # 255
    if _is_match(True, "branch"):
        index += 1

        if _is_match(True, "<check-3D-branch>"):
            _check_3D_branch()

        return

    # 256: EPSILON
    return


# 257-264
def _filter_3D_state() -> None:
    global index

    # 257
    if _is_match(True, "<constant>"):
        _constant()

        if _is_match(True, "<insert-variable>"):
            _insert_variable()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            _filter_3D_state()

        return

    # 258
    elif _is_match(True, "<i/o-statement>"):
        if _is_match(True, "<i/o-statement>"):
            _i_o_statement()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            _filter_3D_state()

    # 259
    elif _is_match(True, "leaf"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            _filter_3D_state()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<3D-eleaf>"):
            _3D_eleaf()

        if _is_match(True, "<3D-else>"):
            _3D_else()

        if _is_match(True, "<filter-3D-state"):
            _filter_3D_state()

        return

    # 260
    elif _is_match(True, "#"):
        index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(True, "<more-id>"):
            _more_id()

        if _is_match(True, "<assignment-op>"):
            _assignment_op()

        if _is_match(True, "<all-type-value>"):
            _all_type_value()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            _filter_3D_state()

        return

    # 261
    elif _is_match(True, "<3D-itertive>"):
        if _is_match(True, "<3-Diterative>"):
            _3D_iterative()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            _filter_3D_state()

        return

    # 262
    elif _is_match(True, "clear"):
        index += 1

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-3D-state>"):
            _filter_3D_state()

        return

    # 263
    elif _is_match(True, "break"):
        index += 1

        if _is_match(False, ";"):
            index += 1

        return

    # 264: EPSILON
    return


# 265-266
def _3D_iterative() -> None:
    global index

    # 265
    if _is_match(True, "fern"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<insert-3D-fern>"):
            _insert_3D_fern()

        return

    # 266
    elif _is_match(True, "willow"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<final-statement>"):
            _final_statement()

        if _is_match(False, ")"):
            index += 1

        return

    return


# 267-268
def _insert_3D_fern() -> None:
    global index

    # 267
    if _is_match(True, "tint"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(False, "="):
            index += 1

        if _is_match(False, "Tint Literal"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ";"):
            index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<assignment-op>"):
            _assignment_op()

        if _is_match(True, "<flora>"):
            _flora()

        if _is_match(False, ";"):
            index += 1

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<final-statement>"):
            _final_statement()

        if _is_match(False, ")"):
            index += 1

        return

    # 268
    elif _is_match(True, "<all-type-value"):
        _all_type_value()

        if _is_match(True, "<more-value>"):
            _more_value()

        if _is_match(False, "at"):
            index += 1

        if _is_match(True, "<sqnc-value>"):
            _sqnc_value()

        if _is_match(False, ";"):
            index += 1

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<final-statement>"):
            _final_statement()

        if _is_match(False, ")"):
            index += 1

        return

    return


# 269-270
def _final_statement() -> None:
    global index

    # 269
    if _is_match(True, "<use-final-tree>"):

        if _is_match(True, "<use-final-tree>"):
            _use_final_tree()

        if _is_match(True, "<filter-final-state>"):
            _filter_final_state()

        if _is_match(True, "<final-statement>"):
            _final_statement()

        return

    # 270: EPSILON
    return


# 271-272
def _use_final_tree() -> None:
    global index

    # 271
    if _is_match(True, "tree"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(False, "branch"):
            index += 1

        if _is_match(True, "<check-final-branch>"):
            _check_final_branch()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    # 272: EPSILON
    return


# 273-274
def _check_final_branch() -> None:
    global index

    # 273
    if _is_match(True, "<all-type-value>"):
        _all_type_value()

        if _is_match(True, "<insert-final-branch>"):
            _insert_final_branch()

        if _is_match(True, "<more-final-branch>"):
            _more_final_branch()

        return

    # 274
    elif _is_match(True, "_"):
        index += 1

        if _is_match(False, ":"):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            _filter_final_state()

        return

    return


# 275-276
def _insert_final_branch() -> None:
    global index

    # 275
    if _is_match(True, ":"):
        index += 1

        if _is_match(True, "<filter-final-state>"):
            _filter_final_state()

        return

    # 276
    elif _is_match(True, "leaf"):
        index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            _filter_final_state()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        return

    return


# 277-278
def _more_final_branch() -> None:
    global index

    # 277
    if _is_match(True, "branch"):
        index += 1

        if _is_match(True, "<check-final-branch>"):
            _check_final_branch()

        return

    # 278: EPSILON
    return


# 279-285
def _filter_final_state() -> None:
    global index

    # 279
    if _is_match(True, "<constant>") or _is_match(True, "<insert-variable>"):
        if _is_match(True, "<constant>"):
            _constant()

        if _is_match(True, "<insert-variable>"):
            _insert_variable()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            _filter_final_state()

        return

    # 280
    elif _is_match(True, "<i/o-statement>"):
        _i_o_statement()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            _filter_final_state()

    # 281
    elif _is_match(True, "leaf"):
        index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<bloom>"):
            _bloom()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            _filter_final_state()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<final-eleaf>"):
            _final_eleaf()

        if _is_match(True, "<final-else>"):
            _final_else()

        if _is_match(True, "<filter-final-state"):
            _filter_final_state()

        return

    # 282
    elif _is_match(True, "#"):
        index += 2

        if _is_match(True, "<insert-func>"):
            _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(True, "<more-id>"):
            _more_id()

        if _is_match(True, "<assignment-op>"):
            _assignment_op()

        if _is_match(True, "<all-type-value>"):
            _all_type_value()

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            _filter_final_state()

        return

    # 283
    elif _is_match(True, "clear"):
        if _is_match(True, ";"):
            index += 1

        if _is_match(True, "<filter-final-state>"):
            _filter_final_state()

        return

    # 284
    elif _is_match(True, "break"):
        index += 1

        if _is_match(False, ";"):
            index += 1

        return

    # 285: EPSILON
    return


# 286-288
def _argument() -> None:
    global index

    # 286
    if _is_match(True, "<insert-argument>"):
        _insert_argument()
        return

    # 287
    elif _is_match(True, "#"):
        index += 2

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<2D-argument>"):
            _2D_argument()

        if _is_match(False, ")"):
            index += 1

        if _is_match(True, "<add-argument>"):
            _add_argument()

        return

    # 288: EPSILON
    return


# 289-291
def _insert_argument() -> None:
    global index

    # 289
    if _is_match(True, "<all-type-value>"):
        _all_type_value()

        if _is_match(True, "<add-argument>"):
            _add_argument()

        return

    # 290
    elif _is_match(True, "#"):
        index += 2

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<2D-argument>"):
            _2D_argument()

        if _is_match(False, ")"):
            index += 1

        if _is_match(True, "<add-argument>"):
            _add_argument()

        return

    # 291: EPSILON
    return


# 292-296
def _insert_kwargs() -> None:
    global index

    # 292
    if _is_match(True, "tint"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<tint-value"):
            _tint_value()

        if _is_match(True, "<more**kwargs>"):
            _more_kwargs()

        return

    # 293
    elif _is_match(True, "flora"):
        index += 1

        if _is_match(True, "<flora-value>"):
            _flora_value()

        if _is_match(True, "<more**kwargs>"):
            _more_kwargs()

        return

    # 294
    elif _is_match(True, "chard"):
        index += 1

        if _is_match(True, "<chard-value>"):
            _chard_value()

        if _is_match(True, "<more**kwargs>"):
            _more_kwargs()

        return

    # 295
    elif _is_match(True, "string"):
        index += 1

        if _is_match(True, "<string-value>"):
            _string_value()

        if _is_match(True, "<more**kwargs>"):
            _more_kwargs()

        return

    # 296
    elif _is_match(True, "bloom"):
        index += 1

        if _is_match(True, "<bloom-value>"):
            _bloom_value()

        if _is_match(True, "<more**kwargs>"):
            _more_kwargs()

        return

    return


# 297-298
def _more_kwargs() -> None:
    global index

    # 297
    if _is_match(True, ","):
        index += 1

        if _is_match(True, "<insert**kwargs>"):
            _insert_kwargs()

        return

    # 298: EPSILON
    return


# 299-300
def _add_argument() -> None:
    global index

    # 299
    if _is_match(True, ","):
        index += 1

        if _is_match(True, "<argument>"):
            _argument()

        return

    # 300: EPSILON
    return


# 301-302
def _2D_argument() -> None:
    global index

    # 301
    if _is_match(True, "<all-type-value>"):
        _all_type_value()

        if _is_match(True, "<more-value>"):
            _more_value()

        return

    # 302
    elif _is_match(True, "#"):
        index += 2

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<all-type-value>"):
            _all_type_value()

        if _is_match(True, "add-3D-argument"):
            _add_3D_argument()

        if _is_match(False, ")"):
            index += 1

        if _is_match(True, "<add-2D-argument>"):
            _add_2D_argument()

        return

    return


# 303-304
def _add_2D_argument() -> None:
    global index

    # 303
    if _is_match(True, ","):
        index += 1

        if _is_match(True, "<2D-argument>"):
            _2D_argument()

        return

    # 304: EPSILON
    return


# 305-306
def _add_3D_argument() -> None:
    global index

    # 305
    if _is_match(True, ","):
        index += 1

        if _is_match(True, "<all-type-value>"):
            _all_type_value()

        if _is_match(True, "<add-3D-argument>"):
            _add_3D_argument()

        return

    # 306: EPSILON
    return


# 307-308
def _check_func() -> None:
    global index

    # 307
    if _is_match(True, "("):
        index += 1

        if _is_match(True, "<argument>"):
            _argument

        if _is_match(False, ")"):
            index += 1

        return

    # 308
    elif _is_match(True, "<insert-func>"):
        _insert_func()

        if _is_match(True, "<indexing>"):
            _indexing()

        if _is_match(True, "<more-id>"):
            _more_id()

        if _is_match(True, "<assignment-op>"):
            _assignment_op()

        if _is_match(True, "<all-type-value>"):
            _all_type_value()

        return

    return


# 309-311
def _function() -> None:
    global index

    # 309
    if _is_match(True, "<common-type>"):
        _common_type()

        if _is_match(False, "#"):
            index += 2

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<parameter>"):
            _parameter()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<statement>"):
            _statement()

        if _is_match(False, "regrow"):
            index += 1

        if _is_match(True, "<all-type-value>"):
            _all_type_value()

        if _is_match(True, "<add-at>"):
            _add_at()

        if _is_match(False, ";"):
            index += 1

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<function>"):
            _function()

        return

    # 310
    elif _is_match(True, "viola"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<undefined-param>"):
            _undefined_param()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, "("):
            index += 2

        if _is_match(True, "<statement>"):
            _statement()

        if _is_match(False, ")"):
            index += 1

        if _is_match(False, ";"):
            index += 1

        if _is_match(True, "<function>"):
            _function()

        return

    # 311: EPSILON
    return


# 312-313
def _add_at() -> None:
    global index

    # 312
    if _is_match(True, "<more-value>"):
        _more_value()

        if _is_match(False, "at"):
            index += 1

        if _is_match(True, "<all-type-value>"):
            _all_type_value()

        return

    # 313: EPSILON
    return


# 314-318
def _common_variable() -> None:
    global index

    # 314
    if _is_match(True, "tint"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<tint-value>"):
            _tint_value()

        return

    # 315
    elif _is_match(True, "flora"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<flora-value>"):
            _flora_value()
        return

    # 316
    elif _is_match(True, "chard"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<chard-value>"):
            _chard_value()
        return

    # 317
    elif _is_match(True, "string"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<string-value>"):
            _string_value()
        return

    # 318
    elif _is_match(True, "bloom"):
        index += 1

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<bloom-value>"):
            _bloom_value()
        return

    return


# 319-323
def _parameter() -> None:
    global index

    # 319
    if _is_match(True, "<undefined-param>") and lexemes[index + 1] == "*#":
        _undefined_param()
        return

    # 320
    elif _is_match(True, "<common-variable>"):
        _common_variable()

        if _is_match(True, "<next-parameter>"):
            _next_parameter()

        return

    # 321
    elif _is_match(True, "<sqnc-type>"):
        _sqnc_type()

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<sqnc-value>"):
            _sqnc_value()

        if _is_match(True, "<next-parameter>"):
            _next_parameter()

        return

    # 322
    elif _is_match(True, "#"):
        index += 2

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<2D-parameter>"):
            _2D_parameter()

        if _is_match(False, ")"):
            index += 1

        if _is_match(True, "<next-parameter>"):
            _next_parameter()

        return

    # 323: EPSILON
    return


# 324-325
def _undefined_param() -> None:
    global index

    # 324
    if _is_match(True, "<common-type>"):
        _common_type()

        if _is_match(False, "*#"):
            index += 2

        if _is_match(True, "<add-kwargs>"):
            _add_kwargs()

    # 325: EPSILON
    return


# 326-327
def _add_kwargs() -> None:
    global index

    # 326
    if _is_match(True, ","):
        index += 1

        if _is_match(False, "**#"):
            index += 2

        return

    # 327: EPSILON
    return


# 328-329
def _next_parameter() -> None:
    global index

    # 328
    if _is_match(True, ","):
        index += 1

        if _is_match(True, "<parameter>"):
            _parameter()

        return

    # 329: EPSILON
    return


# 330-333
def _2D_parameter() -> None:
    global index

    # 330
    if _is_match(True, "<undefined-param>"):
        _undefined_param()
        return

    # 331
    elif _is_match(True, "<common-variable>"):
        _common_variable()

        if _is_match(True, "<next-2D-param>"):
            _next_2D_param()

        return

    # 332
    elif _is_match(True, "<sqnc-type>"):
        _sqnc_type()

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<sqnc-value>"):
            _sqnc_value()

        if _is_match(True, "<next-2D-param>"):
            _next_2D_param()

        return

    # 333
    elif _is_match(True, "#"):
        index += 2

        if _is_match(False, "("):
            index += 1

        if _is_match(True, "<3D-parameter>"):
            _3D_parameter()

        if _is_match(False, ")"):
            index += 1

        if _is_match(True, "<next-2D-param>"):
            _next_2D_param()

        return

    return


# 334-335
def _next_2D_param() -> None:
    global index

    # 334
    if _is_match(True, ","):
        index += 1

        if _is_match(True, "<2D-parameter>"):
            _2D_parameter()

        return

    # 335: EPSILON
    return


# 336-338
def _3D_parameter() -> None:
    global index

    # 336
    if _is_match(True, "<undefined-param>"):
        _undefined_param()
        return

    # 337
    elif _is_match(True, "<common-variable>"):
        _common_variable()

        if _is_match(True, "<next-3D-param>"):
            _next_3D_param()

        return

    # 338
    elif _is_match(True, "<sqnc-type>"):
        _sqnc_type()

        if _is_match(False, "#"):
            index += 2

        if _is_match(True, "<sqnc-value>"):
            _sqnc_value()

        if _is_match(True, "<next-3D-param>"):
            _next_3D_param()

        return

    return


# 339-340
def _next_3D_param() -> None:
    global index

    # 339
    if _is_match(True, ","):
        index += 1

        if _is_match(True, "<3D-parameter>"):
            _3D_parameter()

        return

    # 340: EPSILON
    return
