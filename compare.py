import ast
import numpy as np
import argparse
from argparse import RawTextHelpFormatter


def get_text_from_file(file_name):
    with open(file_name) as input:
        text = input.read()
    return text

def preprocess_code(code):
    code = ast.unparse(ast.parse(code))
    code = "".join(filter(lambda x: not x.isspace(), code))
    code = code.lower()
    return code

def find_edit_distance(first_code, second_code):
    n = len(first_code)
    m = len(second_code)
    if n > m:
        first_code, second_code = second_code, first_code
    n = len(first_code)
    m = len(second_code)
    distances = range(n + 1)
    for i2, c2 in enumerate(second_code):
        distances_ = [i2+1]
        for i1, c1 in enumerate(first_code):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]/len(first_code)

parser = argparse.ArgumentParser(
                    prog = 'Compare.py',
                    description = 'Program compares two source codes written \
                         in Python using Levenshtein distance', \
                    formatter_class = RawTextHelpFormatter)

parser.add_argument('input_file_name', help= 'Name of file with paths to files which this program needs to compare.\nThis file needs to be in the following format :\nfiles/main.py plagiat1/main.py\nfiles/loss.py plagiat2/loss.py')
parser.add_argument('output_file_name', help = 'Name of file where you want to store results of comparings')
args = parser.parse_args()
results = []
with open(args.input_file_name) as input:
    for line in input.readlines():
        first_file_name = line.strip().split(' ')[0]
        second_file_name = line.strip().split(' ')[1]
        first_text = get_text_from_file(first_file_name)
        second_text = get_text_from_file(second_file_name)
        first_code = preprocess_code(first_text)
        second_code = preprocess_code(second_text)
        results.append(str(find_edit_distance(first_code, second_code)))
with open(args.output_file_name, 'w') as output:
    output.write('\n'.join(results))
