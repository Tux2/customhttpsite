from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf nodes require a value")
        opening_tag_values = []
        tag = f"<{self.tag}>"
        if self.props != None:
            for key, prop in self.props.items():
                opening_tag_values.append(f" {key}=\"{prop}\"")
            tag = f"<{self.tag}{" ".join(opening_tag_values)}>"
        tag += f"{self.value}</{self.tag}>"
        return tag
    

    def __repr__(self):
        full_string = f"tag=\"{self.tag}\" value=\"{self.value}\" props:{self.props_to_html()}"