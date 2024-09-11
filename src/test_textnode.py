import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node,
    split_nodes_delimiter
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node2", text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_italic, "https://www.boot.dev")
        node2 = TextNode(
            "This is a text node", text_type_italic, "https://www.boot.dev"
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", text_type_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", text_type_image, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", text_type_bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(new_nodes, 
			[
				TextNode("This is text with a ", text_type_text),
				TextNode("code block", text_type_code),
				TextNode(" word", text_type_text),
			]
        )

    def test_multiple_nodes(self):
        nodes = [
            TextNode("This is text with a `code block` word, this is another `code block` word", text_type_text),
            TextNode("`This is text with a code block word`", text_type_text),
            TextNode("This is text with a `code block` word too", text_type_text),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", text_type_code)
        self.assertEqual(new_nodes, 
			[
				TextNode("This is text with a ", text_type_text),
				TextNode("code block", text_type_code),
				TextNode(" word, this is another ", text_type_text),
				TextNode("code block", text_type_code),
				TextNode(" word", text_type_text),
				TextNode("This is text with a code block word", text_type_code),
				TextNode("This is text with a ", text_type_text),
				TextNode("code block", text_type_code),
				TextNode(" word too", text_type_text),
			]
        )

    
    def test_bold(self):
        node = TextNode("This is text with a **bold block** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(new_nodes, 
			[
				TextNode("This is text with a ", text_type_text),
				TextNode("bold block", text_type_bold),
				TextNode(" word", text_type_text),
			]
        )

    def test_italic(self):
        node = TextNode("This is text with a *italic block* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(new_nodes, 
			[
				TextNode("This is text with a ", text_type_text),
				TextNode("italic block", text_type_italic),
				TextNode(" word", text_type_text),
			]
        )

if __name__ == "__main__":
    unittest.main()

