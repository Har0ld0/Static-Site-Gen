class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html_not_implemented")

    def props_to_html(self):
        html = ""
        if not self.props or len(self.props) == 0:
            return ""
        for prop in self.props:
            html += f' {prop}="{self.props[prop]}"'

        return html

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children = {self.children}, {self.props})"
