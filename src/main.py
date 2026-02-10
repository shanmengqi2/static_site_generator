from block_to_html import markdown_to_html_node
from textnode import TextNode, TextType
from leafnode import LeafNode
import os
import sys


def copy_static_to_public():
    """
    Copies all contents from the static directory to the public directory.
    First deletes all contents of the public directory to ensure a clean copy.
    """
    # Get the project root directory (parent of src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "docs")

    # Delete all contents of public directory
    if os.path.exists(public_dir):
        print(f"Deleting contents of {public_dir}")
        delete_directory_contents(public_dir)
    else:
        print(f"Creating {public_dir}")
        os.makedirs(public_dir)

    # Copy all contents from static to public
    print(f"Copying from {static_dir} to {public_dir}")
    copy_directory_contents(static_dir, public_dir)


def delete_directory_contents(directory_path):
    """
    Recursively deletes all contents of a directory without deleting the directory itself.
    """
    if not os.path.exists(directory_path):
        return

    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)

        if os.path.isfile(item_path):
            print(f"  Deleting file: {item_path}")
            os.remove(item_path)
        elif os.path.isdir(item_path):
            print(f"  Deleting directory: {item_path}")
            delete_directory_contents(item_path)  # Recursively delete contents
            os.rmdir(item_path)  # Remove the empty directory


def copy_directory_contents(src_dir, dest_dir):
    """
    Recursively copies all files and subdirectories from src_dir to dest_dir.
    """
    if not os.path.exists(src_dir):
        raise ValueError(f"Source directory does not exist: {src_dir}")

    # Ensure destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Iterate through all items in the source directory
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            # Copy file
            print(f"  Copying file: {src_path} -> {dest_path}")
            with open(src_path, 'rb') as src_file:
                with open(dest_path, 'wb') as dest_file:
                    dest_file.write(src_file.read())
        elif os.path.isdir(src_path):
            # Create subdirectory and recursively copy its contents
            print(f"  Creating directory: {dest_path}")
            os.makedirs(dest_path, exist_ok=True)
            copy_directory_contents(src_path, dest_path)  # Recursive call


def extract_title(markdown):
    """
    Extracts the h1 header from markdown text.

    Args:
        markdown: A string containing markdown text

    Returns:
        The h1 header text without the # and leading/trailing whitespace

    Raises:
        ValueError: If no h1 header is found in the markdown
    """
    lines = markdown.split('\n')

    for line in lines:
        # Strip leading/trailing whitespace to check the line
        stripped_line = line.strip()

        # Check if line starts with exactly one # followed by a space
        if stripped_line.startswith('# ') and not stripped_line.startswith('## '):
            # Extract the title by removing the # and stripping whitespace
            title = stripped_line[1:].strip()
            return title

    # If we get here, no h1 header was found
    raise ValueError("No h1 header found in markdown")


def generate_page(from_path, template_path, dest_path, basepath):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as from_file:
        markdown = from_file.read()

    with open(template_path, 'r') as template_file:
        template = template_file.read()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    # replace href="/ with href="{basepath} src="/ with src="{basepath}
    template = template.replace("href=\"/", f"href=\"{basepath}\"")
    template = template.replace("src=\"/", f"src=\"{basepath}\"")

# if dest not exits , create it
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, 'w') as dest_file:
        dest_file.write(template)


def main():
    basepath = sys.argv[1] or "/"
    copy_static_to_public()

    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive(
        "content", "template.html", "docs", basepath)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    """
    Recursively crawls the content directory and generates HTML pages for all markdown files.

    Args:
        dir_path_content: Path to the content directory to crawl
        template_path: Path to the HTML template file
        dest_dir_path: Path to the destination directory where HTML files will be generated
    """
    # Ensure the content directory exists
    if not os.path.exists(dir_path_content):
        raise ValueError(
            f"Content directory does not exist: {dir_path_content}")

    # Iterate through all items in the content directory
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)

        if os.path.isfile(item_path):
            # Check if it's a markdown file
            if item.endswith('.md'):
                # Generate the destination path by replacing .md with .html
                dest_file = item.replace('.md', '.html')
                dest_path = os.path.join(dest_dir_path, dest_file)

                # Generate the HTML page
                generate_page(item_path, template_path, dest_path, basepath)

        elif os.path.isdir(item_path):
            # Create corresponding subdirectory in destination
            dest_subdir = os.path.join(dest_dir_path, item)

            # Recursively process the subdirectory
            generate_pages_recursive(
                item_path, template_path, dest_subdir, basepath)


if __name__ == "__main__":
    main()
