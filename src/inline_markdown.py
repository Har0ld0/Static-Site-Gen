import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        split_texts = node.text.split(delimiter)
        if len(split_texts) % 2 == 0:
            raise ValueError("Even number of splits, should not be possible")
        for i in range(len(split_texts)):
            if split_texts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(split_texts[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_texts[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        images = extract_markdown_images(node.text)
        text_to_split = node.text
        if len(images) == 0:
            new_nodes.append(node)
            continue
        while len(images) > 0:
            image_alt = images[0][0]
            image_link = images[0][1]
            sections = text_to_split.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            if sections[1] != "" and len(images) > 1:
                text_to_split = sections[1]
            elif sections[1] != "" and len(images) == 1:
                split_nodes.append(TextNode(sections[1], TextType.TEXT))
            images.pop(0)
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        links = extract_markdown_links(node.text)
        text_to_split = node.text
        if len(links) == 0:
            new_nodes.append(node)
        while len(links) > 0:
            link_alt = links[0][0]
            link = links[0][1]
            sections = text_to_split.split(f"[{link_alt}]({link})", 1)
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(link_alt, TextType.LINK, link))
            if sections[1] != "" and len(links) > 1:
                text_to_split = sections[1]
            elif sections[1] != "" and len(links) == 1:
                split_nodes.append(TextNode(sections[1], TextType.TEXT))
            links.pop(0)
        new_nodes.extend(split_nodes)
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)

    return text_nodes
