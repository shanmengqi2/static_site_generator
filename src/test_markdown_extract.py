import unittest
from markdown_extract import extract_markdown_images, extract_markdown_links

class TestMarkdownExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
            ],
            matches,
        )

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
            matches,
        )

    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_ignore_images(self):
        # This test ensures that image syntax ![]() is not caught by the link extractor
        text = "This is text with an ![image](https://example.com/img.png) and a [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("link", "https://example.com"),
            ],
            matches,
        )

    def test_extract_markdown_empty_values(self):
        text = "![]() and []()"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertListEqual([("", "")], images)
        self.assertListEqual([("", "")], links)

def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )