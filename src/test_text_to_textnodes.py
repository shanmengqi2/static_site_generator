import unittest
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_just_text(self):
        nodes = text_to_textnodes("This is just text")
        self.assertListEqual(
            [
                TextNode("This is just text", TextType.PLAIN),
            ],
            nodes,
        )

    def test_text_to_textnodes_bold(self):
        nodes = text_to_textnodes("**Bold**")
        self.assertListEqual(
            [
                TextNode("Bold", TextType.BOLD),
            ],
            nodes,
        )

    def test_text_to_textnodes_italic(self):
        nodes = text_to_textnodes("_Italic_")
        self.assertListEqual(
            [
                TextNode("Italic", TextType.ITALIC),
            ],
            nodes,
        )

    def test_text_to_textnodes_code(self):
        nodes = text_to_textnodes("`Code`")
        self.assertListEqual(
            [
                TextNode("Code", TextType.CODE),
            ],
            nodes,
        )

    def test_text_to_textnodes_image(self):
        nodes = text_to_textnodes("![image](https://example.com/image.png)")
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            ],
            nodes,
        )

    def test_text_to_textnodes_link(self):
        nodes = text_to_textnodes("[link](https://example.com)")
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            nodes,
        )

    def test_text_to_textnodes_incomplete_bold(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This is **bold with no closing")


if __name__ == "__main__":
    unittest.main()
