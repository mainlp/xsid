#from transformers import AutoTokenizer
#tokenizer = AutoTokenizer.from_pretrained("xlm-mlm-tlm-xnli15-1024")

import sys
from allennlp.data.tokenizers import Token, PretrainedTransformerTokenizer

tokenizer  = PretrainedTransformerTokenizer('xlm-mlm-tlm-xnli15-1024')

def count(path):
    unk = 0
    total = 0
    sent = ''
    for line in open(path):
        tok = line.split('\t')
        if len(line.strip()) <= 1:
            for word in tokenizer.tokenize(sent.strip()):
                #print(word)
                if word.text == '<unk>':
                    unk+= 1
                total += 1
            sent = ''
        elif len(tok) != 4:
            continue
        else:
            sent += tok[1] + ' '
    print(path)
    print(unk, total)
    print(unk/ total)
    print()

for path in sys.argv[1:]:
    count(path)
for word in tokenizer.tokenize("Don't you love 🤗 Transformers? We sure do."):
    print(word, word.text == '<unk>')
        

