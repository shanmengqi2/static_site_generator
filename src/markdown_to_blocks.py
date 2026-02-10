
from enum import Enum
import re


class BlockType(Enum):
  PARAGRAPH = "p"
  HEADING = "h1"
  CODE = "pre"
  QUOTE = "blockquote"
  U_LIST = "ul"
  O_LIST = "ol"

def check_markdown_headings(text):
  regex = r"^#{1,6}\s+\S.*$"
  matches = re.findall(regex, text)
  return matches

def check_markdown_codeblock(text):
  regex = r"^```[\r\n]+[\s\S]*?[\r\n]+```$"
  matches = re.findall(regex, text, re.MULTILINE)
  return matches

def check_markdown_ulist(text):
  regex = r"^(?:-\s.+\r?\n?)+$"
  matches = re.findall(regex, text, re.MULTILINE)
  return matches

def check_markdown_olist(text):
  regex = r"^(?:1\. .+\r?\n)(?:2\. .+\r?\n)*(?:\d+\. .+\r?\n?)$"
  matches = re.findall(regex, text, re.MULTILINE)
  return matches

def check_markdown_quoteblock(text):
  regex = r"^(?:>(?:\s?.*)\r?\n?)+$"
  matches = re.findall(regex, text, re.MULTILINE)
  return matches

def markdown_to_blocks(markdown):
  temp_blocks = markdown.split("\n\n")
  blocks = []
  for block in temp_blocks:
    if block == "":
      continue
    block = block.strip()
    if block != "":
      blocks.append(block)
  return blocks


def block_to_block_type(block):
  if check_markdown_headings(block):
    return BlockType.HEADING
  if check_markdown_codeblock(block):
    return BlockType.CODE
  if check_markdown_quoteblock(block):
    return BlockType.QUOTE
  if check_markdown_ulist(block):
    return BlockType.U_LIST
  if check_markdown_olist(block):
    return BlockType.O_LIST
  
  return BlockType.PARAGRAPH
