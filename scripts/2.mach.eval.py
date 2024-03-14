import copy
import os
import pprint
import myutils
import os

for embeds in myutils.embeds:
    for dataset in myutils.datasets:
        for lang in myutils.data2langs[dataset]:
            dev = myutils.getNLUdev(dataset, lang)
            lang = lang.lower()
            for task in myutils.models:
                if lang == 'en' and task in ['attent', 'nmt']:
                    continue
                for seed in myutils.seeds:
                    name = '.'.join([embeds, dataset, lang, task, seed])
    
                    out = myutils.predDir + '/' + name
                    if os.path.isfile(out):
                        cmd = ' '.join(['python3 scripts/nluEval.py', dev, out, '> ' + out + '.eval'])
                        os.system(cmd)
                    else:
                        print("ERROR: ", name, ' not found')

    


