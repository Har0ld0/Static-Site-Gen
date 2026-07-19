import sys

from site_generator import cleaning_dir, copy_to_dir, generate_page_recursive

def main():
    basepath = "/"
    if sys.argv[0] is not None:
        basepath = sys.argv[0]
    print("Cleaning /docs and copying /static into /docs")
    cleaning_dir("docs/")
    copy_to_dir("static/", "docs/")
    generate_page_recursive("content/", "template.html", "docs/", basepath)


main()
