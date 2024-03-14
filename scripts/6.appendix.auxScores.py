import myutils
import json
import os
from scipy.stats import pearsonr, spearmanr

def getAttentScore(name):
    lang = name.split('.')[2]
    if lang == 'en':
        return 0.0
    path = 'data/xSID/mt.train.' + lang + '/eval'
    if not os.path.isfile(path):
        return 0.0
    line = open('data/xSID/mt.train.' + lang + '/eval').readlines()[-1]
    return float(line.split(' ')[2].replace(',', ''))/100

def getAuxScore(model, name):
    if model == 'base' or (lang == 'en' and model in ['attent', 'nmt']):
        return 0.0
    if model == 'attent':
        return getAttentScore(name)
    scores = []
    for seed in myutils.seeds:
        metricsFile = 'mtp/' + myutils.getModel(name + '.' + seed).replace('model.tar.gz', 'metrics.json')
        if not os.path.isfile(metricsFile):
            return 0.0
        metricsData = json.load(open(metricsFile))

        for infoPiece in metricsData:
            if infoPiece.startswith('best_validation_.run/') and infoPiece != 'best_validation_.run/.sum':
                if 'intent' not in infoPiece and 'slot' not in infoPiece:
                    scores.append(metricsData[infoPiece])
    return sum(scores)/len(scores)

for embed in myutils.embeds:
    print(embed + ' \\\\')
    for dataset in myutils.datasets[:1]:
        for lang in sorted(myutils.data2langs[dataset]):
            if len(lang) != 2:
                continue
            lang = lang.lower()
            langScores = []
            for model in ['ud', 'mlm', 'nmt', 'attent']:
                name = '.'.join([embed, dataset, lang, model])
                score = getAuxScore(model, name)
                langScores.append(score)
                if langScores[-1] > 1.0:
                    langScores[-1] /=100
            print(' & '.join([lang] + ['{:.2f}'.format(x*100) for x in langScores]) + ' \\\\')
                


