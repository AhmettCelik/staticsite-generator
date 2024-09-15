import shutil
import os
from markdown_blocks import markdown_to_html_node

def main():
    source_directory = "./static"
    destination_directory = "./public"
    copy_directory_recursive(source_directory, destination_directory)
    
    source_path = "./content/index.md"
    destination_path = "./public/index.html"
    template_path = "./template.html"
    
    generate_page(source_path, template_path, destination_path)

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

main()
