#!/usr/bin/python3

import sys
import os
import hashlib


def convert_md5(content):
    return hashlib.md5(content.encode()).hexdigest()


def remove_chars(content, chars):
    for char in chars:
        content = content.replace(char, "")
    return content


def convert_markdown_to_html(markdown_file, output_file):
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    # Read the content of the Markdown file
    with open(markdown_file, "r") as f:
        markdown_content = f.read()

    # Convert Markdown headings to HTML headings
    html_content = markdown_content.replace("# ", "<h1>").replace("## ", "<h2>").replace(
        "### ", "<h3>").replace("#### ", "<h4>").replace("##### ", "<h5>").replace("###### ", "<h6>")
    html_content = html_content.replace("\n", "</h1>\n")

    # Convert Markdown ordered lists to HTML ordered lists
    html_content = html_content.replace(
        "* ", "<ol>\n<li>").replace("\n* ", "</li>\n<li>")
    html_content = html_content.replace(
        "</h1>\n<ol>", "</h1>\n").replace("</li>\n<h2>", "</li>\n</ol>\n<h2>")

    # Convert Markdown unordered lists to HTML unordered lists
    html_content = html_content.replace(
        "- ", "<ul>\n<li>").replace("\n- ", "</li>\n<li>")
    html_content = html_content.replace("</h1>\n<ul>", "</h1>\n")

    # Convert Markdown paragraphs to HTML paragraphs
    html_content = html_content.replace(
        "\n\n", "</p>\n<p>").replace("\n", "<br />\n")
    html_content = "<p>\n" + html_content + "</p>\n"

    # Convert bold and emphasized text to HTML
    html_content = html_content.replace(
        "**", "<b>").replace("__", "<em>").replace("</em></b>", "</b></em>")

    # Convert [[Hello]] to MD5
    md5_list = []
    for match in re.findall(r'\[\[(.*?)\]\]', html_content):
        md5_list.append(match)
    for match in md5_list:
        html_content = html_content.replace(f"[[{match}]]", convert_md5(match))

    # Convert ((Hello Chicago)) to remove characters
    remove_chars_list = []
    for match in re.findall(r'\(\((.*?)\)\)', html_content):
        remove_chars_list.append(match)
    for match in remove_chars_list:
        html_content = html_content.replace(
            f"(({match}))", remove_chars(match, "c"))

    # Write the HTML content to the output file
    with open(output_file, "w") as f:
        f.write(html_content)

    print(f"Converted {markdown_file} to {output_file}")
    sys.exit(0)


def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <markdown_file> <output_file>",
              file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(markdown_file, output_file)


if __name__ == "__main__":
    main()
