from enum import Enum


class TextType(Enum):
    TEXT_PLAIN = "text"
    BOLD_TEXT = "**Bold text**"
    ITALIC_TEXT = "_Italic text_"
    CODE_TEXT = "'Code text'"
    LINKS = "[anchor text](url)"
    IMAGES = "![alt text](url)"


class TextNode:
    def __init__(self, text, text_type: TextType, url):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        else:
            return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url}"
