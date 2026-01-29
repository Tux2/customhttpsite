from textnode import *
import re
from enum import Enum
from htmlfunctions import *
from parentnode import ParentNode

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        subtext = old_node.text
        while delimiter in subtext:
            split_1 = subtext.split(delimiter, maxsplit=1)
            if delimiter not in split_1[len(split_1) - 1]:
                raise Exception("No closing tag found!")
            split_2 = split_1[len(split_1) - 1].split(delimiter, maxsplit=1)
            if len(split_1) > 1 and split_1[0] != "":
                plain_txt = TextNode(split_1[0], TextType.PLAIN)
                new_nodes.append(plain_txt)
            other_node = TextNode(split_2[0], text_type)
            new_nodes.append(other_node)
            if len(split_2) > 1:
                subtext = split_2[1]
            else:
                subtext = ""
        if subtext != "":
            plain_txt = TextNode(subtext, TextType.PLAIN)
            new_nodes.append(plain_txt)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]+)\]\((http[s]?:\/\/[a-zA-Z0-9\.\/]+)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\]]+)\]\((http[s]?:\/\/[a-zA-Z0-9\.\/]+)\)",  text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        subtext = old_node.text
        images = extract_markdown_images(old_node.text)
        for image in images:
            split_1 = subtext.split(f"![{image[0]}]({image[1]})", maxsplit=1)
            if split_1[0] != "":
                plain_txt = TextNode(split_1[0], TextType.PLAIN)
                new_nodes.append(plain_txt)
            link_txt = TextNode(image[0], TextType.IMAGE, image[1])
            new_nodes.append(link_txt)
            if len(split_1) > 1:
                subtext = split_1[len(split_1) - 1]
            else:
                subtext = ""
        if subtext != "":
            plain_txt = TextNode(subtext, TextType.PLAIN)
            new_nodes.append(plain_txt)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        subtext = old_node.text
        images = extract_markdown_links(old_node.text)
        for image in images:
            split_1 = subtext.split(f"[{image[0]}]({image[1]})", maxsplit=1)
            if split_1[0] != "":
                plain_txt = TextNode(split_1[0], TextType.PLAIN)
                new_nodes.append(plain_txt)
            link_txt = TextNode(image[0], TextType.LINK, image[1])
            new_nodes.append(link_txt)
            if len(split_1) > 1:
                subtext = split_1[len(split_1) - 1]
            else:
                subtext = ""
        if subtext != "":
            plain_txt = TextNode(subtext, TextType.PLAIN)
            new_nodes.append(plain_txt)
    return new_nodes

def text_to_textnodes(text):
    text_node = TextNode(text, TextType.PLAIN)
    result_nodes = split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([text_node], "**", TextType.BOLD), "_", TextType.ITALIC), "`", TextType.CODE)
    linked_nodes = split_nodes_link(split_nodes_image(result_nodes))
    return linked_nodes

def markdown_to_blocks(text):
    blocks_raw = text.split("\n\n")
    blocks_processed =[]
    for block in blocks_raw:
        temp = block.strip()
        if temp != "":
            blocks_processed.append(temp)
    return blocks_processed

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("\n```"):
        return BlockType.CODE
    elif block.startswith(">"):
        line_split = block.split("\n")
        is_quote = True
        for line in line_split:
            if not block.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE
    elif block.startswith("- "):
        line_split = block.split("\n")
        is_list = True
        for line in line_split:
            if not block.startswith("- "):
                is_list = False
                break
        if is_list:
            return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        line_split = block.split("\n")
        is_list = True
        line_num = 1
        for line in line_split:
            if not line.startswith(f"{line_num}. "):
                is_list = False
                break
            line_num += 1
        if is_list:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(text):
    blocks = markdown_to_blocks(text)
    block_array = []
    for block in blocks:
        type = block_to_block_type(block)
        if type == BlockType.CODE:
            node = TextNode(block[4:-3], TextType.CODE)
            block_array.append(ParentNode("pre", [text_node_to_html_node(node)]))
        elif type == BlockType.HEADING:
            headings = re.findall(r"(^|\n)(#{1,6}) (.+)", block)
            for heading in headings:
                t_nodes = text_to_textnodes(heading[2])
                heading_level = "h1"
                match heading[1]:
                    case "#":
                        heading_level = "h1"
                    case "##":
                        heading_level = "h2"
                    case "###":
                        heading_level = "h3"
                    case "####":
                        heading_level = "h4"
                    case "#####":
                        heading_level = "h5"
                    case "######":
                        heading_level = "h6"
                html_nodes = []
                for text_node in t_nodes:
                    html_nodes.append(text_node_to_html_node(text_node))
                block_array.append(ParentNode(heading_level, html_nodes))
        elif type == BlockType.PARAGRAPH:
            t_nodes = text_to_textnodes(block.replace("\n", " "))
            html_nodes = []
            for text_node in t_nodes:
                html_nodes.append(text_node_to_html_node(text_node))
            block_array.append(ParentNode("p", html_nodes))
        elif type == BlockType.QUOTE:
            lines = block.split("\n")
            quote_nodes = []
            new_lines = []
            for line in lines:
                new_lines.append(line[2::])
            combined_lines = " ".join(new_lines)
            t_nodes = text_to_textnodes(combined_lines)
            for text_node in t_nodes:
                quote_nodes.append(text_node_to_html_node(text_node))
            block_array.append(ParentNode("quote", quote_nodes))
        elif type == BlockType.UNORDERED_LIST:
            list_items = []
            lines = block.split("\n")
            for line in lines:
                t_nodes = text_to_textnodes(line[2::])
                item_nodes = []
                for text_node in t_nodes:
                    item_nodes.append(text_node_to_html_node(text_node))
                list_items.append(ParentNode("li", item_nodes))
            block_array.append(ParentNode("ul", list_items))
        elif type == BlockType.ORDERED_LIST:
            list_items = []
            lines = block.split("\n")
            for line in lines:
                t_nodes = text_to_textnodes(re.findall(r"(\d+\. )(.+)", line)[0][1])
                item_nodes = []
                for text_node in t_nodes:
                    item_nodes.append(text_node_to_html_node(text_node))
                list_items.append(ParentNode("li", item_nodes))
            block_array.append(ParentNode("ol", list_items))
    return ParentNode("div", block_array)



