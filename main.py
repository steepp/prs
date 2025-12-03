import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="A JSON file to parse.")

args = parser.parse_args()
print(args.filename)
