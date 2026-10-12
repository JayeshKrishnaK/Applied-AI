import re

def main():
    # more_generic()
    # re_way()
    re_examples()
    # format_name()
    # extract_username_from_url()
    # misc()

def misc():
    s = "apple,;banana;orange"
    print(re.split(r";",s)) # ['apple,', 'banana','orange']
    print(re.findall(r";",s)) # [';', ';']

def extract_username_from_url():
    url = "https://x.com/BillGates?lang=en"
    pattern = r"^(?:https?://)?(?:www\.)?x\.com/([a-z0-9_]+).*"

def format_name():
    # Task - IF name is entered in isreali way like Kannan,Jayesh Krishna, we need to format it to global way.
    # if normal way then, print as it is, if not, then format and print it.
    
    '''
    To explain group() vs groups()
    name = "cats"
    match = re.search(r"(cat|dog)s",name)
    print(match.groups()[0])
    '''
    name = input("Enter your name: ").strip()
    pattern = r"^([A-Za-z]+) *, *([A-Z][a-z]+) *([A-Z][a-z]+)?" # ?: Cant be used cause I stil need to capture
    '''
    ([A-Z][a-z]+) Vs ([A-Za-z]+)
    
    ([A-Z][a-z]+) - ([Any one charcater of A-Z][Any one charcater of a-z] - 1 or more reps)
    *** for input Kolla, anuRA it won't find a match at all. it won't enter the blow if conditions
    ([A-Za-z]+) - ([Any one charcater of A-Z or a-z] - 1 or more reps) - ****RIGHT WAY****
    '''
    if match := re.search(pattern,name): # use of warlus operator
        nameBreakdown = match.groups()
        print(nameBreakdown)
        '''
        Important:
        Enter your name: Kolla,Anurag
        ('Kolla', 'Anurag', None)
        '''
        if len(nameBreakdown) == 3 and nameBreakdown[2] != None:
            name = nameBreakdown[1] + " " + nameBreakdown[2] + " " + nameBreakdown[0]
        else:
            name = nameBreakdown[1] + " " + nameBreakdown[0]
    print(f"Hello {name}")


def re_examples():
    s = "jaaaay"
    m =  re.search(r"a*ay",s)
    print(m.group())


def re_way():
    s = ".edu@.edu"
    # pattern = r"^[^@]+@[^@]+\.edu$"
    pattern = r"^\w+@\w+\.edu"  # will fail for malan@cs50.harvard.edu
    pattern = r"^\w+@(\w+\.)?\w+\.edu" # if I don't include ? then malan@harvard.edu will fail but malan@cs50.harvard.edu will pass
    pattern = r"^(\w|\.)+@(\w+\.)?\w+\.edu" # it still works for emails with . inbetween. As every rep checks either a \w or .
    if re.search(pattern,s):
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