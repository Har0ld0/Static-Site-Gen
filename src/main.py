import sys

from site_generator import cleaning_dir, copy_to_dir, generate_page_recursive

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print(basepath)
    print("Cleaning /docs and copying /static into /docs")
    cleaning_dir("docs/")
    copy_to_dir("static/", "docs/")
    generate_page_recursive("content/", "template.html", "docs/", basepath)


main()
