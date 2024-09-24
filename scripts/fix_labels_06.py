import os

oldPath = 'data/xSID-0.5'
newPath = 'data/xSID-0.6'
if not os.path.isdir(newPath):
    os.mkdir(newPath)

slot_mapping = {'Orecurring_datetime': 'O', 'B-ecurring_datetime': 'B-recurring_datetime', 'I-dateime': 'I-datetime', 'I-ecurring_datetime': 'I-recurring_datetime', 'I-locatioin': 'I-location'}

for conlFile in os.listdir(oldPath):
    old_path = os.path.join(oldPath, conlFile)
    new_file = open(os.path.join(newPath, conlFile), 'w')

    for line in open(old_path):
        tok = line.strip().split('\t')
        if len(line.strip()) <= 2:
            new_file.write('\n')
        elif line[0] == '#':
            new_file.write(line)
        else:
            if len(tok) != 4:
                if '' in tok:
                    index = tok.index('')
                    tok = tok[:index] + tok[index+1:]
                elif ' ' in line:
                    line = line.replace(' ', '\t')
                    tok = line.strip().split('\t')
                else:
                    print('ERROR', conlFile, tok)
            tok = [x.strip() for x in tok]
            if tok[2] == 'RateBooke':
                tok[2] = 'RateBook'
            if tok[3] in slot_mapping:
                tok[3] = slot_mapping[tok[3]]
            new_file.write('\t'.join(tok) + '\n')

            
