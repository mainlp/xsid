import os

datasets = {'facebook': ['ar', 'da', 'de', 'en', 'id', 'it', 'nl', 'sr', 'zh', 'kk', 'tr', 'ja', 'st-wipptal'], 'snips': ['ar', 'da', 'de', 'en', 'id', 'it', 'nl', 'sr', 'zh', 'kk', 'tr', 'st-wipptal']}

langs = []
for lang in datasets['facebook']:
    if lang in datasets['snips']:
        langs.append(lang)
    else:
        print(lang + ' only in one language')


tgtDir = 'data/xSID/'
if not os.path.isdir(tgtDir):
    os.mkdir(tgtDir)

mapping = {}
for line in open('scripts/mapping.txt'):
    line = line.strip().split(' ')
    mapping[line[0]] = line[1]        

def mapLabels(path):
    data = []
    for line in open(path):
        tok = line.strip().split('\t')
        if len(tok) == 4:
            if tok[3][2:] in mapping:
                tok[3] = tok[3][:2] + mapping[tok[3][2:]]
            if tok[2] in mapping:
                tok[2] = mapping[tok[2]]
        if line.startswith('# intent:'):
            intent = line.split(' ')[-1].strip()
            print(intent)
            if intent in mapping:
                tok = ['# intent: ' + mapping[intent]]
        data.append(tok)
    outFile = open(path, 'w')
    for line in data:
        outFile.write('\t'.join(line) + '\n')
    outFile.close()

mapLabels('data/xSID/kk.projectedTrain.conll.fixed')

def concat(file1, file2, target):
    if not os.path.isfile(file1):
        print('Not a file: ' + file1)
        return
    if not os.path.isfile(file2):
        print('Not a file: ' + file2)
        return

    cmd = 'cat ' + file1 + ' ' + file2 + ' > ' + target
    print(cmd)
    os.system(cmd)
    mapLabels(target)    


trainFB = 'data/facebook/en/train-en.adapted.conll'
trainSN = 'data/snips/en/train-en.conll'
trainDest = tgtDir + 'en.train.conll'
concat(trainFB, trainSN, trainDest)

for lang in sorted(set(langs)):
    for split in ['test', 'valid']:
        fbFile = 'data/facebook/' + lang + '/5.' + split + '-' + lang + '.conll'
        snFile = 'data/snips/' + lang + '/4.' + split + '-' + lang + '.conll'
        target = tgtDir + lang + '.' + split + '.conll'
        concat(fbFile, snFile, target)

    #mtFB = 'data/facebook/mt.train.' + lang + '.conllu.fixed'
    #mtSN = 'data/snips/mt.train.' + lang + '.conllu.fixed'
    #target = tgtDir + lang + '.projectedTrain.conll'
    #concat(mtFB, mtSN, target)


