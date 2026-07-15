from htmlnode import HTMLNode, ParentNode
from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type
from inline_markdown import textnodes_to_htmlnodes, text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    childrens = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.QUOTE:
                lines = block.split("\n")
                new_lines = []
                for line in lines:
                    if not line.startswith(">"):
                        raise ValueError("invalid quote block")
                    new_lines.append(line.lstrip(">").strip())
                content = " ".join(new_lines)
                child_nodes = textnodes_to_htmlnodes(text_to_textnodes(content))
                node = ParentNode("blockquote", child_nodes)
                childrens.append(node)
            case BlockType.PARAGRAPH:
                lines = block.split("\n")
                paragraph = " ".join(lines)
                child_nodes = textnodes_to_htmlnodes(text_to_textnodes(paragraph))
                node = ParentNode("p", child_nodes)
                childrens.append(node)
            case BlockType.CODE:
                text = block[4:-3]
                raw_text = TextNode(text, TextType.TEXT)
                node = ParentNode("pre", [ParentNode("code", [text_node_to_html_node(raw_text)])])
                childrens.append(node)
            case BlockType.HEADING:
                h_count = 0
                for char in block:
                    if char == "#":
                        h_count += 1
                    else:
                        break
                text = block[h_count+1:]
                child_nodes = textnodes_to_htmlnodes(text_to_textnodes(text))
                node = ParentNode(f"h{h_count}", child_nodes)
                childrens.append(node)
            case BlockType.ULIST:
                lines = block.split("\n")
                list_nodes = []
                for line in lines:
                    line = line[2:]
                    list_nodes.append(ParentNode("li", textnodes_to_htmlnodes(text_to_textnodes(line))))
                node = ParentNode("ul", list_nodes)
                childrens.append(node)
            case BlockType.OLIST:
                lines = block.split("\n")
                list_nodes = []
                for line in lines:
                    clean_line = line.split(". ", 1)
                    line = clean_line[1]
                    list_nodes.append(ParentNode("li", textnodes_to_htmlnodes(text_to_textnodes(line))))
                node = ParentNode("ol", list_nodes)
                childrens.append(node)
            case _:
                raise Exception("Block type not covered")

    return ParentNode("div", childrens)
