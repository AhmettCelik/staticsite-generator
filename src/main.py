import shutil
import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    copy_directory_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

def copy_directory_recursive(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.makedirs(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            copy_directory_recursive(src_path, dest_path)
        else:
            shutil.copy(src_path, dest_path)
            print(f'Copied file: {src_path} -> {dest_path}')
            
def extract_title(markdown):
    lines = markdown.split("\n")
    h1 = [line for line in lines if line.startswith("# ")]
    if len(h1) == 0:
        raise Exception("need least one h1")
    return h1[0]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as from_file:
        from_path_as_string = from_file.read()
        
    with open(template_path, 'r') as template_file:
        template_path_as_string = template_file.read()
        
    HTML = markdown_to_html_node(from_path_as_string).to_html()
    page_title = extract_title(from_path_as_string)
    
    new_template_path_as_string = template_path_as_string.replace("{{ Title }}", page_title)
    new_template_path_as_string = new_template_path_as_string.replace("{{ Content }}", HTML)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'w') as dest_file:
        dest_file.write(new_template_path_as_string)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
            
main()
