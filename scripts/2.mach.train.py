import copy
import os
import pprint
import myutils

def write(config, name):
    jsonPath = 'configs/' + name + '.json'
    pprint.pprint(config, stream=open(jsonPath, 'wt'))

    for embed in myutils.embeds:
        for seed in myutils.seeds:
            cmd = 'python3 train.py --dataset_configs ../' + jsonPath 
            if 'base' not in name and 'attent' not in name:
                cmd += ' ../configs/' + name.split('.')[0] + '.base.json'
            fullName = embed + '.' + name + '.' + seed
            if myutils.getModel(fullName) != '':
                continue

            cmd += ' --parameters_config ../configs/params.' + embed + '.json'
            cmd += ' --name ' + fullName + ' --seed ' + seed
            print(cmd)

if not os.path.isdir('configs'):
    os.mkdir('configs')

for dataset in myutils.datasets:
    train = myutils.getNLUtrain(dataset)
    enDev = myutils.getNLUdev(dataset, 'en') 
    baseConfig = {'NLU': myutils.getNLUconfig(train, enDev, False)}

    write(baseConfig, dataset + '.base')
    for lang in myutils.data2langs[dataset]:
        lang = lang.lower()
        # don't train for de-st
        if len(lang) > 2:
            continue
    
        # UD
        udTrain, udDev = myutils.getUDTrainDev(lang)
        udLangConfig = {'UD': myutils.getUDconfig(udTrain, udDev)}
        if os.path.isfile(udTrain) and os.path.isfile(udDev):
            write(udLangConfig, dataset + '.' + lang + '.ud')

        # UPOS
        #udTrain, udDev = myutils.getUDTrainDev(lang)
        #udLangConfig = {'UPOS': myutils.getUPOSconfig(udTrain, udDev)}
        #if os.path.isfile(udTrain) and os.path.isfile(udDev):
        #    write(udLangConfig, dataset + '.' + lang + '.upos')
    
        # MLM
        mlmTrain = 'data/mt.tok/en-' + lang + '/train.' + lang
        mlmDev = 'data/mt.tok/en-' + lang + '/dev.' + lang
        if lang == 'en':
            mlmTrain = 'data/mt.tok/en-es/train.' + lang
            mlmDev = 'data/mt.tok/en-es/dev.' + lang
        mlmLangConfig = {'MLM': myutils.getMLMconfig(mlmTrain, mlmDev)}
        if os.path.isfile(mlmTrain) and os.path.isfile(mlmDev):
            write(mlmLangConfig, dataset + '.' + lang + '.mlm')
    
        # NMT
        nmtTrain = 'data/mt.tok/en-' + lang + '/train.en' + lang
        nmtDev = 'data/mt.tok/en-' + lang + '/dev.en' + lang
        nmtLangConfig = {'NMT': myutils.getNMTconfig(nmtTrain, nmtDev)}
        if os.path.isfile(nmtTrain) and os.path.isfile(nmtDev) and lang != 'en':
            write(nmtLangConfig, dataset + '.' + lang + '.nmt')
    
        # attention
        attTrain = 'data/' + dataset + '/' + lang + '.projectedTrain.conll.fixed'
        if dataset == 'multiAtis':
            attTrain = 'data/' + dataset + '/mt.train.' + lang + '.conllu.fixed'
        attentConfig = copy.deepcopy(baseConfig)
        attentConfig['NLU']['train_data_path'] = '../' + attTrain
        if os.path.isfile(attTrain) and lang != 'en':
            write(attentConfig, dataset + '.' + lang + '.attent')
    

