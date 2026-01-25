import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node5 = TextNode("Oh, what a url!", TextType.IMAGE)
        node6 = TextNode("Oh, what a url!", TextType.IMAGE, None)
        self.assertEqual(node5, node6)
    def test_not_eq(self):
        node3 = TextNode("Oh, what a url!", TextType.LINK, "https://tux2gaming.com")
        node4 = TextNode("Oh, what a url!", TextType.IMAGE, "https://tux2gaming.com")
        self.assertNotEqual(node3, node4)
        node5 = TextNode("Oh, what a url!", TextType.IMAGE)
        self.assertNotEqual(node4, node5)
        node7 = TextNode("Oh, wut a url!", TextType.LINK, "https://tux2gaming.com")
        self.assertNotEqual(node3, node7)


if __name__ == "__main__":
    unittest.main()