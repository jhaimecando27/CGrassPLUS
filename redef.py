# Regular Definitions:
zero = "0"
dig = [chr(i) for i in range(49, 58)]
let = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]
num = dig + [zero]
newline = ["\n"]
diglet = dig + let
id = let + num + ["_", "-"]
ht = ["#"]
space = [" "]
ascii = [chr(i) for i in range(128)]


# Delimiters
delimi = space + ["=", ";", ")", "(", ","]
delimtf = newline + space + ["+", "-", "*", "/", "%",
                             ";", ")", "]", "}", "<", ">", "!", "=", ",", ":"]
delims = ["\"",]
delimc = ["'"]
delimb = space + ["=", "<", ">", "!", ";", "]", ")"]
delim1 = [";", " "]
delim2 = ["\n", ' ']
delim3 = [' ', "("]
delim4 = [" "]
delim5 = num + space + ht + ["(", "["]
delim6 = let + num + space + newline + ht + \
    ["(", "[", "{", "\"", "\'", ")", "]"]
delim7 = newline + dig + space + ht + ["\"", "\'", "(", "[", "{"]
delim8 = let + num + ht + space + ["\"", "["]
delim9 = space + newline
delim10 = [";", ' ',  "\n", ","]
delim11 = [";", "+", " ", ",", ")", "}", "]"]
delim12 = space + ["=", ";", ")", "}", ","]
delim13 = dig + space + ["("]
delim14 = ascii
delim15 = space + dig + let + newline + ["\"", ")", "]"]
delim16 = let + ht + ["\n", " ", ")"]
delim17 = newline + space + ["=", "-", "/", "*", "+", "]",
                             ")", "}", ",", ";", "\'", "(", "."]
delim18 = [";", ",", "]", "),", "}", "."]
delim19 = num + space + ht + ["("]
delim20 = let
delim21 = space + [":", "("]
delim22 = num + [" ", "(", "#"]
delim23 = space + newline + ["\"", "}", "("] + dig
delim24 = space + ["("]
delim25 = newline + space + [")", ","]
delim26 = newline + space + [")"]
delim27 = space + num + ht + [",", "_", "[", ")", ":"]
delim28 = let + ht
