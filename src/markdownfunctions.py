from textnode import *
import re

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