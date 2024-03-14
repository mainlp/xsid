import myutils
import json
import os
from scipy.stats import pearsonr, spearmanr
import lang2vec.lang2vec as l2v
from scipy.spatial import distance

def getAttentScore(name):
    lang = name.split('.')[2]
    if lang == 'en':
        return 100.0
    path = 'data/xSID/mt.train.' + lang + '/eval'
    if not os.path.isfile(path):
        scores.append(0.0)
    line = open('data/xSID/mt.train.' + lang + '/eval').readlines()[-1]
    return float(line.split(' ')[2].replace(',', ''))

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

def getLangDist(lang1, lang2):
    if len(lang1) != 2 or len(lang2) != 2:
        return 0.0
    lang1 = myutils.convLang[lang1]
    lang2 = myutils.convLang[lang2]
    vec1 = l2v.get_features(lang1, 'syntax_knn+phonology_knn+inventory_knn')[lang1]
    vec2 = l2v.get_features(lang2, 'syntax_knn+phonology_knn+inventory_knn')[lang2]
    return distance.cosine(vec1, vec2)


allLangs = set()
for dataset in myutils.datasets[:1]:
    for lang in myutils.data2langs[dataset]:
        allLangs.add(lang)
langDists = {}
for lang in allLangs:
    dist = getLangDist(lang, 'en')
    langDists[lang] = dist
    

print('model & slot & intent & slot & intent\\\\')
print(' & \\multicolumn{2}{c}{' + myutils.embeds[0] + '} & \\multicolumn{2}{c}{' + myutils.embeds[1] + '} \\\\')
for model, modelName in zip(myutils.models, myutils.names):
    row = []
    row2 = []
    for embed in myutils.embeds:
        slotScores = []
        intentScores = []
        auxScores = []
        distances = []
        for dataset in myutils.datasets[:1]:
            for lang in myutils.data2langs[dataset]:
                lang = lang.lower()
                if lang == 'en' or len(lang) != 2: # skip de-st here, because it messes up the language distance
                    continue
                name = '.'.join([embed, dataset, lang, model])
                scores = myutils.getNLUscores(name)
                if model != 'base':
                    auxScore = getAuxScore(model, name)
                    auxScores.append(auxScore)
                slotScores.append(scores[0])
                intentScores.append(scores[1])
                distances.append(langDists[lang])
        if model != 'base':
            pearsSlot, _ = pearsonr(slotScores, auxScores)
            pearsIntent, _ = pearsonr(intentScores, auxScores)
        else:
            pearsSlot = 0.0
            pearsIntent = 0.0
        row.append(pearsSlot)
        row.append(pearsIntent)

        pearsSlotDist, _ = pearsonr(slotScores, distances)
        pearsIntentDist, _ = pearsonr(intentScores, distances)
        row2.append(pearsSlotDist)
        row2.append(pearsIntentDist)
    if model == 'base':
        print(' & '.join([model, 'lang2vec'] + ['{:.2f}'.format(x) for x in row2]) + ' \\\\')
    else:
        metric = {'ud': 'average', 'nmt':'bleu', 'attent':'bleu', 'mlm':'perplexity'}[model]
        print(' & '.join([modelName, metric] + ['{:.2f}'.format(x) for x in row]) + ' \\\\')
        print(' & '.join(['', 'lang2vec'] + ['{:.2f}'.format(x) for x in row2]) + ' \\\\')



