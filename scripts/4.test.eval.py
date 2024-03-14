import copy
import os
import pprint
import myutils
import os

for embeds in myutils.embeds:
    for dataset in myutils.datasets:
        for lang in myutils.data2langs[dataset]:
            test = myutils.getNLUtest(dataset, lang)
            for task in myutils.models:
                for seed in myutils.seeds:
                    lang = lang.lower()
                    name = '.'.join([embeds, dataset, lang, task, seed])

                    out = myutils.predDir + '/test.' + name

                    if os.path.isfile(out):
                        cmd = ' '.join(['python3 scripts/nluEval.py', test, out, '> ' + out + '.eval'])
                        os.system(cmd)

    


