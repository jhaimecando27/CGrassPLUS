symbol_table: dict = {}


class ParseTreeNode:
    def __init__(self, symbol: str, level=0, con_level=0, itr_level=0):
        self.symbol = symbol
        self.level = level
        self.children = []
        self.con_level = con_level
        self.itr_level = itr_level

        self.kind = None
        self.type = None
        self.properties = {}
        self.line_number = None

    def add_child(self, child):
        child.level = self.level
        if self.symbol in [
            "garden",
            "<statement>",
            "<function>",
            "tree",
        ] and self.symbol in [
            "garden",
            "<statement>",
            "<function>",
            "<body>",
            "tree",
        ]:
            child.level += 1
        child.con_level = self.con_level
        child.itr_level = self.itr_level

        if child.symbol in ["leaf", "eleaf", "moss"]:
            child.con_level += 1

        if child.symbol in ["fern", "willow"]:
            child.itr_level += 1

        self.children.append(child)

    def set_kind(self, kind):
        self.kind = kind

    def set_type(self, type_):
        self.type = type_

    def set_properties(self, properties):
        self.properties.update(properties)

    def set_line_number(self, line_number):
        self.line_number = line_number

    def set_data(self, data):
        self.data = data

    def __str__(self):
        output: str = ""
        output += "" if self.con_level == 0 else f" (Con Level: {self.con_level})"
        output += "" if self.itr_level == 0 else f" (Itr Level: {self.itr_level})"
        output += "" if self.kind is None else f" (kind: {self.kind})"
        output += "" if self.type is None else f" (type: {self.type})"
        output += f" (level: {self.level})"
        output += (
            "" if self.line_number is None else f" (line number: {self.line_number})"
        )
        output += (
            "" if len(self.properties) == 0 else f" (properties: {self.properties})"
        )
        if output != "":
            output = "-" + output
        return f"{self.symbol} {output}"


parse_tree_root = ParseTreeNode("<program>")


def add_parse_tree_node(parent, symbol):
    """
    Add a new node to the parse tree.
    :param parent: The parent node.
    :param symbol: The symbol of the new node.
    :return: The new node.
    """
    if symbol == "<newline>":
        return
    new_node = ParseTreeNode(symbol)
    parent.add_child(new_node)
    return new_node


def print_parse_tree(node=parse_tree_root, level=0):
    print("  " * level + "- " + str(node))
    for child in node.children:
        print_parse_tree(child, level + 1)


# del all parse_tree_root children
def delete_parse_tree(node=parse_tree_root):
    """
    Delete the parse tree.
    """
    node.children = []
    for child in node.children:
        delete_parse_tree(child)
