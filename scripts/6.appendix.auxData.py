import myutils

def getUDsize(conlFile):
    numWords = 0
    numSents = 0
    for line in open(conlFile):
        if len(line) < 2:
            numSents += 1
        else:
            tok = line.strip().split('\t')
            if len(tok) == 10:
                numWords += 1
    return numWords, numSents

def getNMTsize(lang):
    numWords = 0
    numSents = 0
    for line in open('data/mt.tok/en-' + lang + '/train.' + lang):
        numSents += 1
        numWords += line.count(' ')
    return numWords, numSents

for lang in sorted(myutils.lang2ud):
    lang = lang.lower()
    train, _ = myutils.getUDTrainDev(lang)
    UDnumWords, UDnumSents = getUDsize(train)
    if lang == 'en':
        NMTnumWords, NMTnumSents = 0,0
    else:
        NMTnumWords, NMTnumSents = getNMTsize(lang)
    udName = myutils.lang2ud[lang.upper()].replace('_', '\\_')
    print(' & '.join([lang, udName] + ['{:,}'.format(x) for x in[UDnumSents, UDnumWords, NMTnumSents, NMTnumWords]]) + ' \\\\')

    

