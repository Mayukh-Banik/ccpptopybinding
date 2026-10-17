import argparse


def add_one(number):
    return number + 1


def main():
    parser = argparse.ArgumentParser(description="Add one to a number.")
    parser.add_argument("number", type=int, help="the number to increment")
    args = parser.parse_args()
    print(add_one(args.number))


if __name__ == "__main__":
    main()