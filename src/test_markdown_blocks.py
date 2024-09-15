import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        blocks = [
            "# This a basic text",
            "## This a basic text             ",
            "   ### This a basic text",
            "#### This a basic text",
            "      ##### This a basic text ",
            "   ###### This a basic text  ",
        ]

        self.assertEqual(block_to_block_type(blocks[0]), "heading")
        self.assertEqual(block_to_block_type(blocks[1]), "heading")
        self.assertEqual(block_to_block_type(blocks[2]), "heading")
        self.assertEqual(block_to_block_type(blocks[3]), "heading")
        self.assertEqual(block_to_block_type(blocks[4]), "heading")
        self.assertEqual(block_to_block_type(blocks[5]), "heading")

    def test_block_to_block_type_code(self):
        block = "     ```private static String = 'Goodbye World!'```    "

        self.assertEqual(block_to_block_type(block), "code")

    def test_block_to_block_type_quote(self):
        block = "         >schools are not real - Tesla   "

        self.assertEqual(block_to_block_type(block), "quote")

    def test_block_to_block_type_ul_list(self):
        block = """
* You
* Need
* To
* Watch
* Those
* Animes
        """

        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_block_to_block_type_ul_list(self):
        block = """
1. Attack on Titan
2. Vinland Saga
3. Naruto
4. Monster
5. and more...
        """

if __name__ == "__main__":
    unittest.main()
