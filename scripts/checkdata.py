import os
import myutils
rootDir = 'data/xSID-0.3/'

def checkText(path):
    curText = ''
    words = []
    for lineIdx, line in enumerate(open(path)):
        if line.startswith('# text: '):
            if ''.join(words) != curText.replace(' ', '') and curText != '':
                print('MISMATCH in ' + path + ': ' + str(lineIdx) )
                print(' '.join(words))
                print(curText)
                print(''.join(words))
                print(curText.replace(' ', ''))
                print()
            curText = line[8:].strip()
            words = []
        if len(line.split('\t')) == 4:
            words.append(line.split('\t')[1])
    if ''.join(words) != curText.replace(' ', '') and curText != '':
        print('MISMATCH in ' + path + ': ' + str(lineIdx) )
        print(' '.join(words))
        print(curText)
        print(''.join(words))
        print(curText.replace(' ', ''))
        print()

def checkENmatch(langPath, enPath):
    dataEN = []
    for line in open(enPath):
        if line.startswith('# text: '):
            dataEN.append(line[8:])
    data = []
    for line in open(langPath):
        if line.startswith('# text-en: '):
            data.append(line[11:])
    for sent, sentEN in zip(data, dataEN):
        if sent != sentEN:
            print('MISMATCH with EN:')
            print(sent)
            print(sentEN)
            print()

for lang in myutils.data2langs['xSID']:
    #if lang == 'en':
    #    continue
    for split in ['valid', 'test']:
        checkText(rootDir + lang + '.' + split + '.conll')
    if lang == 'en':
        checkText(rootDir + 'en.train.conll')
    else:
        for split in ['valid', 'test']:
            checkENmatch(rootDir + lang + '.' + split + '.conll', rootDir + 'en.' + split + '.conll')

