import myutils
import os

for embeds in myutils.embeds:
    if not os.path.isdir(myutils.predDir):
        os.mkdir(myutils.predDir)
    for dataset in myutils.datasets:
        for lang in myutils.data2langs[dataset]:
            test = '../' + myutils.getNLUtest(dataset, lang) 
            for task in myutils.models:
                for seed in myutils.seeds:
                    lang = lang.lower()
                    if task == 'base':
                        name = '.'.join([embeds, dataset, task, seed])
                    else:
                        name = '.'.join([embeds, dataset, lang[:2], task, seed])

                    model = myutils.getModel(name)
                    if task == 'base' or len(lang) > 2:
                        name = '.'.join([embeds, dataset, lang, task, seed])
                    out = '../' + myutils.predDir + '/test.' + name
            
                    if model != '' and not os.path.isfile(out[3:]):
                        cmd = ' '.join(['python3 predict.py', model, test, out, '--dataset NLU'])
                        print('cd mtp && ' + cmd + ' && cd ../') 

