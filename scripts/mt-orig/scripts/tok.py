import bert_tokenize
import sys

tknzr = bert_tokenize.BasicTokenizer()

for line in open(sys.argv[1]):
    print(' '.join(tknzr.tokenize(line.strip('\n'))))
