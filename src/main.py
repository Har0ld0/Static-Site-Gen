from site_generator import cleaning_dir, copy_to_dir, generate_page_recursive

def main():
    print("Cleaning /public and copying /static into /public")
    cleaning_dir("public/")
    copy_to_dir("static/", "public/")
    generate_page_recursive("content/", "template.html", "public/")


main()
