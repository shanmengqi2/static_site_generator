import unittest
from textnode import TextNode, TextType
from markdown_extract import split_nodes_image, split_nodes_link

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_image_basic(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/img.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://example.com/img.png")

    def test_split_nodes_image_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/img.png) and another ![second](https://example.com/img2.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].url, "https://example.com/img.png")
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[3].text, "second")
        self.assertEqual(new_nodes[3].url, "https://example.com/img2.png")

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is text with no images", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with no images")

    def test_split_nodes_link_basic(self):
        node = TextNode(
            "This is text with a [link](https://example.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://example.com")

    def test_split_nodes_link_multiple(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second](https://example.com/2)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].url, "https://example.com")
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[3].text, "second")
        self.assertEqual(new_nodes[3].url, "https://example.com/2")

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is text with no links", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with no links")
