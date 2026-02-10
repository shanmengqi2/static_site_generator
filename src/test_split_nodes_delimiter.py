import unittest
from textnode import TextNode, TextType
from markdown_extract import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN)

    def test_split_nodes_delimiter_multi(self):
        node = TextNode("This is text with a `code block` word and `another` one", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[3].text, "another")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("This is text with no code block", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with no code block")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)

    def test_split_nodes_delimiter_non_plain(self):
        node = TextNode("This is bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_nodes_delimiter_incomplete(self):
        node = TextNode("This is text with a `code block word", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bold** text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is *italic* text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        
    def test_split_nodes_delimiter_double(self):
        node = TextNode("**bold** and **bold again**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, " and ")
        self.assertEqual(new_nodes[1].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[2].text, "bold again")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)

if __name__ == "__main__":
    unittest.main()
