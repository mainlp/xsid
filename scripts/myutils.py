import os
import statistics 

lang2ud = {'DE':'UD_German-GSD', 'ES':'UD_Spanish-GSD', 'FR':'UD_French-GSD', 'HI':'UD_Hindi-HDTB', 'JA':'UD_Japanese-GSD', 'PT':'UD_Portuguese-GSD', 'TR':'UD_Turkish-IMST', 'ZH':'UD_Chinese-GSD', 'NL':'UD_Dutch-LassySmall', 'IT': 'UD_Italian-ISDT', 'DA':'UD_Danish-DDT', 'AR':'UD_Arabic-PADT', 'KK': 'UD_Kazakh-KTB', 'ES':'UD_Spanish-GSD', 'SR':'UD_Serbian-SET', 'EN': 'UD_English-EWT', 'TH': 'UD_Thai-PUD', 'ID': 'UD_Indonesian-GSD'}

data2langs = {'multiAtis': ['DE', 'EN', 'ES', 'FR', 'HI', 'JA', 'PT', 'TR', 'ZH'], 'facebook-orig': ['en', 'th', 'es'], 'xSID': ['ar', 'da', 'de', 'de-st', 'en', 'id', 'it', 'ja', 'nl', 'sr', 'zh', 'tr', 'kk'], 'snips': ['en']}

convLang = {'de':'deu', 'es':'spa', 'ja':'jpn', 'tr':'tur', 'nl':'nld', 'it':'ita', 'da':'dan', 'ar':'arb', 'kk':'kaz', 'sr':'srp', 'en':'eng', 'id':'ind', 'zh':'cmn'}

xlmLangs = ['de', 'en', 'ar', 'zh', 'tr']

datasets = ['xSID', 'multiAtis']

embeds = ['mbert', 'xlm15'] # these have to match a configs/params.[EMBEDNAME].json file

models = ['base', 'attent', 'mlm', 'nmt', 'ud']#, 'upos']

names = ['base', 'nmt-transfer', 'aux-mlm', 'aux-nmt', 'aux-ud']#, 'aux-upos']

predDir = 'predictions/'

seeds = ['1','2','3','4','5']

def getModel(name):
    modelDir = 'mtp/logs/'
    nameDir = modelDir + name + '/'
    if os.path.isdir(nameDir):
        for modelDir in os.listdir(nameDir):
            modelPath = nameDir + modelDir + '/model.tar.gz'
            if os.path.isfile(modelPath):
                return modelPath[4:]
    return ''

def getMtLangs():
    allLangs = set()
    for dataset in datasets:
        for lang in data2langs[dataset]:
            lang = lang.lower()
            if len(lang) == 2 and lang != 'en':
                allLangs.add(lang)
    return allLangs


def getUDTrainDev(lang):
    train = ''
    dev = ''
    test = ''
    udDir = 'data/ud-treebanks-v2.6/' + lang2ud[lang.upper()] + '/'
    for conlFile in os.listdir(udDir):
        if 'train' in conlFile and conlFile.endswith('.conllu'):
            train = udDir + conlFile
        if 'test' in conlFile and conlFile.endswith('.conllu'):
            test = udDir + conlFile
        if 'dev' in conlFile and conlFile.endswith('.conllu'):
            dev = udDir + conlFile
    if train == '' and dev == '':
        train = test
        dev = test
    if lang == 'kk':
        dev = train
        train = test
    return train, dev

def getNLUconfig(trainPath, devPath, crf=True):
    config = {}
    config['train_data_path'] = '../' + trainPath
    config['validation_data_path'] = '../' + devPath
    config['word_idx'] = 1
    config['tasks'] = {}
    if crf:
        config['tasks']['slot'] = {'task_type': 'seq_bio', 'metric': 'span_f1', 'column_idx':3}
    else:
        config['tasks']['slot'] = {'task_type': 'seq', 'metric': 'acc', 'column_idx':3}
    config['tasks']['intent'] = {'task_type': 'classification', 'column_idx':-1}
    #for task in config['tasks']:
    #    config['tasks'][task]['loss_weight'] = 0.5
    return config

