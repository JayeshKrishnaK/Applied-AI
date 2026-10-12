import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name",
                        "-n",
                        default="Dumbass, Can't you use -h and see how to use me?",
                        type=str,
                        help="Please provide your name in double quotes to me 😊",
                        dest="name")
    args = parser.parse_args()

    print("Bye Bye 👋🏻,",args.name)