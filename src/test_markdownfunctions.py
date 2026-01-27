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
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_with_crazy_description(self):
        matches = extract_markdown_images("This is text with an ![Image, but with some interesting punctionation, that'll knock your socks off!](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("Image, but with some interesting punctionation, that'll knock your socks off!", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_more_markdown_images(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links_with_crazy_description(self):
        matches = extract_markdown_links("This is text with a [Link, but with some interesting punctionation, that'll knock your socks off!](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("Link, but with some interesting punctionation, that'll knock your socks off!", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_more_markdown_links(self):
        matches = extract_markdown_links("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_and_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link(split_nodes_image([node]))
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_combined(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            result,
        )
