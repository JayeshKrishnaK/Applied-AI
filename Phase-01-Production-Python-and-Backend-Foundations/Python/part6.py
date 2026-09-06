import csv
import sys
from PIL import Image

def main():
    # file_ops_wo_with()
    # file_ops_w_with()
    # print_names_in_sorted_order()

    #csv
    # file_ops_write_to_csv()
    # file_ops_read_from_csv()

    # Binary files - image
    file_ops_with_binary()

def file_ops_write_to_csv():
    # get input about family
    family = []
    for _ in range(4):
        member = {}
        # this below code, creates a function object and assigns it to name and place respectively.
        name = lambda : input("Enter your name: ")
        place = lambda : input("Enter your place: ")
        member = {"name": name(), "place": place()} # calling the function here.
        family.append(member)

    # *******Using file object itself to write********

    with open("family.csv", "w") as file:
        for member in family:
            file.write(f"{member["name"]},{member["place"]}\n")

    """
    Input:
    Enter your name: name
    Enter your place: place
    Enter your name: Jayesh Krishna
    Enter your place: Civil Aerodrome Post, CBE
    Enter your name: Kannan
    Enter your place: Bhavani, Erode
    Enter your name: Latha
    Enter your place: Bhavani, Erode

    Output to csv:
    name,place
    Jayesh Krishna,Civil Aerodrome Post, CBE
    Kannan,Bhavani, Erode
    Latha,Bhavani, Erode
    """

    # ******************Using writer*******************

    # with open("family.csv","w",newline="") as file:
    #     writer = csv.writer(file)
    #     # writer.writerow(["name","place"])
    #     writer.writerows([
    #         ["name","place"],
    #         ["Jayesh","Civil,Aerodrome Post, Coimbatore"],
    #         ["Kannan","Bhavani","Erode"],
    #         # ["Latha",,"Bhavani"], # Throw an error as normally we fill array without missing any values in between
    #         ["Suba","Bhavani",] # Works fine
    #     ])

    '''
    Output:
    name,place
    Jayesh,"Civil,Aerodrome Post, Coimbatore"
    Kannan,Bhavani,Erode
    Suba,Bhavani
    '''

    # ****************using DictWriter**************

    with open("family.csv","w",newline="") as file:

        writer = csv.DictWriter(file,fieldnames=["name","place"])
        writer.writerows([
            {"name": "Jayesh","place": "CBE"},
            {"name": "Kannan","place": "Bhavani"}
            ])
        '''
        Output:
        Jayesh,CBE
        Kannan,Bhavani
        '''

        # writer = csv.DictWriter(file,fieldnames=["place","name"])
        # writer.writerows([
        #     {"name": "Jayesh","place": "CBE"},
        #     {"name": "Kannan","place": "Bhavani"}
        #     ])
        '''
        Output:
        CBE,Jayesh
        Bhavani,Kannan
        '''

        # writer = csv.DictWriter(file,fieldnames=["name","place","district"])
        # writer.writerows([
        #     {"name": "Jayesh","place": "CBE"},
        #     {"name": "Kannan","place": "Bhavani"},
        #     {"name": "Kannan","place": "","district":"Erode"},
        #     {"name": "Suba","district": "Erode"},
        #     ])
        '''
        Output:
        Jayesh,CBE,
        Kannan,Bhavani,
        Kannan,,Erode
        Suba,,Erode
        Note: 
        1. For Output lines 1 & 2 -> At end comma is added, When reading it will be trated as empty string for fieldname "district"
        2. For output line 3 -> As I just passed an empty string for "place", When reading - "place" : "" 
        3. Output line 4 -> Here also my dict didnt contain "place" key, so an empty string is added.
        So if there is no value for a defined Key -> an empty string is added
        '''

        # writer = csv.DictWriter(file,fieldnames=["name","place"])
        # writer.writerows([
        #     {"name": "Jayesh","place": "CBE"},
        #     {"name": "Kannan","place": "Bhavani"},
        #     {"name": "Kannan","place": "","district":"Erode"},
        #     {"name": "Suba","district": "Erode"},    
        #     ])
        '''
        Output:
        ValueError: dict contains fields not in fieldnames: 'district'
        -> Why?
        It checked if there is any feildname called "district" exists, as we don't have one. It don't know
        where to put the value of key "district". So it resulted in ValueError
        Note: So It's mandatory to provide only the dict keys as mentioned by fieldnames
        '''

