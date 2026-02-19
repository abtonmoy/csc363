from charstream import CharStream
from tokenizer import Tokenizer
from tokenstream import TokenStream
from tokens import TokenType, Token
from acdcast import *
from acdcastpretty import *
from parser import parse
from semantic import *


import sys

# Expectation of program: 
# input filename will be sys.argv[1]
# output filename will be sys.argv[2]


# Get input from file
with open(sys.argv[1], 'r') as inputfile:
    inputlines = inputfile.readlines()

program = [] # Start with an empty list for the program
tokenstreams = [] 
#We will append ASTs to this list, one per line of source


outputfile = open(sys.argv[2], 'w')

for linenumber, line in enumerate(inputlines, start=1):
    if line.strip() == '':
        continue

    cs = CharStream(line)
    
    try:
        ts = Tokenizer(cs).tokenize()
        tokenstreams.append(ts)
        #for tok in ts:
        #    outputfile.write(str(tok) + "\n")
    


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

# Put semantic analysis here

try:
    semanticanalysis(program)
except Exception as e:
    outputfile.write(f"Semantic Error: {e}")
    outputfile.close()
    exit(1)



for statement in program:
    outputfile.write(pretty_str(statement))
    outputfile.write("\n")


outputfile.close()
