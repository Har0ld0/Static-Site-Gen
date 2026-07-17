from site_generator import cleaning_dir, copy_to_dir, generate_page

def main():
    print("Cleaning /public and copying /static into /public")
    cleaning_dir("public/")
    copy_to_dir("static/", "public/")
    generate_page("content/index.md", "template.html", "public/index.html")


main()
