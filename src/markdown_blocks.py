def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            clean_blocks.append(block)

    return clean_blocks
