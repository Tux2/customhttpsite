from textnode import *

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