def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block_of_markdown):
    block_of_markdown = block_of_markdown.strip()
    heading_prefixes = ["# ", "## ", "### ", "#### ", "##### ", "###### "]

    for prefix in heading_prefixes:
        if block_of_markdown.startswith(prefix):
            return "heading"

    if block_of_markdown.startswith("```") and block_of_markdown.endswith("```"):
        return "code"

    if block_of_markdown.startswith(">"):
        return "quote"

    if block_of_markdown.startswith("* ") or block_of_markdown.startswith("- "):
        split_block = block_of_markdown.split("\n")
        for line in split_block:
            if not (line.startswith("* ") or line.startswith("- ")):
                return "paragraph"
        return "unordered_list"

    ordered_list_count = 1
    if block_of_markdown.startswith("1. "):
        split_block = block_of_markdown.split("\n")
        for line in split_block:
            if line.startswith(f"{ordered_list_count}. "):
                ordered_list_count += 1
            else:
                return "paragraph"
        return "ordered_list"

    return "paragraph"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

    
