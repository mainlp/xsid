import myutils
import json
import os
from scipy.stats import pearsonr, spearmanr
import lang2vec.lang2vec as l2v
from scipy.spatial import distance
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('scripts/rob.mplstyle')

def getAttentScore(name):
    lang = name.split('.')[2]
    if lang == 'en':
        return 100.0
    path = 'data/xSID/mt.train.' + lang + '/eval'
    if not os.path.isfile(path):
        return 0.0
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
    
fig, ax = plt.subplots(figsize=(8,5), dpi=300)

rowAux = []
rowLang = []
for embed in myutils.embeds:
    for model, modelName in zip(myutils.models, myutils.names):
        avgScores = []
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
                avgScores.append((scores[0] + scores[1])/2)
                distances.append(langDists[lang])
        if model != 'base':
            pearsAvg, _ = pearsonr(avgScores, auxScores)
        else:
            pearsAvg = 0.0
        rowAux.append(abs(pearsAvg))

        pearsAvgDist, _ = pearsonr(avgScores, distances)
        rowLang.append(abs(pearsAvgDist))
x = np.arange(len(rowAux))
print(rowAux)
print(x-.8)
print()
print(rowLang)
print(x+.8)
width = .35
ax.bar(x - width/2, rowLang, width, label='Lang2vec')
ax.bar(x + width/2, rowAux, width, label='Auxiliary')

ax.set_xticks([-.5, .5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5])
ax.set_xticklabels(myutils.names * 2, rotation=45)
#ha = ['right', 'center', 'left']
ax.plot([4.5, 4.5], [0.0,1.0], color='black')
ax.set_ylim((0.0,1.0))
ax.set_xlim((-.5,9.5))
ax.text(1.5, -.25, 'mBERT')
ax.text(6.75, -.25, 'XLM15')

leg = ax.legend(loc='upper left')
leg.get_frame().set_linewidth(1.5)

fig.savefig('correlations.pdf', bbox_inches='tight')

