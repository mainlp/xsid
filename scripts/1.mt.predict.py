import os
import myutils

for dataset in myutils.datasets:
    trainPath = myutils.getNLUtrain(dataset)

    for lang in myutils.data2langs[dataset]:
        lang = lang.lower()
        if not os.path.isfile('data/mt.models/' + lang + '/checkpoint_best.pt'):
            print(lang)
            continue
        tgtPath = 'data/' + dataset + '/mt.train.' + lang + '/'
        if not os.path.isfile(tgtPath[:-1] + '.conllu'):
            cmd = './scripts/1.mt.predict.sh ' + lang + ' 0 ' + trainPath + ' ' + tgtPath  
            print(cmd)
            cmd = 'python3 scripts/combine.py ' + lang + ' ' + tgtPath + ' > ' + tgtPath[:-1] + '.conllu'
            print(cmd)
            cmd = 'python3 scripts/fixBIO.py ' + tgtPath[:-1] + '.conllu > ' + tgtPath[:-1] + '.conllu.fixed'
            print(cmd)
            

