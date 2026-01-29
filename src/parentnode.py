from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent nodes need a tag")
        if self.children == None:
            raise ValueError(f"{self.tag} Parent nodes need at least one child")
        opening_tag_values = []
        tag = f"<{self.tag}>"
        if self.props != None:
            for key, prop in self.props.items():
                opening_tag_values.append(f" {key}=\"{prop}\"")
            tag = f"<{self.tag}{" ".join(opening_tag_values)}>"
        for child in self.children:
            tag += child.to_html()
        tag += f"</{self.tag}>"
        return tag