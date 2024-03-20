from lexical_helper import Errors, skip, skip_word
import redef as rd


def is_lexical_valid(output_instance, token_instance, input_string):
    output, errors = tokenize(input_string)

    if errors:
        for error in errors:
            output_instance.set_output(f"LexicalAnalyser: {error[1]} : {error[0]}\n")
        output_instance.set_output("LexicalAnalyser: Error Found.\n")
        return False

    output_instance.set_output("LexicalAnalyser: No Errors Found.\n")
    token_instance.set_output(output)

    return True, output


def tokenize(input_string):
    tokens = []
    errors = []

    error_unknown = Errors.Unknown
    error_invalid_range = Errors.InvalidRange

    is_comment = False

    line_number = 1

    for line in input_string:
        char_index = 0

        if line[char_index] != "\n":
            line += "\n"

        while char_index < len(line):
            tmp_word = ""

            if is_comment:
                while line[char_index] != "\n":
                    if line[char_index] == "-":
                        char_index += 1
                        if line[char_index] == "-":
                            char_index += 1
                            if line[char_index] == ">":
                                char_index += 1
                                if (
                                    char_index < len(line)
                                    and line[char_index] in rd.DELIM2
                                ):
                                    tokens.append((rd.RS, "-->"))
                                    is_comment = False
                                    break
                    char_index += 1

                if is_comment:
                    break

            if line[char_index] == " ":
                tokens.append((rd.RS, "<space>"))
                char_index += 1
                continue
            elif line[char_index] == "\t":
                char_index += 1
                continue

            elif line[char_index] == "\n":
                tokens.append((rd.RS, "<newline>"))
                char_index += 1
                line_number += 1
                break

            # ---------------------- Reserved Word ---------------------- #

            # AT delim4
            if line[char_index] == "a":
                char_index += 1
                tmp_word = "a"
                if line[char_index] == "t":
                    char_index += 1
                    tmp_word += "t"
                    if line[char_index] in rd.DELIM4:
                        tokens.append((rd.RW, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM4,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue

            # bare delim1, bloom delim3, branch, delim27, break delim1
            elif line[char_index] == "b":
                char_index += 1
                tmp_word = "b"
                if line[char_index] == "a":
                    char_index += 1
                    tmp_word += "a"
                    if line[char_index] == "r":
                        char_index += 1
                        tmp_word += "r"
                        if line[char_index] == "e":
                            char_index += 1
                            tmp_word += "e"
                            print(line[char_index])
                            if line[char_index] in rd.DELIM1:
                                tokens.append((rd.RW, tmp_word))
                                continue
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIM1,
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue
                elif line[char_index] == "l":
                    char_index += 1
                    tmp_word += "l"
                    if line[char_index] == "o":
                        char_index += 1
                        tmp_word += "o"
                        if line[char_index] == "o":
                            char_index += 1
                            tmp_word += "o"
                            if line[char_index] == "m":
                                char_index += 1
                                tmp_word += "m"
                                if line[char_index] in rd.DELIM3:
                                    tokens.append((rd.RW, tmp_word))
                                    continue
                                else:
                                    # Finish whole word if error
                                    errors.append(
                                        error_unknown.delim(
                                            line_number,
                                            char_index,
                                            tmp_word,
                                            line[char_index],
                                            rd.DELIM3,
                                        )
                                    )
                                    char_index = skip(char_index, line)
                                    continue
                elif line[char_index] == "r":
                    char_index += 1
                    tmp_word += "r"
                    if line[char_index] == "a":
                        char_index += 1
                        tmp_word += "a"
                        if line[char_index] == "n":
                            char_index += 1
                            tmp_word += "n"
                            if line[char_index] == "c":
                                char_index += 1
                                tmp_word += "c"
                                if line[char_index] == "h":
                                    char_index += 1
                                    tmp_word += "h"
                                    if line[char_index] in rd.DELIM27:
                                        tokens.append((rd.RW, tmp_word))
                                        continue
                                    else:
                                        # Finish whole word if error
                                        errors.append(
                                            error_unknown.delim(
                                                line_number,
                                                char_index,
                                                tmp_word,
                                                line[char_index],
                                                rd.DELIM27,
                                            )
                                        )
                                        char_index = skip(char_index, line)
                                        continue
                    elif line[char_index] == "e":
                        char_index += 1
                        tmp_word += "e"
                        if line[char_index] == "a":
                            char_index += 1
                            tmp_word += "a"
                            if line[char_index] == "k":
                                char_index += 1
                                tmp_word += "k"
                                if line[char_index] in rd.DELIM1:
                                    tokens.append((rd.RW, tmp_word))
                                    continue
                                else:
                                    # Finish whole word if error
                                    errors.append(
                                        error_unknown.delim(
                                            line_number,
                                            char_index,
                                            tmp_word,
                                            line[char_index],
                                            rd.DELIM1,
                                        )
                                    )
                                    char_index = skip(char_index, line)
                                    continue

            # chard delim3, clear delim1
            elif line[char_index] == "c":
                char_index += 1
                tmp_word = "c"
                if line[char_index] == "h":
                    char_index += 1
                    tmp_word += "h"
                    if line[char_index] == "a":
                        char_index += 1
                        tmp_word += "a"
                        if line[char_index] == "r":
                            char_index += 1
                            tmp_word += "r"
                            if line[char_index] == "d":
                                char_index += 1
                                tmp_word += "d"
                                if line[char_index] in rd.DELIM3:
                                    tokens.append((rd.RW, tmp_word))
                                    continue
                                else:
                                    # Finish whole word if error
                                    errors.append(
                                        error_unknown.delim(
                                            line_number,
                                            char_index,
                                            tmp_word,
                                            line[char_index],
                                            rd.DELIM3,
                                        )
                                    )
                                    char_index = skip(char_index, line)
                                    continue
                elif line[char_index] == "l":
                    char_index += 1
                    tmp_word += "l"
                    if line[char_index] == "e":
                        char_index += 1
                        tmp_word += "e"
                        if line[char_index] == "a":
                            char_index += 1
                            tmp_word += "a"
                            if line[char_index] == "r":
                                char_index += 1
                                tmp_word += "r"
                                if line[char_index] in rd.DELIM1:
                                    tokens.append((rd.RW, tmp_word))
                                    continue
                                else:
                                    # Finish whole word if error
                                    errors.append(
                                        error_unknown.delim(
                                            line_number,
                                            char_index,
                                            tmp_word,
                                            line[char_index],
                                            rd.DELIM1,
                                        )
                                    )
                                    char_index = skip(char_index, line)
                                    continue

            # dirt delim3
            elif line[char_index] == "d":
                char_index += 1
                tmp_word = "d"
                if line[char_index] == "i":
                    char_index += 1
                    tmp_word += "i"
                    if line[char_index] == "r":
                        char_index += 1
                        tmp_word += "r"
                        if line[char_index] == "t":
                            char_index += 1
                            tmp_word += "t"
                            if line[char_index] in rd.DELIM3:
                                tokens.append((rd.RW, tmp_word))
                                continue
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIM3,
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue

            # eleaf delim24
            elif line[char_index] == "e":
                char_index += 1
                tmp_word = "e"
                if line[char_index] == "l":
                    char_index += 1
                    tmp_word += "l"
                    if line[char_index] == "e":
                        char_index += 1
                        tmp_word += "e"
                        if line[char_index] == "a":
                            char_index += 1
                            tmp_word += "a"
                            if line[char_index] == "f":
                                char_index += 1
                                tmp_word += "f"
                                if line[char_index] in rd.DELIM24:
                                    tokens.append((rd.RW, tmp_word))
                                    continue
                                else:
                                    # Finish whole word if error
                                    errors.append(
                                        error_unknown.delim(
                                            line_number,
                                            char_index,
                                            tmp_word,
                                            line[char_index],
                                            rd.DELIM24,
                                        )
                                    )
                                    char_index = skip(char_index, line)
                                    continue

            # false delimb, fern delim3, flora delim3, florist delim3, floral delim4
            elif line[char_index] == "f":
                char_index += 1
                tmp_word = "f"
                if line[char_index] == "a":
                    char_index += 1
                    tmp_word += "a"
                    if line[char_index] == "l":
                        char_index += 1
                        tmp_word += "l"
                        if line[char_index] == "s":
                            char_index += 1
                            tmp_word += "s"
                            if line[char_index] == "e":
                                char_index += 1
                                tmp_word += "e"
                                if line[char_index] in rd.DELIM3:
                                    tokens.append((rd.BL, tmp_word))
                                    continue
                                else:
                                    # Finish whole word if error
                                    errors.append(
                                        error_unknown.delim(
                                            line_number,
                                            char_index,
                                            tmp_word,
                                            line[char_index],
                                            rd.DELIM3,
                                        )
                                    )
                                    char_index = skip(char_index, line)
                                    continue
                elif line[char_index] == "e":
                    char_index += 1
                    tmp_word += "e"
                    if line[char_index] == "r":
                        char_index += 1
                        tmp_word += "r"
                        if line[char_index] == "n":
                            char_index += 1
                            tmp_word += "n"
                            if line[char_index] in rd.DELIM3:
                                tokens.append((rd.RW, tmp_word))
                                continue
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIM3,
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue
                elif line[char_index] == "l":
                    char_index += 1
                    tmp_word += "l"
                    if line[char_index] == "o":
                        char_index += 1
                        tmp_word += "o"
                        if line[char_index] == "r":
                            char_index += 1
                            tmp_word += "r"
                            if line[char_index] == "a":
                                char_index += 1
                                tmp_word += "a"
                                if line[char_index] in rd.DELIM3:
                                    tokens.append((rd.RW, tmp_word))
                                    continue
                                elif line[char_index] == "l":
                                    char_index += 1
                                    tmp_word += "l"
                                    if line[char_index] in rd.DELIM4:
                                        tokens.append((rd.RW, tmp_word))
                                        continue
                                    else:
                                        # Finish whole word if error
                                        errors.append(
                                            error_unknown.delim(
                                                line_number,
                                                char_index,
                                                tmp_word,
                                                line[char_index],
                                                rd.DELIM4,
                                            )
                                        )
                                        char_index = skip(char_index, line)
                                        continue
                                else:
                                    # Finish whole word if error
                                    errors.append(
                                        error_unknown.delim(
                                            line_number,
                                            char_index,
                                            tmp_word,
                                            line[char_index],
                                            rd.DELIM3,
                                        )
                                    )
                                    char_index = skip(char_index, line)
                                    continue
                            elif line[char_index] == "i":
                                char_index += 1
                                tmp_word += "i"
                                if line[char_index] == "s":
                                    char_index += 1
                                    tmp_word += "s"
                                    if line[char_index] == "t":
                                        char_index += 1
                                        tmp_word += "t"
                                        if line[char_index] in rd.DELIM3:
                                            tokens.append((rd.RW, tmp_word))
                                            continue
                                        else:
                                            # Finish whole word if error
                                            errors.append(
                                                error_unknown.delim(
                                                    line_number,
                                                    char_index,
                                                    tmp_word,
                                                    line[char_index],
                                                    rd.DELIM3,
                                                )
                                            )
                                            char_index = skip(char_index, line)
                                            continue

            # garden delim3, getItems delim24, getKeys delim24, getValues delim24
            elif line[char_index] == "g":
                char_index += 1
                tmp_word = "g"
                if line[char_index] == "a":
                    char_index += 1
                    tmp_word += "a"
                    if line[char_index] == "r":
                        char_index += 1
                        tmp_word += "r"
                        if line[char_index] == "d":
                            char_index += 1
                            tmp_word += "d"
                            if line[char_index] == "e":
                                char_index += 1
                                tmp_word += "e"
                                if line[char_index] == "n":
                                    char_index += 1
                                    tmp_word += "n"
                                    if line[char_index] in rd.DELIM3:
                                        tokens.append((rd.RW, tmp_word))
                                        continue
                                    else:
                                        # Finish whole word if error
                                        errors.append(
                                            error_unknown.delim(
                                                line_number,
                                                char_index,
                                                tmp_word,
                                                line[char_index],
                                                rd.DELIM3,
                                            )
                                        )
                                        char_index = skip(char_index, line)
                                        continue
                elif line[char_index] == "e":
                    char_index += 1
                    tmp_word += "e"
                    if line[char_index] == "t":
                        char_index += 1
                        tmp_word += "t"
                        if line[char_index] == "I":
                            char_index += 1
                            tmp_word += "I"
                            if line[char_index] == "t":
                                char_index += 1
                                tmp_word += "t"
                                if line[char_index] == "e":
                                    char_index += 1
                                    tmp_word += "e"
                                    if line[char_index] == "m":
                                        char_index += 1
                                        tmp_word += "m"
                                        if line[char_index] == "s":
                                            char_index += 1
                                            tmp_word += "s"
                                            if line[char_index] in rd.DELIM24:
                                                tokens.append((rd.RW, tmp_word))
                                                continue
                                            else:
                                                # Finish whole word if error
                                                errors.append(
                                                    error_unknown.delim(
                                                        line_number,
                                                        char_index,
                                                        tmp_word,
                                                        line[char_index],
                                                        rd.DELIM24,
                                                    )
                                                )
                                                char_index = skip(char_index, line)
                                                continue
                        elif line[char_index] == "K":
                            char_index += 1
                            tmp_word += "K"
                            if line[char_index] == "e":
                                char_index += 1
                                tmp_word += "e"
                                if line[char_index] == "y":
                                    char_index += 1
                                    tmp_word += "y"
                                    if line[char_index] == "s":
                                        char_index += 1
                                        tmp_word += "s"
                                        if line[char_index] in rd.DELIM24:
                                            tokens.append((rd.RW, tmp_word))
                                            continue
                                        else:
                                            # Finish whole word if error
                                            errors.append(
                                                error_unknown.delim(
                                                    line_number,
                                                    char_index,
                                                    tmp_word,
                                                    line[char_index],
                                                    rd.DELIM24,
                                                )
                                            )
                                            char_index = skip(char_index, line)
                                            continue
                        elif line[char_index] == "V":
                            char_index += 1
                            tmp_word += "V"
                            if line[char_index] == "a":
                                char_index += 1
                                tmp_word += "a"
                                if line[char_index] == "l":
                                    char_index += 1
                                    tmp_word += "l"
                                    if line[char_index] == "u":
                                        char_index += 1
                                        tmp_word += "u"
                                        if line[char_index] == "e":
                                            char_index += 1
                                            tmp_word += "e"
                                            if line[char_index] == "s":
                                                char_index += 1
                                                tmp_word += "s"
                                                if line[char_index] in rd.DELIM24:
                                                    tokens.append((rd.RW, tmp_word))
                                                    continue
                                                else:
                                                    # Finish whole word if error
                                                    errors.append(
                                                        error_unknown.delim(
                                                            line_number,
                                                            char_index,
                                                            tmp_word,
                                                            line[char_index],
                                                            rd.DELIM24,
                                                        )
                                                    )
                                                    char_index = skip(char_index, line)
                                                    continue

            # hard delim4
            elif line[char_index] == "h":
                char_index += 1
                tmp_word = "h"
                if line[char_index] == "a":
                    char_index += 1
                    tmp_word += "a"
                    if line[char_index] == "r":
                        char_index += 1
                        tmp_word += "r"
                        if line[char_index] == "d":
                            char_index += 1
                            tmp_word += "d"
                            if line[char_index] in rd.DELIM4:
                                tokens.append((rd.RW, tmp_word))
                                continue
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIM4,
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue

            # inpetal delim3
            elif line[char_index] == "i":
                char_index += 1
                tmp_word = "i"
                if line[char_index] == "n":
                    char_index += 1
                    tmp_word += "n"
                    if line[char_index] == "p":
                        char_index += 1
                        tmp_word += "p"
                        if line[char_index] == "e":
                            char_index += 1
                            tmp_word += "e"
                            if line[char_index] == "t":
                                char_index += 1
                                tmp_word += "t"
                                if line[char_index] == "a":
                                    char_index += 1
                                    tmp_word += "a"
                                    if line[char_index] == "l":
                                        char_index += 1
                                        tmp_word += "l"
                                        if line[char_index] in rd.DELIM3:
                                            tokens.append((rd.RW, tmp_word))
                                            continue
                                        else:
                                            # Finish whole word if error
                                            errors.append(
                                                error_unknown.delim(
                                                    line_number,
                                                    char_index,
                                                    tmp_word,
                                                    line[char_index],
                                                    rd.DELIM3,
                                                )
                                            )
                                            char_index = skip(char_index, line)
                                            continue

            # leaf delim24, lent DELIM3
            elif line[char_index] == "l":
                char_index += 1
                tmp_word = "l"
                if line[char_index] == "e":
                    char_index += 1
                    tmp_word += "e"
                    if line[char_index] == "a":
                        char_index += 1
                        tmp_word += "a"
                        if line[char_index] == "f":
                            char_index += 1
                            tmp_word += "f"
                            if line[char_index] in rd.DELIM24:
                                tokens.append((rd.RW, tmp_word))
                                continue
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIM24,
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue
                    if line[char_index] == "n":
                        char_index += 1
                        tmp_word += "n"
                        if line[char_index] == "t":
                            char_index += 1
                            tmp_word += "t"
                            if line[char_index] in rd.DELIM3:
                                tokens.append((rd.RW, tmp_word))
                                continue
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIM3,
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue

            # mint delim3, moss delim24
            elif line[char_index] == "m":
                char_index += 1
                tmp_word = "m"
                if line[char_index] == "i":
                    char_index += 1
                    tmp_word += "i"
                    if line[char_index] == "n":
                        char_index += 1
                        tmp_word += "n"
                        if line[char_index] == "t":
                            char_index += 1
                            tmp_word += "t"
                            if line[char_index] in rd.DELIM3:
                                tokens.append((rd.RW, tmp_word))
                                continue
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIM3,
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue
                elif line[char_index] == "o":
                    char_index += 1
                    tmp_word += "o"
                    if line[char_index] == "s":
                        char_index += 1
                        tmp_word += "s"
                        if line[char_index] == "s":
                            char_index += 1
                            tmp_word += "s"
                            if line[char_index] in rd.DELIM24:
                                tokens.append((rd.RW, tmp_word))
                                continue
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIM24,
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue

            # nut delim4
            elif line[char_index] == "n":
                char_index += 1
                tmp_word = "n"
                if line[char_index] == "u":
                    char_index += 1
                    tmp_word += "u"
                    if line[char_index] == "t":
                        char_index += 1
                        tmp_word += "t"
                        if line[char_index] in rd.DELIM4:
                            tokens.append((rd.RW, tmp_word))
                            continue
                        else:
                            # Finish whole word if error
                            errors.append(
                                error_unknown.delim(
                                    line_number,
                                    char_index,
                                    tmp_word,
                                    line[char_index],
                                    rd.DELIM4,
                                )
                            )
                            char_index = skip(char_index, line)
                            continue

            # plant delim2
            elif line[char_index] == "p":
                char_index += 1
                tmp_word = "p"
                if line[char_index] == "l":
                    char_index += 1
                    tmp_word += "l"
                    if line[char_index] == "a":
                        char_index += 1
                        tmp_word += "a"
                        if line[char_index] == "n":
                            char_index += 1
                            tmp_word += "n"
                            if line[char_index] == "t":
                                char_index += 1
                                tmp_word += "t"
                                if line[char_index] in rd.DELIM2:
                                    tokens.append((rd.RW, tmp_word))
                                    continue
                                else:
                                    # Finish whole word if error
                                    errors.append(
                                        error_unknown.delim(
                                            line_number,
                                            char_index,
                                            tmp_word,
                                            line[char_index],
                                            rd.DELIM2,
                                        )
                                    )
                                    char_index = skip(char_index, line)
                                    continue

            # regrow delim4
            elif line[char_index] == "r":
                char_index += 1
                tmp_word = "r"
                if line[char_index] == "e":
                    char_index += 1
                    tmp_word += "e"
                    if line[char_index] == "g":
                        char_index += 1
                        tmp_word += "g"
                        if line[char_index] == "r":
                            char_index += 1
                            tmp_word += "r"
                            if line[char_index] == "o":
                                char_index += 1
                                tmp_word += "o"
                                if line[char_index] == "w":
                                    char_index += 1
                                    tmp_word += "w"
                                    if line[char_index] in rd.DELIM4:
                                        tokens.append((rd.RW, tmp_word))
                                        continue
                                    else:
                                        # Finish whole word if error
                                        errors.append(
                                            error_unknown.delim(
                                                line_number,
                                                char_index,
                                                tmp_word,
                                                line[char_index],
                                                rd.DELIM4,
                                            )
                                        )
                                        char_index = skip(char_index, line)
                                        continue

            # seed delim16, stem delim3, string delim3
            elif line[char_index] == "s":
                char_index += 1
                tmp_word = "s"
                if line[char_index] == "e":
                    char_index += 1
                    tmp_word += "e"
                    if line[char_index] == "e":
                        char_index += 1
                        tmp_word += "e"
                        if line[char_index] == "d":
                            char_index += 1
                            tmp_word += "d"
                            if line[char_index] in rd.DELIM16:
                                tokens.append((rd.RW, tmp_word))
                                continue
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIM16,
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue
                elif line[char_index] == "t":
                    char_index += 1
                    tmp_word += "t"
                    if line[char_index] == "e":
                        char_index += 1
                        tmp_word += "e"
                        if line[char_index] == "m":
                            char_index += 1
                            tmp_word += "m"
                            if line[char_index] in rd.DELIM3:
                                tokens.append((rd.RW, tmp_word))
                                continue
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIM3,
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue
                    elif line[char_index] == "r":
                        char_index += 1
                        tmp_word += "r"
                        if line[char_index] == "i":
                            char_index += 1
                            tmp_word += "i"
                            if line[char_index] == "n":
                                char_index += 1
                                tmp_word += "n"
                                if line[char_index] == "g":
                                    char_index += 1
                                    tmp_word += "g"
                                    if line[char_index] in rd.DELIM3:
                                        tokens.append((rd.RW, tmp_word))
                                        continue
                                    else:
                                        # Finish whole word if error
                                        errors.append(
                                            error_unknown.delim(
                                                line_number,
                                                char_index,
                                                tmp_word,
                                                line[char_index],
                                                rd.DELIM3,
                                            )
                                        )
                                        char_index = skip(char_index, line)
                                        continue

            # tint delim3, tree delim24, true delimb, tulip delim3
            elif line[char_index] == "t":
                char_index += 1
                tmp_word = "t"
                if line[char_index] == "i":
                    char_index += 1
                    tmp_word += "i"
                    if line[char_index] == "n":
                        char_index += 1
                        tmp_word += "n"
                        if line[char_index] == "t":
                            char_index += 1
                            tmp_word += "t"
                            if line[char_index] in rd.DELIM3:
                                tokens.append((rd.RW, tmp_word))
                                continue
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIM3,
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue
                elif line[char_index] == "r":
                    char_index += 1
                    tmp_word += "r"
                    if line[char_index] == "e":
                        char_index += 1
                        tmp_word += "e"
                        if line[char_index] == "e":
                            char_index += 1
                            tmp_word += "e"
                            if line[char_index] in rd.DELIM24:
                                tokens.append((rd.RW, tmp_word))
                                continue
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIM24,
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue
                    elif line[char_index] == "u":
                        char_index += 1
                        tmp_word += "u"
                        if line[char_index] == "e":
                            char_index += 1
                            tmp_word += "e"
                            if line[char_index] in rd.DELIMb:
                                tokens.append((rd.BL, tmp_word))
                                continue
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIMb,
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue
                elif line[char_index] == "u":
                    char_index += 1
                    tmp_word += "u"
                    if line[char_index] == "l":
                        char_index += 1
                        tmp_word += "l"
                        if line[char_index] == "i":
                            char_index += 1
                            tmp_word += "i"
                            if line[char_index] == "p":
                                char_index += 1
                                tmp_word += "p"
                                if line[char_index] in rd.DELIM3:
                                    tokens.append((rd.RW, tmp_word))
                                    continue
                                else:
                                    # Finish whole word if error
                                    errors.append(
                                        error_unknown.delim(
                                            line_number,
                                            char_index,
                                            tmp_word,
                                            line[char_index],
                                            rd.DELIM3,
                                        )
                                    )
                                    char_index = skip(char_index, line)
                                    continue

            # viola delim4
            elif line[char_index] == "v":
                char_index += 1
                tmp_word = "v"
                if line[char_index] == "i":
                    char_index += 1
                    tmp_word += "i"
                    if line[char_index] == "o":
                        char_index += 1
                        tmp_word += "o"
                        if line[char_index] == "l":
                            char_index += 1
                            tmp_word += "l"
                            if line[char_index] == "a":
                                char_index += 1
                                tmp_word += "a"
                                if line[char_index] in rd.DELIM4:
                                    tokens.append((rd.RW, tmp_word))
                                    continue
                                else:
                                    # Finish whole word if error
                                    errors.append(
                                        error_unknown.delim(
                                            line_number,
                                            char_index,
                                            tmp_word,
                                            line[char_index],
                                            rd.DELIM4,
                                        )
                                    )
                                    char_index = skip(char_index, line)
                                    continue

            # willow delim3
            elif line[char_index] == "w":
                char_index += 1
                tmp_word = "w"
                if line[char_index] == "i":
                    char_index += 1
                    tmp_word += "i"
                    if line[char_index] == "l":
                        char_index += 1
                        tmp_word += "l"
                        if line[char_index] == "l":
                            char_index += 1
                            tmp_word += "l"
                            if line[char_index] == "o":
                                char_index += 1
                                tmp_word += "o"
                                if line[char_index] == "w":
                                    char_index += 1
                                    tmp_word += "w"
                                    if line[char_index] in rd.DELIM3:
                                        tokens.append((rd.RW, tmp_word))
                                        continue
                                    else:
                                        # Finish whole word if error
                                        errors.append(
                                            error_unknown.delim(
                                                line_number,
                                                char_index,
                                                tmp_word,
                                                line[char_index],
                                                rd.DELIM3,
                                            )
                                        )
                                        char_index = skip(char_index, line)
                                        continue

            # ---------------------- Reserved Symbol ---------------------- #

            # + delim5, += delim19
            elif line[char_index] == "+":
                char_index += 1
                tmp_word = "+"
                if line[char_index] in rd.DELIM5:
                    tokens.append((rd.RS, tmp_word))
                    continue
                elif line[char_index] == "=":
                    char_index += 1
                    tmp_word += "="
                    if line[char_index] in rd.DELIM19:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM19,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM5,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # - delim19, -= DELIM19
            elif line[char_index] == "-":
                char_index += 1
                tmp_word = "-"
                if line[char_index] in rd.DELIM19:
                    tokens.append((rd.RS, tmp_word))
                    continue
                elif line[char_index] == "=":
                    char_index += 1
                    tmp_word += "="
                    if line[char_index] in rd.DELIM19:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM19,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM19,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # * delim13, *# delim25, ** delim13, **= delim13, **# delim26, *= delim 13
            elif line[char_index] == "*":
                char_index += 1
                tmp_word = "*"
                if line[char_index] in rd.DELIM13:
                    tokens.append((rd.RS, tmp_word))
                    continue
                elif line[char_index] == "#":
                    char_index += 1
                    tmp_word += "#"

                    if line[char_index] in rd.DELIMID:
                        tokens.append((rd.RS, tmp_word))
                        tmp_word = ""
                        tmp_word += line[char_index]
                        char_index += 1

                        for x in range(50):
                            if line[char_index] == "\n":
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIMID,
                                    )
                                )
                                char_index += skip(char_index, line)
                                break

                            if line[char_index] in rd.DELIMID:
                                tmp_word += line[char_index]
                                char_index += 1

                            if line[char_index] in rd.DELIM25:
                                break

                        if line[char_index] in rd.DELIM25:
                            tokens.append((rd.ID, tmp_word))
                            continue
                        else:
                            # Finish whole word if error
                            errors.append(
                                error_unknown.delim(
                                    line_number,
                                    char_index,
                                    tmp_word,
                                    line[char_index],
                                    rd.DELIM25,
                                )
                            )
                            char_index = skip(char_index, line)
                            continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIMID,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                elif line[char_index] == "*":
                    char_index += 1
                    tmp_word += "*"
                    if line[char_index] in rd.DELIM13:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    elif line[char_index] == "=":
                        char_index += 1
                        tmp_word += "="
                        if line[char_index] in rd.DELIM13:
                            tokens.append((rd.RS, tmp_word))
                            continue
                        else:
                            # Finish whole word if error
                            errors.append(
                                error_unknown.delim(
                                    line_number,
                                    char_index,
                                    tmp_word,
                                    line[char_index],
                                    rd.DELIM13,
                                )
                            )
                            char_index = skip(char_index, line)
                            continue
                    elif line[char_index] == "#":
                        char_index += 1
                        tmp_word += "#"
                        if line[char_index] in rd.DELIMID:
                            tokens.append((rd.RS, tmp_word))
                            tmp_word = ""
                            tmp_word += line[char_index]
                            char_index += 1

                            for x in range(50):
                                if line[char_index] == "\n":
                                    errors.append(
                                        error_unknown.delim(
                                            line_number,
                                            char_index,
                                            tmp_word,
                                            line[char_index],
                                            rd.DELIMi,
                                        )
                                    )
                                    char_index += skip(char_index, line)
                                    break

                                if line[char_index] in rd.DELIMID:
                                    tmp_word += line[char_index]
                                    char_index += 1

                                if line[char_index] in rd.DELIM26:
                                    break

                            if line[char_index] in rd.DELIM26:
                                tokens.append((rd.ID, tmp_word))
                                continue
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        line_number,
                                        char_index,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIM25,
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue
                        else:
                            # Finish whole word if error
                            errors.append(
                                error_unknown.delim(
                                    line_number,
                                    char_index,
                                    tmp_word,
                                    line[char_index],
                                    rd.DELIMID,
                                )
                            )
                            char_index = skip(char_index, line)
                            continue
                elif line[char_index] == "=":
                    char_index += 1
                    tmp_word += "="
                    if line[char_index] in rd.DELIM13:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM13,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM13,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # / delim13, // delim13, //= delim13, /= delim13
            elif line[char_index] == "/":
                char_index += 1
                tmp_word = "/"
                if line[char_index] in rd.DELIM13:
                    tokens.append((rd.RS, tmp_word))
                    continue
                elif line[char_index] == "/":
                    char_index += 1
                    tmp_word += "/"
                    if line[char_index] in rd.DELIM13:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    elif line[char_index] == "=":
                        char_index += 1
                        tmp_word += "="
                        if line[char_index] in rd.DELIM13:
                            tokens.append((rd.RS, tmp_word))
                            continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM13,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                elif line[char_index] == "=":
                    char_index += 1
                    tmp_word += "="
                    if line[char_index] in rd.DELIM13:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM13,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM13,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # % delim13, %= delim13
            elif line[char_index] == "%":
                char_index += 1
                tmp_word = "%"
                if line[char_index] in rd.DELIM13:
                    tokens.append((rd.RS, tmp_word))
                    continue
                elif line[char_index] == "=":
                    char_index += 1
                    tmp_word += "="
                    if line[char_index] in rd.DELIM13:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM13,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM13,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # != delim5
            elif line[char_index] == "!":
                char_index += 1
                tmp_word = "!"
                if line[char_index] == "=":
                    char_index += 1
                    tmp_word += "="
                    if line[char_index] in rd.DELIM5:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM5,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM5,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # > delim22, >= delim 13
            elif line[char_index] == ">":
                char_index += 1
                tmp_word = ">"
                if line[char_index] == "=":
                    char_index += 1
                    tmp_word += "="
                    if line[char_index] in rd.DELIM13:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM13,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                elif line[char_index] in rd.DELIM22:
                    tokens.append((rd.RS, tmp_word))
                    continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM22,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # < delim22, <= delim22, <-- delim14
            elif line[char_index] == "<":
                char_index += 1
                tmp_word = "<"
                if line[char_index] == "=":
                    char_index += 1
                    tmp_word += "="
                    if line[char_index] in rd.DELIM22:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM22,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                elif line[char_index] == "-":
                    char_index += 1
                    tmp_word += "-"
                    if line[char_index] == "-":
                        char_index += 1
                        tmp_word += "-"
                        if line[char_index] in rd.DELIM14:
                            is_comment = True
                            tokens.append((rd.RS, tmp_word))
                            continue
                        else:
                            # Finish whole word if error
                            errors.append(
                                error_unknown.delim(
                                    line_number,
                                    char_index,
                                    tmp_word,
                                    line[char_index],
                                    rd.DELIM14,
                                )
                            )
                            char_index = skip(char_index, line)
                            continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM14,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                elif line[char_index] in rd.DELIM22:
                    tokens.append((rd.RS, tmp_word))
                    continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM22,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # ( delim6
            elif line[char_index] == "(":
                char_index += 1
                tmp_word = "("
                if line[char_index] in rd.DELIM6:
                    tokens.append((rd.RS, tmp_word))
                    continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM6,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # [ delim6
            elif line[char_index] == "[":
                char_index += 1
                tmp_word = "["
                if line[char_index] in rd.DELIM6:
                    tokens.append((rd.RS, tmp_word))
                    continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM6,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # { delim23
            elif line[char_index] == "{":
                char_index += 1
                tmp_word = "{"
                if line[char_index] in rd.DELIM23:
                    tokens.append((rd.RS, tmp_word))
                    continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM23,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # ] delim12
            elif line[char_index] == "]":
                char_index += 1
                tmp_word = "]"
                if line[char_index] in rd.DELIM12:
                    tokens.append((rd.RS, tmp_word))
                    continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM12,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # } delim18
            elif line[char_index] == "}":
                char_index += 1
                tmp_word = "}"
                if line[char_index] in rd.DELIM18:
                    tokens.append((rd.RS, tmp_word))
                    continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM18,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # ) delim17
            elif line[char_index] == ")":
                char_index += 1
                tmp_word = ")"
                if line[char_index] in rd.DELIM17:
                    tokens.append((rd.RS, tmp_word))
                    continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM17,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # , delim7
            elif line[char_index] == ",":
                char_index += 1
                tmp_word = ","
                if line[char_index] in rd.DELIM7:
                    tokens.append((rd.RS, tmp_word))
                    continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM7,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # : delim15
            elif line[char_index] == ":":
                char_index += 1
                tmp_word = ":"
                if line[char_index] in rd.DELIM15:
                    tokens.append((rd.RS, tmp_word))
                    continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM15,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # . delim28
            elif line[char_index] == ".":
                char_index += 1
                tmp_word = "."
                if line[char_index] in rd.DELIM28:
                    tokens.append((rd.RS, tmp_word))
                    continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM28,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # _ delim21
            elif line[char_index] == "_":
                char_index += 1
                tmp_word = "_"
                if line[char_index] in rd.DELIM21:
                    tokens.append((rd.RS, tmp_word))
                    continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM21,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # ; delim16
            elif line[char_index] == ";":
                char_index += 1
                tmp_word = ";"
                if line[char_index] in rd.DELIM16:
                    tokens.append((rd.RS, tmp_word))
                    continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM16,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # # delim20
            elif line[char_index] == "#":
                char_index += 1
                tmp_word = "#"
                if line[char_index] in rd.DELIM20:
                    tokens.append((rd.RS, tmp_word))
                    tmp_word = ""
                    tmp_word += line[char_index]
                    char_index += 1

                    for x in range(50):
                        if line[char_index] == "\n":
                            errors.append(
                                error_unknown.delim(
                                    line_number,
                                    char_index,
                                    tmp_word,
                                    line[char_index],
                                    rd.DELIMID,
                                )
                            )
                            char_index += skip(char_index, line)
                            break

                        if line[char_index] in rd.DELIMID:
                            tmp_word += line[char_index]
                            char_index += 1
                        else:
                            break

                    if line[char_index] in rd.DELIMi:
                        tokens.append((rd.ID, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIMi,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM20,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # ? delim20
            elif line[char_index] == "?":
                char_index += 1
                tmp_word = "?"
                if line[char_index] in rd.DELIM20:
                    tokens.append((rd.RS, tmp_word))
                    break
                else:
                    # Finish whole word if error
                    errors.append(
                        error_unknown.delim(
                            line_number,
                            char_index,
                            tmp_word,
                            line[char_index],
                            rd.DELIM20,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue

            # = delim8, == delim8, =! delim8, =& delim8, =/ delim8, =- delim21
            elif line[char_index] == "=":
                char_index += 1
                tmp_word = "="
                if line[char_index] in rd.DELIM8:
                    tokens.append((rd.RS, tmp_word))
                    continue
                elif line[char_index] == "=":
                    char_index += 1
                    tmp_word += "="
                    if line[char_index] in rd.DELIM8:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM8,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                elif line[char_index] == "!":
                    char_index += 1
                    tmp_word += "!"
                    if line[char_index] in rd.DELIM8:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM8,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                elif line[char_index] == "&":
                    char_index += 1
                    tmp_word += "&"
                    if line[char_index] in rd.DELIM8:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM8,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                elif line[char_index] == "/":
                    char_index += 1
                    tmp_word += "/"
                    if line[char_index] in rd.DELIM8:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM8,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                elif line[char_index] == "-":
                    char_index += 1
                    tmp_word += "-"
                    if line[char_index] in rd.DELIM21:
                        tokens.append((rd.RS, tmp_word))
                        continue
                    else:
                        # Finish whole word if error
                        errors.append(
                            error_unknown.delim(
                                line_number,
                                char_index,
                                tmp_word,
                                line[char_index],
                                rd.DELIM21,
                            )
                        )
                        char_index = skip(char_index, line)
                        continue

            # ---------------------- Literals ---------------------- #

            # Tint
            elif line[char_index].isdigit():
                tmp_word = ""
                for x in range(6):
                    if line[char_index].isdigit():
                        tmp_word += line[char_index]
                        char_index += 1

                    if x == 5:
                        if line[char_index].isdigit():
                            tmp_word += line[char_index]
                            errors.append(
                                error_invalid_range.tint(
                                    char_index, line_number, tmp_word
                                )
                            )
                            char_index = skip(char_index, line)
                            continue
                        elif line[char_index] in rd.DELIMtf:
                            tokens.append((rd.TINT_LIT, tmp_word))
                            continue
                        elif line[char_index] == ".":
                            tmp_word += line[char_index]
                            char_index += 1
                            break

                    continue

                if line[char_index - 1] == ".":
                    # Flora
                    for x in range(7):
                        if line[char_index].isdigit():
                            tmp_word += line[char_index]
                            char_index += 1
                        if x == 5:
                            if line[char_index].isdigit():
                                tmp_word += line[char_index]
                                errors.append(
                                    error_invalid_range.flora(
                                        char_index, line_number, tmp_word
                                    )
                                )
                                char_index = skip(char_index, line)
                                continue
                            elif line[char_index] in rd.DELIMtf:
                                tokens.append((rd.FLORA_LIT, tmp_word))
                                continue

                if line[char_index] not in rd.DELIMtf:
                    errors.append(
                        error_unknown.id(
                            char_index,
                            line_number,
                            tmp_word,
                            line[char_index],
                            rd.DELIMtf,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue
                continue

            # String
            elif line[char_index] == '"':
                tmp_word = line[char_index]
                char_index += 1
                if line[char_index] in rd.ASCII:
                    while True:
                        if line[char_index] == "\n":
                            errors.append(
                                error_unknown.delim(
                                    char_index,
                                    line_number,
                                    tmp_word,
                                    line[char_index],
                                    ['"'],
                                )
                            )
                            char_index = skip(char_index, line)
                            break

                        tmp_word += line[char_index]
                        char_index += 1

                        if line[char_index - 1] == "\\":
                            tmp_esc = "\\"
                            if line[char_index] == "n":
                                tmp_esc = "n"
                                char_index += 1
                                tokens.append((rd.STR_LIT, tmp_esc))
                            elif line[char_index] == "\\":
                                tmp_esc = "\\"
                                char_index += 1
                                tokens.append((rd.STR_LIT, tmp_esc))
                            elif line[char_index] == '"':
                                tmp_esc = '"'
                                char_index += 1
                                tokens.append((rd.STR_LIT, tmp_esc))
                            elif line[char_index] == "t":
                                tmp_esc = "t"
                                char_index += 1
                                tokens.append((rd.STR_LIT, tmp_esc))
                            elif line[char_index] == "'":
                                tmp_esc = "\\'"
                                char_index += 1
                                tokens.append((rd.STR_LIT, tmp_esc))

                        if line[char_index] == '"':
                            tmp_word += line[char_index]
                            char_index += 1
                            if line[char_index] in rd.DELIMtf:
                                tokens.append((rd.STR_LIT, tmp_word))
                                break
                            else:
                                # Finish whole word if error
                                errors.append(
                                    error_unknown.delim(
                                        char_index,
                                        line_number,
                                        tmp_word,
                                        line[char_index],
                                        rd.DELIMtf,
                                    )
                                )
                                char_index = skip(char_index, line)
                                break
                    continue

            elif line[char_index] == "'":
                tmp_word += line[char_index]
                char_index += 1
                if line[char_index].isascii():
                    if line[char_index] == "\n":
                        errors.append(
                            error_unknown.delim(
                                char_index,
                                line_number,
                                tmp_word,
                                line[char_index],
                                ['"'],
                            )
                        )
                        char_index = skip(char_index, line)
                        continue
                    if line[char_index].isascii():
                        tmp_word += line[char_index]
                        char_index += 1
                    if line[char_index] == "'":
                        tmp_word += line[char_index]
                        char_index += 1
                        if line[char_index] in rd.DELIMtf:
                            tokens.append((rd.CHR_LIT, tmp_word))
                            continue
                        else:
                            # Finish whole word if error
                            errors.append(
                                error_unknown.delim(
                                    char_index,
                                    line_number,
                                    tmp_word,
                                    line[char_index],
                                    rd.DELIMtf,
                                )
                            )
                            char_index = skip(char_index, line)
                            continue
                    else:
                        errors.append(
                            error_unknown.delim(
                                char_index,
                                line_number,
                                tmp_word,
                                line[char_index],
                                ["'"],
                            )
                        )
                        char_index = skip(char_index, line)
                        continue

                if line[char_index] not in rd.DELIMtf:
                    errors.append(
                        error_unknown.delim(
                            char_index,
                            line_number,
                            tmp_word,
                            line[char_index],
                            rd.DELIMtf,
                        )
                    )
                    char_index = skip(char_index, line)
                    continue
                continue

            # ----------  The letter is none existent ---------- #
            char_index, tmp_word = skip_word(char_index, line, tmp_word)
            errors.append(error_unknown.id(line_number, char_index, tmp_word))

    return tokens, errors
