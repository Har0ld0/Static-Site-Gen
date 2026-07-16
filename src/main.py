from site_generator import cleaning_dir, copy_to_dir

def main():
    print("Cleaning /public and copying /static into /public")
    cleaning_dir("public/")
    copy_to_dir("static/", "public/")


main()
