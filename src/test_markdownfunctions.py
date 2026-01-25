import unittest

from textnode import TextNode, TextType
from markdownfunctions import *

class TestMarkdownParse(unittest.TestCase):
    def test_bold(self):
        node1 = TextNode("This is a text node with **some bolded** text", TextType.PLAIN)
        node2 = TextNode("**This is a text node with all bolded text**", TextType.PLAIN)
        result = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertEqual(result[0].text, "This is a text node with ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "some bolded")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.PLAIN)
        self.assertEqual(result[3].text, "This is a text node with all bolded text")
        self.assertEqual(result[3].text_type, TextType.BOLD)
    
    def test_italic(self):
        node1 = TextNode("This is a text node with _some italic_ text", TextType.PLAIN)
        node2 = TextNode("**This is a text node with all bolded text**", TextType.PLAIN)
        result = split_nodes_delimiter([node1, node2], "_", TextType.ITALIC)
        self.assertEqual(result[0].text, "This is a text node with ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "some italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.PLAIN)
        self.assertEqual(result[3].text, "**This is a text node with all bolded text**")
        self.assertEqual(result[3].text_type, TextType.PLAIN)
    
    def test_italic_and_bold(self):
        node1 = TextNode("This is a text node with _some italic_ text", TextType.PLAIN)
        node2 = TextNode("**This is a text node with all bolded text**", TextType.PLAIN)
        result = split_nodes_delimiter(split_nodes_delimiter([node1, node2], "_", TextType.ITALIC), "**", TextType.BOLD)
        self.assertEqual(result[0].text, "This is a text node with ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "some italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.PLAIN)
        self.assertEqual(result[3].text, "This is a text node with all bolded text")
        self.assertEqual(result[3].text_type, TextType.BOLD)
    
    def test_malformed(self):
        node1 = TextNode("This is a text node with **some bolded text", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node1], "**", TextType.BOLD)