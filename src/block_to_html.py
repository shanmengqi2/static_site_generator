from leafnode import LeafNode
from textnode_to_htmlnode import text_node_to_html_node
from markdown_to_blocks import BlockType, markdown_to_blocks, block_to_block_type
from parentnode import ParentNode
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType


def markdown_to_html_node(markdown):
    # split md to blocks
    blocks = markdown_to_blocks(markdown)
    html_node_list = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.CODE:
            code_text_node = TextNode(block[4:-3], TextType.CODE)
            code_html_node = text_node_to_html_node(code_text_node)
            pre_code_html = LeafNode("pre", code_html_node.to_html())
            html_node_list.append(pre_code_html)
            continue

        tag = block_type.value
        strip_text = block

        if block_type == BlockType.HEADING:
            tag, strip_text = count_hash_return_htag(block)
        if block_type == BlockType.QUOTE:
            strip_text = md_quote_text(block)
        if block_type == BlockType.U_LIST or block_type == BlockType.O_LIST:
            strip_text = md_list_text(block)
        if block_type == BlockType.PARAGRAPH:
            strip_text = block.replace("\n", " ")

        children_nodes = text_to_children(strip_text)  # you wen ti
        htmlnode = ParentNode(tag, children_nodes)
        # htmlnode.children = children_nodes
        html_node_list.append(htmlnode)

    div_node = ParentNode("div", html_node_list)
    # div_node.children = html_node_list
    return div_node


def count_hash_return_htag(text):
    level = text.count('#', 0, text.find(' '))
    text = text[level + 1:]
    return f"h{level}", text


def md_quote_text(md_quote: str) -> str:
    """
    md_quote: one or multiple lines of valid markdown quote text
    returns: quote content with leading '>' (and optional space) removed
    """
    lines = md_quote.splitlines()
    return "\n".join(
        line[1:].lstrip() if line.startswith(">") else line
        for line in lines
    )


def md_list_text(md: str) -> str:
    lines = md.splitlines()
    ulist_text = ""
    for line in lines:
        line = f"<li>{line[2:].strip()}</li>\n"
        ulist_text += line
    return ulist_text


def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes
