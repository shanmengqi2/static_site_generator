from enum import Enum
from pydoc import plain

class TextType(Enum):
  PLAIN = "plain"
  BOLD = "bold"
  ITALIC = "italic"
  CODE = "code"
  LINK = "link"
  IMAGE = "image"

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
        url_part = f", {self.url}" if self.url else ""
        return f"TextNode({self.text}, {self.text_type.value}{url_part})"