def file_ops_read_from_csv():
    """
    family.csv
    
    Kannan,Sri Bright Designers office
    Jayesh Krishna,MCW office
    Suba Lakshmi,Aadharsh School
    Latha,Home
    """

    # *******Using file object itself to read********

    # family = []
    # with open("family.csv") as file:
    #     for line in file:
            # member = line.rstrip().split(",")
            # family.append({"name":member[0], "place":member[1]})

            # better approach:
            # name, place = line.rstrip().split(",")
            # family.append({"name":name, "place":place})

    # Task - Print
    # for member in family:
    #     print(f"{member["name"]} is in {member["place"]}")

    # Task print them in sorted order by names
    # key here takes a function object. That is is why In lecture, he just passed function name.
    # for member in sorted(family, key= lambda member: member["name"]):
    #     print(f"{member["name"]} is in {member["place"]}")

    # **********Using CSV module's reader function to read a csv************

    # Task - same as before but now we have values containing ,(comma) in them
    '''
    family.csv

    Kannan,"Sri Bright Designers office, Bhavani"
    Jayesh Krishna,"MCW office, Civil Aerodrome Post"
    Suba Lakshmi,"Aadharsh School, Anthiyur"
    Latha,"Home, Bhavani"
    '''
    # with open("family.csv") as file:
        # reader = csv.reader(file) # Returns  a iteratable object
    #     for name,place in reader:
    #         print(f"{name} is in {place}")

    # ************Using CSV module's dictReader to read a csv**********

    # Task - same as before
    # To use this, our csv must have a column header. By default 
    # first row is treated as header. Our csv assumed here is:
    '''
    family.csv

    name,place
    Kannan,"Sri Bright Designers office, Bhavani"
    Jayesh Krishna,"MCW office, Civil Aerodrome Post"
    Suba Lakshmi,"Aadharsh School, Anthiyur"
    Latha,"Home, Bhavani"
    '''
    with open("family.csv") as file:
        # reader = csv.DictReader(file)
        reader = csv.DictReader(file,fieldnames=["name","place"])
        # reader = csv.DictReader(file,fieldnames=["place","name"])
        # reader = csv.DictReader(file,fieldnames=["name","place","district"])
        for member in reader:
            print(member)
            # print(f"{member["name"]} is in {member["place"]}")

def print_names_in_sorted_order():
    #Write  names
    file_ops_w_with()

    names = []
    with open("names.txt") as file:
        for line in file:
            names.append(line.rstrip())

    for name in sorted(names):
        print(name)

def file_ops_w_with():
    # name = input("Enter a name: ")

    # write
    # with open("names.txt","w") as file:
    #     file.write(name)

    # task - append all family members in file. Each member in a new line
    names = []
    for _ in range(4):
        names.append(input("Enter name: "))

    with open("names.txt","a") as file:
        for name in names:
            # file.write(name) # Output - JayeshSubaKannanLatha
            file.write(f"{name}\n")

    #read - default one, can be specified explicitly as well "r"
    # with open("names.txt") as file:
        # for line in file.readlines():
        #     # print(line) # Here extra line due to while writing to file we did \n and by default print has end='\n'
        #     print(line.rstrip()) # reomve white space characters at end

        # using iterator object
        # for line in file:
        #     print(line.rstrip())

def file_ops_wo_with():
    '''
    Closing should be handled separately.
    '''
    name = input("Enter a name: ")
    file = open("names.txt","w")
    file.write(name)
    file.close()

def file_ops_with_binary():
    images= []
    for file in sys.argv[1:]:
        image = Image.open(file)
        images.append(image)
    images[0].save("sparrow.gif",save_all=True,append_images=[images[1],images[2],images[3]],duration=100,loop=0)
    

if __name__ == "__main__":
    main()