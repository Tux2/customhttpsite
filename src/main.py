from textnode import *
import os
import sys
import shutil
from markdownfunctions import *

def copy(public_folder, static_folder, path=""):
    full_path = os.path.join(public_folder, path)
    read_path = os.path.join(static_folder, path)
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    files = os.listdir(read_path)
    for file in files:
        file_path = os.path.join(read_path, file)
        if os.path.isdir(file_path):
            new_path = os.path.join(path, file)
            copy(public_folder, static_folder, new_path)
        else:
            shutil.copy(file_path, os.path.join(full_path, file))

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path, 'r')
    markdown = f.read()
    f.close()
    template_f = open(template_path, 'r')
    template = template_f.read()
    template_f.close()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    result = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
    dir = os.path.dirname(dest_path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    w = open(dest_path, 'w')
    w.write(result)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    files = os.listdir(dir_path_content)
    for file in files:
        source = os.path.join(dir_path_content, file)
        if file.endswith(".md"):
            dest = os.path.join(dest_dir_path, file[:-3] + ".html")
            generate_page(source, template_path, dest, basepath)
        elif os.path.isdir(source):
            dest = os.path.join(dest_dir_path, file)
            generate_pages_recursive(source, template_path, dest, basepath)


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    public_folder = "docs"
    static_folder = "static"
    if os.path.exists(public_folder):
        shutil.rmtree(public_folder)
    copy(public_folder, static_folder)
    generate_pages_recursive("content", "template.html", "docs", basepath)
    

main()