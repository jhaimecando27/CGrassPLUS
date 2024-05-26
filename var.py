symbol_table: dict = {}


class ParseTreeNode:
    def __init__(
        self,
        symbol: str,
        level=0,
        leaf_level=0,
        eleaf_level=0,
        fern_level=0,
        willow_level=0,
    ):
        self.symbol = symbol
        self.level = level
        self.children = []
        self.leaf_level = leaf_level
        self.eleaf_level = eleaf_level
        self.fern_level = fern_level
        self.willow_level = willow_level

        self.kind = None
        self.type = None
        self.properties = {}
        self.line_number = None

    def add_child(self, child):
        child.level = self.level
        if child.symbol in ["<statement>", "branch", "tree"] and self.symbol in [
            "tree",
            "branch",
            "garden",
            "<body>",
            "<function>",
            "leaf",
            "eleaf",
            "fern",
            "willow",
        ]:
            child.level += 1

        child.leaf_level = self.leaf_level
        child.eleaf_level = self.eleaf_level
        child.fern_level = self.fern_level
        child.willow_level = self.willow_level

        if child.symbol == "leaf":
            child.leaf_level += 1

        if child.symbol == "eleaf":
            child.leaf_level += 1

        if child.symbol == "fern":
            child.fern_level += 1

        if child.symbol == "willow":
            child.willow_level += 1

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
        output += "" if self.leaf_level == 0 else f" (Leaf Level: {self.leaf_level})"
        output += "" if self.eleaf_level == 0 else f" (Eleaf Level: {self.eleaf_level})"
        output += "" if self.fern_level == 0 else f" (Fern Level: {self.fern_level})"
        output += (
            "" if self.willow_level == 0 else f" (Willow Level: {self.willow_level})"
        )
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
