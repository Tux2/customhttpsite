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

    def only_links(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
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
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_malformed_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line





- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_block_heading(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_code(self):
        md = """
```
This is a disaster! Utter disaster of code block text
```

```
And yet here we are! ()
# With some code blocks, yes we are!
```
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_block_quote(self):
        md = """
> All's well with the world, but not here

> When you want a duck
>You gotta cook it yourself!

>#Sometimes, there's
>just a lot of fluff
> Ya know?
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_block_unordered_list(self):
        md = """
- Why only have a list with one item? Because!

- When you want a duck
- You gotta cook it yourself!

- #Sometimes, there's
- just a lot of fluff
- Ya know?
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_block_ordered_list(self):
        md = """
1. Why only have a list with one item? Because!

1. When you want a duck
2. You gotta cook it yourself!

1. #Sometimes, there's
2. just a lot of fluff
3. Ya know?
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_block_plain_text(self):
        md = """
#This is a malformed heading

####### Another malformed heading with tooo many #

```
Ooops! Someone forgot to end this code block!

2. Why only have a list with one item? Because! This list is malformed

1. When you want a duck
3. You gotta cook it yourself!

1. #Sometimes, there's
2. just a lot of fluff
4. Ya know?

-Lists need a space between the dash, this one isn't
-Even though it looks like a list
-It isn't a list!

1. This one looks like a List
2. It quacks like a list
3. But in the end
```
"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_unordered_and_ordered_lists(self):
        md = """
1. This is an **ordered** List
2. With several items

- This is an unordered list
- With _several_ items
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an <b>ordered</b> List</li><li>With several items</li></ol><ul><li>This is an unordered list</li><li>With <i>several</i> items</li></ul></div>",
        )
    
    def test_quotes_and_headlines(self):
        md = """
# Heading 1
## Heading 2

> This is a multiline
> quote. _Please_ treat
> accordingly.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><quote>This is a multiline quote. <i>Please</i> treat accordingly.</quote></div>",
        )

    def test_extract_title(self):
        md = """
# Heading 1
## Heading 2

> This is a multiline
> quote. _Please_ treat
> accordingly.
"""

        node = extract_title(md)
        self.assertEqual(
            node,
            "Heading 1",
        )

    def test_extract_title_2(self):
        md = """
## Heading 2
# Heading 1

> This is a multiline
> quote. _Please_ treat
> accordingly.
"""

        node = extract_title(md)
        self.assertEqual(
            node,
            "Heading 1",
        )

    def test_extract_title_3(self):
        md = """
## Heading 2
## Heading 2

# Let Us Do This

> This is a multiline
> quote. _Please_ treat
> accordingly.
"""

        node = extract_title(md)
        self.assertEqual(
            node,
            "Let Us Do This",
        )