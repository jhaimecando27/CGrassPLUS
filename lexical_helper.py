# escape char to string
def convert_esc_char(s):
    if s == "\n":
        return "\\n"
    elif s == "\t":
        return "\\t"
    elif s == " ":
        return "<space>"
    else:
        return s


# skip remaining characters
def skip(i, program):
    AVOID = [" ", "\n"]
    while i < len(program) and program[i] not in AVOID:
        i += 1
    return i


def skip_word(char_index, line, tmp_wrd):
    AVOID = [" ", "\n"]
    while line[char_index] not in AVOID:
        tmp_wrd += line[char_index]
        char_index += 1
    return char_index, tmp_wrd

class Errors:
    class Unknown:
        def delim(
            row_num: int, col_num: int, word: str, wrong_delim: chr, avail_delims: list
        ):
            return (
                "line "
                + str(row_num)
                + ":"
                + str(col_num)
                + ":"
                + '"'
                + word
                + convert_esc_char(wrong_delim)
                + '": Invalid Delimeter "'
                + convert_esc_char(wrong_delim)
                + '". Expecting Delimeter after "'
                + word
                + '": Available '
                + str(avail_delims),
                "UNKNOWN DELIMITER",
            )

        def id(row_num: int, col_num: int, word: str):
            return (
                "line "
                + str(row_num)
                + ":"
                + str(col_num)
                + ": "
                + '"' + word + '"'
                + ' : Expecting "#" symbol before '
                + '"' + word + '"',
                "UNKNOWN IDENTIFIER"
            )

    class InvalidRange:
        def tint(row_num, col_num, word):
            return (
                "line "
                + str(row_num)
                + ":"
                + str(col_num)
                + ":"
                + '"'
                + word
                + '": Invalid range. '
                + "-999999 or 999999",
                "INVALID RANGE",
            )

        def flora(row_num, col_num, word):
            return (
                "line "
                + str(row_num)
                + ":"
                + str(col_num)
                + ":"
                + '"'
                + word
                + '": Invalid range. '
                + "-999999.999999 or 999999.999999",
                "INVALID RANGE",
            )
