import sys


def getConll(path):
    data = []
    curSent = []
    for line in open(path):
        tok = line.strip('\n').split('\t')
        if len(line.strip('\n')) == 0:
            data.append(curSent)
            curSent = []
        else:
            curSent.append(tok)
    return data

conl = getConll(sys.argv[1])

for sent in conl:
    for i in reversed(range(4,len(sent))):
        curLabel = sent[i][3]
        if curLabel == 'O':
            continue
        # if the previous one is the same: I
        if curLabel[1:] == sent[i-1][3][1:]:
            sent[i][3] = 'I-' + curLabel[2:]
        # else: B
        else:
            sent[i][3] = 'B-' + curLabel[2:]
    for line in sent:
        print('\t'.join(line))
    print()
