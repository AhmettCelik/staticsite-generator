import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_basic(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        expected_output = '' 
        self.assertEqual(node.props_to_html(), expected_output)


    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        expected_output = '' 
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_characters(self):
        props = {
            "aria-label": 'My "special" button',
            "data-value": "5 > 3",
        }
        node = HTMLNode(props=props)
        expected_output = ' aria-label="My "special" button" data-value="5 > 3"' 
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_order_independence(self):
        props1 = {
            "class": "button",
            "id": "submit-btn"
        }
        props2 = {
            "id": "submit-btn",
            "class": "button"
        }
        node1 = HTMLNode(props=props1)
        node2 = HTMLNode(props=props2)
        self.assertEqual(node1.props_to_html(), node2.props_to_html())

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )

        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, None, {'class': 'primary'})",
        )

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_valid_data(self):
        node = LeafNode("p", "Hello World", {"class": "text"})
        self.assertEqual(node.to_html(), '<p class="text">Hello World</p>')

    def test_to_html_with_empty_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", "").to_html()

        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_to_html_with_empty_tag(self):
        node = LeafNode(None, "Hello World")
        self.assertEqual(node.to_html(), "Hello World")

    def test_to_html_with_empty_props(self):
        node = LeafNode("p", "Hello World")
        self.assertEqual(node.to_html(), '<p>Hello World</p>')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_valid_data(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_parent_data(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = ParentNode(
            "a",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                node,
            ],
        )
     
        self.assertEqual(node2.to_html(), "<a><b>Bold text</b>Normal text<i>italic text</i><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></a>")

    def test_to_html_with_no_data(self):
        with self.assertRaises(ValueError):
            ParentNode(None, LeafNode("p", "Normal text")).to_html()

        with self.assertRaises(ValueError):
            ParentNode("p", None).to_html()

if __name__ == "__main__":
    unittest.main()
