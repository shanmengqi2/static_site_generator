from src.textnode import TextNode, TextType

def main():
    node = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.boot.dev")
    print(node)
    print(f"Text: {node.text}")
    print(f"Type: {node.text_type}")
    print(f"URL: {node.url}")

    node2 = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.boot.dev")
    print(f"Equality: {node == node2}")

    node3 = TextNode("Different", TextType.ITALIC_TEXT)
    print(f"Inequality: {node == node3}")
    print(f"URL Default: {node3.url}")

if __name__ == "__main__":
    main()