def getUDconfig(trainPath, devPath, prefix=''):
    config = {}
    config['train_data_path'] = '../' + trainPath
    config['validation_data_path'] = '../' + devPath
    config['word_idx'] = 1
    config['tasks'] = {}
    config['tasks'][prefix + 'upos'] = {'task_type': 'seq', 'column_idx':3}
    config['tasks'][prefix + 'lemma'] = {'task_type': 'string2string', 'column_idx':2}
    config['tasks'][prefix + 'feats'] = {'task_type': 'seq', 'column_idx':5}
    config['tasks'][prefix + 'dependency'] = {'task_type': 'dependency', 'column_idx':6}
    for task in config['tasks']:
        config['tasks'][task]['loss_weight'] = 0.25
    return config

def getUPOSconfig(trainPath, devPath, prefix=''):
    config = {}
    config['train_data_path'] = '../' + trainPath
    config['validation_data_path'] = '../' + devPath
    config['word_idx'] = 1
    config['tasks'] = {}
    config['tasks'][prefix + 'upos'] = {'task_type': 'seq', 'column_idx':3}
    for task in config['tasks']:
        config['tasks'][task]['loss_weight'] = 0.25
    return config

def getMLMconfig(trainPath, devPath):
    config = {}
    config['train_data_path'] = '../' + trainPath
    config['validation_data_path'] = '../' + devPath
    config['max_sents'] = 100000
    config['tasks'] = {}
    config['tasks']['mlm'] = {'task_type': 'mlm'}
    config['tasks']['mlm']['loss_weight'] = 0.01
    return config

def getNMTconfig(trainPath, devPath):
    config = {}
    config['train_data_path'] = '../' + trainPath
    config['validation_data_path'] = '../' + devPath
    config['column_idx'] = 0
    config['max_sents'] = 100000
    config['sent_idxs'] = [0]
    config['tasks'] = {}
    config['tasks']['nmt'] = {'task_type': 'seq2seq', 'column_idx': 1}
    config['tasks']['nmt']['loss_weight'] = 0.01
    return config

def getNLUtrain(dataset):
    datasetDir = 'data/' + dataset
    for conlFile in os.listdir(datasetDir):
        if 'conll' in conlFile and 'train' in conlFile and 'en' in conlFile.lower() and 'fixed' not in conlFile:
            return datasetDir + '/' + conlFile
    return ''

def getNLUdev(dataset, lang):
    datasetDir = 'data/' + dataset
    for conlFile in os.listdir(datasetDir):
        if 'conll' in conlFile and ('valid' in conlFile or 'dev' in conlFile or 'eval' in conlFile) and ('.' + lang.lower() + '.' in conlFile.lower() or '_' + lang.lower() + '.' in conlFile.lower() or conlFile.lower().startswith(lang.lower())):
            return datasetDir + '/' + conlFile
    return ''

def getNLUtest(dataset, lang):
    datasetDir = 'data/' + dataset
    for conlFile in os.listdir(datasetDir):
        if 'conll' in conlFile and 'test' in conlFile and ('.' + lang.lower() + '.' in conlFile.lower() or '_' + lang.lower() + '.' in conlFile.lower() or conlFile.lower().startswith(lang.lower())):
            return datasetDir + '/' + conlFile
    return ''

def getNLUscores(evalName):
    intents = []
    slots = []
    for seed in seeds:
        path = predDir +evalName + '.' + str(seed) + '.eval'
        if not os.path.isfile(path):
            slots.append(0.0)
            intents.append(0.0)
            continue
        intent = 0.0
        slot = 0.0
        for line in open(path):
            if line.startswith('slot'):
                slot = float(line.strip('\n').split(' ')[-1])
            if line.startswith('intents'):
                intent = float(line.strip('\n').split(' ')[-1])
        slots.append(slot)
        intents.append(intent)
    return [sum(slots)/len(slots), sum(intents)/len(intents), statistics.stdev(slots), statistics.stdev(intents), slots, intents]

