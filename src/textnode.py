from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    tag_map = {
        text_type_text: (None, text_node.text),
        text_type_bold: ("b", text_node.text),
        text_type_italic: ("i", text_node.text),
        text_type_code: ("code", text_node.text),
        text_type_link: ("a", text_node.text, {"href": text_node.url}),
        text_type_image: ("img", "", {"src": text_node.url, "alt": text_node.text}),
    }

    if text_node.text_type in tag_map:
        return LeafNode(*tag_map[text_node.text_type])

    raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    for node in old_nodes:
        if delimiter not in node.text:
            raise Exception("That's invalid Markdown syntax")
    splitted_nodes = list(map(lambda node: node.text.split(delimiter), old_nodes))
    final_list = []
    for node in splitted_nodes:
        text_index = 0
        for text in node:
            if text != "":
                if text_index % 2 == 0:
                    final_list.append(TextNode(text, text_type_text))
                else:
                    final_list.append(TextNode(text, text_type))
            text_index += 1
    return final_list

