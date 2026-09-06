import re

def main():
    # more_generic()
    re_way()

def re_way():
    s = "jayesh@gmail.com"
    if re.search(r".*@.*\.com",s):
        print("Vaiid")
    else:
        print("Invalid")

def more_generic():
    s = "malan@gamil.com"
    if s.find("@") != -1 and s.find(".",s.find("@")) != -1:
        print("valid")
    else:
        print("Invalid")

if __name__ == "__main__":
    main()