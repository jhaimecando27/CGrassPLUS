symbol_table: dict = {}


class ParseTreeNode:
    def __init__(self, symbol: str, level=0):
        self.symbol = symbol
        self.level = level
        self.children = []

    def add_child(self, child):
        child.level = self.level + 1
        self.children.append(child)

    def __str__(self):
        return f"{self.symbol} (Level: {self.level})"


parse_tree_root = ParseTreeNode("<program>")


def add_parse_tree_node(parent, symbol):
    if symbol == "<newline>":
        return
    new_node = ParseTreeNode(symbol)
    parent.add_child(new_node)
    return new_node


def print_parse_tree(node=parse_tree_root, level=0):
    print("  " * level + "- " + str(node))
    for child in node.children:
        print_parse_tree(child, level + 1)
