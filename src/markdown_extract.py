import re

from textnode import TextNode, TextType

def extract_markdown_images(text):
  regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(regex, text)
  return matches


def extract_markdown_links(text):
  regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(regex,text)
  return matches

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.PLAIN))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.PLAIN:
      new_nodes.append(node)
      continue
    
    image_matches = extract_markdown_images(node.text)
    if not image_matches:
      new_nodes.append(node)
      continue
    
    process_text = node.text
    for match in image_matches:
      split_delimiter = f"![{match[0]}]({match[1]})"
      sections = process_text.split(split_delimiter, 1)
      if len(sections) != 2:
          raise ValueError("Invalid markdown, image section not found")
      
      if sections[0] != "":
          new_nodes.append(TextNode(sections[0], TextType.PLAIN))
      
      new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
      process_text = sections[1]
      
    if process_text != "":
      new_nodes.append(TextNode(process_text, TextType.PLAIN))
      
  return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
      if node.text_type != TextType.PLAIN:
        new_nodes.append(node)
        continue
      
      link_matches = extract_markdown_links(node.text)
      if not link_matches:
        new_nodes.append(node)
        continue

      process_text = node.text
      for match in link_matches:
        split_delimiter = f"[{match[0]}]({match[1]})"
        sections = process_text.split(split_delimiter, 1)
        if len(sections) != 2:
            raise ValueError("Invalid markdown, link section not found")
        
        if sections[0] != "":
            new_nodes.append(TextNode(sections[0], TextType.PLAIN))
            
        new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
        process_text = sections[1]
        
      if process_text != "":
          new_nodes.append(TextNode(process_text, TextType.PLAIN))
          
    return new_nodes
