import sys

for path in sys.argv[1:]:
    outFile = open(path.replace('tsv', 'conll'), 'w')
    for lineIdx, line in enumerate(open(path)):
        tok = line.strip('\n').split('\t')
        if tok[0] == 'id':
            continue
        words = tok[1].split(' ')
        labels = tok[2].split(' ')
        intent = tok[3]
        outFile.write('# id: ' + str(lineIdx) + '\n')
        outFile.write('# text: ' + tok[1] + '\n')
        #outFile.write('# text-en: ') 
        outFile.write('# intent: ' + intent + '\n')
        if len(words) != len(labels):
            print(path, lineIdx)
        for wordIdx in range(min(len(words), len(labels))):
            outFile.write('\t'.join([str(wordIdx+1), words[wordIdx], intent, labels[wordIdx]]) + '\n')
        outFile.write('\n')
    outFile.close()

