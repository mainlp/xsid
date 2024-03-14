import myutils
import os

def pred(embeds, dataset, lang, task, seed):            
    dev = '../' + myutils.getNLUdev(dataset, lang) 
    lang = lang.lower()
    if task == 'base':
        name = '.'.join([embeds, dataset, task, seed])
    else:
        name = '.'.join([embeds, dataset, lang[:2], task, seed])
    model = myutils.getModel(name)

    if len(lang) > 2 or task =='base':
        name = '.'.join([embeds, dataset, lang, task, seed])
    out = '../' + myutils.predDir + '/' + name
    if lang == 'en' and task in ['nmt', 'attent']:
        return
    
    if model != '' and not os.path.isfile(out[3:]) and not dev =='../':
        cmd = ' '.join(['python3 predict.py', model, dev, out, '--dataset NLU'])
        print('cd mtp && ' + cmd + ' && cd ../') 
    

for embeds in myutils.embeds:
    if not os.path.isdir(myutils.predDir):
        os.mkdir(myutils.predDir)
    for dataset in myutils.datasets:
        for lang in myutils.data2langs[dataset]:
            for task in myutils.models:
                for seed in myutils.seeds:
                    pred(embeds, dataset, lang, task, seed)
