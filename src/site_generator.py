import os
import shutil

from markdown_to_html import markdown_to_html_node

def cleaning_dir(dir: str) -> None:
    if os.path.exists(dir):
        to_delete = os.listdir(dir)
        for file in to_delete:
            path = os.path.join(dir, file)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

def copy_to_dir(source: str, destination: str) -> None:
    if not os.path.exists(destination):
        os.mkdir(destination)

    if os.path.exists(source):
        to_copy = os.listdir(source)
        for file in to_copy:
            file_path = os.path.join(source, file)
            if os.path.isfile(file_path):
                shutil.copy(file_path, destination)
            elif os.path.isdir(file_path):
                dir_path = os.path.join(destination, file)
                copy_to_dir(file_path, dir_path)

    return None

def extract_title(markdown: str) -> str:
    title = ""
    split_md = markdown.split("\n\n")
    clean_md = []
    for block in split_md:
        if block == "":
            continue
        block = block.strip()
        clean_md.append(block)

    if len(clean_md) >= 1:
        h = clean_md[0]
        if h.startswith("# "):
            title = h[2:]
        else:
            raise Exception("No header found in this md document")

    return title

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as file:
        input_read_data = file.read()

    with open(template_path) as template:
        template_data = template.read()

    html_content = markdown_to_html_node(input_read_data).to_html()
    page_title = extract_title(input_read_data)

    template_data = template_data.replace("{{ Title }}", page_title)
    template_data = template_data.replace("{{ Content }}", html_content)
    template_data = template_data.replace('href="/', f'href="{basepath}')
    template_data = template_data.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, 'w') as page:
        page.write(template_data)

def generate_page_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str):
    content_list = os.listdir(dir_path_content)

    for file in content_list:
        file_path = os.path.join(dir_path_content, file)
        if os.path.isfile(file_path) and ".md" in file_path:
            new_file_path = file.replace(".md", ".html")
            generate_page(file_path, template_path, os.path.join(dest_dir_path, new_file_path), basepath)
        elif os.path.isdir(file_path):
            generate_page_recursive(file_path, template_path, os.path.join(dest_dir_path, file), basepath)
