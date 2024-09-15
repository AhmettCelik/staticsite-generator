import shutil
import os
from markdown_blocks import markdown_to_html_node

def main():
    source_directory = "./static"
    destination_directory = "./public"
    copy_directory_recursive(source_directory, destination_directory)
    
    source_path = "./content"
    destination_path = "./public"
    template_path = "./template.html"
    
    generate_page_recursive(source_path, template_path, destination_path)

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
        
import os

import os

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    every_entry = os.listdir(dir_path_content)
    
    for entry in every_entry:
        entry_path = os.path.join(dir_path_content, entry)

        if os.path.isdir(entry_path):
            new_dest_dir_path = os.path.join(dest_dir_path, entry)
            os.makedirs(new_dest_dir_path, exist_ok=True)
            generate_page_recursive(entry_path, template_path, new_dest_dir_path)
        else:
            _, extension = os.path.splitext(entry)

            if extension.lower() in ['.md', '.markdown']:
                with open(entry_path, 'r', encoding='utf-8') as entry_file:
                    markdown_content = entry_file.read()
                
                with open(template_path, 'r', encoding='utf-8') as template_file:
                    template_HTML = template_file.read()
                
                HTML = markdown_to_html_node(markdown_content).to_html()
                template_HTML = template_HTML.replace("{{ Content }}", HTML)
            
                dest_file_path = os.path.join(dest_dir_path, entry.replace(extension, '.html'))

                with open(dest_file_path, 'w', encoding='utf-8') as dest_file:
                    dest_file.write(template_HTML)



main()
