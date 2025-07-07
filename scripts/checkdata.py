import os
import myutils
rootDir = 'data/xSID-0.7/'

def checkText(path):
    counter = 0
    curText = ''
    words = []
    for lineIdx, line in enumerate(open(path)):
        if line.startswith('# text = '):
            if ''.join(words) != curText.replace(' ', '') and curText != '':
                print('MISMATCH in ' + path + ': ' + str(lineIdx) )
                print(' '.join(words))
                print(curText)
                print(''.join(words))
                print(curText.replace(' ', ''))
                print()
                counter += 1
            curText = line[8:].strip()
            words = []
        if len(line.split('\t')) == 4:
            words.append(line.split('\t')[1])



for conllFile in sorted(os.listdir(rootDir)):
    if conllFile[0] == '.':
        continue
    if 'train' in conllFile:
        continue
    checkText(rootDir + conllFile)
    #checkBIO()
    #checkLabels()

