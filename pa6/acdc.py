from charstream import CharStream
from tokenizer import Tokenizer
from tokenstream import TokenStream
from tokens import TokenType, Token
from acdcast import *
from parser import parse
from semantic import *
from codegen import *
from constfold import constant_fold

import sys

# Expectation of program:
# input filename will be sys.argv[1]
# output filename will be sys.argv[2]

# Get input from file
with open(sys.argv[1], 'r') as inputfile:
    inputlines = inputfile.readlines()

program = []
tokenstreams = []

outputfile = open(sys.argv[2], 'w')

for linenumber, line in enumerate(inputlines, start=1):
    if line.strip() == '':
        continue

    cs = CharStream(line)

    try:
        ts = Tokenizer(cs).tokenize()
        tokenstreams.append(ts)
    except Exception as e:
        outputfile.write(f"ERROR: {type(e).__name__}: {e}\n")
        outputfile.close()
        exit(1)

for ts in tokenstreams:
    try:
        linenumber = tokenstreams.index(ts) + 1
        ast = parse(ts)
        program.append(ast)
    except Exception as e:
        outputfile.write(f"Parse Error: {e} (line {linenumber})")
        outputfile.close()
        exit(1)

# Semantic analysis
try:
    semanticanalysis(program)
except Exception as e:
    outputfile.write(f"Semantic Error: {e}")
    outputfile.close()
    exit(1)

# Constant folding optimization
program = constant_fold(program)

# Code generation
instructions = codegenerator(program)

for instruction in instructions:
    outputfile.write(instruction + '\n')

outputfile.close()
