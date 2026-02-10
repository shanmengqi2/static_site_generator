import markdown_extract
from textnode import TextNode, TextType

def text_to_textnodes(text):
  text_node = TextNode(text, TextType.PLAIN)
  nodes = markdown_extract.split_nodes_delimiter([text_node],"**", TextType.BOLD)
  nodes = markdown_extract.split_nodes_delimiter(nodes, "`", TextType.CODE)
  nodes = markdown_extract.split_nodes_delimiter(nodes, "_", TextType.ITALIC)
  nodes = markdown_extract.split_nodes_image(nodes)
  nodes = markdown_extract.split_nodes_link(nodes)

  return nodes