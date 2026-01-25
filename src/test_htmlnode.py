import unittest
from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_null(self):
        node1 = HTMLNode()
        str1 = ""
        str2 = node1.props_to_html()
        self.assertEqual(str1, str2)
    
    def test_one_prop(self):
        props = {}
        props["url"] = "https://tux2gaming.com"
        node1 = HTMLNode("", "Just a value", None, props)
        str1 = " url=\"https://tux2gaming.com\""
        str2 = node1.props_to_html()
        self.assertEqual(str1, str2)
    
    def test_two_props(self):
        props = {}
        props["url"] = "https://tux2gaming.com"
        props["alt"] = "Tux2 Gaming"
        node1 = HTMLNode("", "Just a value", None, props)
        str1 = " url=\"https://tux2gaming.com\" alt=\"Tux2 Gaming\""
        str2 = node1.props_to_html()
        self.assertEqual(str1, str2)


if __name__ == "__main__":
    unittest.main()