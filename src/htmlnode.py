class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        full_string = ""
        if self.props == None:
            return full_string
        for key,prop in self.props.items():
            full_string += f" {key}=\"{prop}\""
        return full_string
    
    def __repr__(self):
        full_string = f"tag=\"{self.tag}\" value=\"{self.value}\" children=\"{self.children}\" props:{self.props_to_html()}"