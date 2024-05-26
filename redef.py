# Regular Definitions:
ZERO = "0"
DIG = [chr(i) for i in range(49, 58)]
LET = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]
NUM = DIG + [ZERO]
NEWLINE = ["\n"]
DIGLET = DIG + LET
DELIMID = LET + NUM + ["_"]
HT = ["#"]
SPC = [" "]
ASCII = [chr(i) for i in range(128)]
ARITH = ["+", "-", "*", "/", "%"]

# Delimiters
DELIMi = (
    ARITH
    + SPC
    + [
        "=",
        ";",
        ")",
        "(",
        ",",
        "[",
        "]",
        ".",
        "=",
        "<",
        ">",
    ]
)
DELIMtf = (
    NEWLINE
    + SPC
    + ["+", "-", "*", "/", "%", ";", ")", "]", "}", "<", ">", "!", "=", ",", ":"]
)
DELIMs = [
    '"',
]
DELIMc = ["'"]
DELIMb = SPC + ["=", "<", ">", "!", ";", "]", ")"]
DELIM1 = [";", " "]
DELIM2 = ["\n", " "]
DELIM3 = [" ", "(", "]", ")", ";"]
DELIM4 = [" "]
DELIM5 = NUM + SPC + HT + ["(", "["]
DELIM6 = LET + NUM + SPC + NEWLINE + HT + ["(", "[", "{", '"', "'", ")", "]", ":", "-"]
DELIM7 = NEWLINE + DIG + SPC + HT + ['"', "'", "(", "[", "{"]
DELIM8 = LET + NUM + HT + SPC + ['"', "[", "{"]
DELIM9 = SPC + NEWLINE
DELIM10 = [";", " ", "\n", ","]
DELIM11 = [";", "+", " ", ",", ")", "}", "]"]
DELIM12 = NEWLINE + SPC + ["=", ";", ")", "}", ",", "]"]
DELIM13 = DIG + SPC + ["(", "#"]
DELIM14 = ASCII
DELIM15 = SPC + DIG + LET + NEWLINE + ['"', ")", "]", "["]
DELIM16 = LET + HT + ["\n", " ", ")"]
DELIM17 = (
    NUM
    + NEWLINE
    + SPC
    + ["=", "-", "/", "*", "+", "]", ")", "}", ",", ";", "'", "(", ".", "%", "#"]
)
DELIM18 = [";", ",", "]", "),", "}", "."]
DELIM19 = NUM + SPC + HT + ["("]
DELIM20 = ASCII
DELIM21 = SPC + [":", "("]
DELIM22 = NUM + [" ", "(", "#"]
DELIM23 = SPC + NEWLINE + ['"', "}", "(", "'"] + DIG
DELIM24 = SPC + ["("]
DELIM25 = NEWLINE + SPC + [")", ","]
DELIM26 = NEWLINE + SPC + [")"]
DELIM27 = SPC + NUM + HT + [",", "_", "[", ")", ":"]
DELIM28 = LET + HT

RW = "Reserved Word"
RS = "Reserved Symbol"
TINT_LIT = "tint literal"
FLORA_LIT = "flora literal"
STR_LIT = "string literal"
CHR_LIT = "chard literal"
ID = "Identifier"
BL_LIT = "bloom literal"

datatypes = ["tint", "flora", "string", "bloom"]
