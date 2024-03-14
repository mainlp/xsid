import myutils
import lang2vec.lang2vec as l2v
from scipy.spatial import distance

def table(embeds, taskNum, printDist=False, boldHighest=False):# 1 is intents, 0 is slots
    scores = {}
    allLangs = set()
    table = []
    for dataset in myutils.datasets[:1]:
        for lang in myutils.data2langs[dataset]:
            lang = lang.lower()
            allLangs.add(lang)
            for model in myutils.models:
                name = embeds + '.' + dataset + '.' + lang + '.' + model
                scores[name] = myutils.getNLUscores(name)[taskNum]

    distances = []
    for lang in sorted(allLangs):
        if lang in myutils.convLang:
            langCode = myutils.convLang[lang]
            enCode = myutils.convLang['en']
            langVec = l2v.get_features(langCode, 'syntax_knn+phonology_knn+inventory_knn')[langCode]
            engVec = l2v.get_features(enCode, 'syntax_knn+phonology_knn+inventory_knn')[enCode]
            if len(lang) == 2:
                distances.append((lang, distance.cosine(langVec, engVec)))

    distances.sort(key=lambda x: x[1])
    orderedLangs = [x[0] for x in distances]
    # hardcoded for now
    orderedLangs.insert(1,'de-st') 
    distances = [x[1] for x in distances]
    distances.insert(1,'---')
    distances[0] = '---'

    for dataset in myutils.datasets[:1]:
        rows = []
        for model, name in zip(myutils.models, myutils.names):
            row = [dataset + '.' + name]
            row = [name]
            total = 0.0
            numScores = 0
            for lang in orderedLangs:
                name = embeds + '.' + dataset + '.' + lang + '.' + model
                if name in scores:
                    row.append(scores[name] * 100)
                    if lang != 'en':
                        numScores +=1
                        total += scores[name] * 100
                else:
                    row.append('-')
            if numScores == 0:
                row.append(0.0)
            else:
                row.append(total/numScores)
            rows.append(row)
        for i in range(1,len(rows[0])):
            highest = 0.0
            for j in range(len(rows)):
                if rows[j][i] == '-':
                    continue
                if rows[j][i] > highest:
                    highest = rows[j][i]
            for j in range(len(rows)):
                if rows[j][i] == '-':
                    continue
                elif rows[j][i] == highest and boldHighest:
                    rows[j][i] = '\\textbf{' + '{:.1f}'.format(rows[j][i]) + '}'
                else:
                    rows[j][i] = '{:.1f}'.format(rows[j][i])
        for row in rows:
            table.append(row)#print(' & '.join(row) + '\\\\')
    if taskNum == 0:
        if embeds == 'xlm15':
            langs = [('\\textbf{' + lang + '}') if lang in myutils.xlmLangs else lang for lang in orderedLangs]
        else: 
            langs = ['\\textbf{' + lang + '}' for lang in orderedLangs]
        print(' & '.join([embeds] + langs) + ' \\\\')
    if printDist:
        print(' & '.join(['lang2vec'] + ['{:.2f}'.format(x) if type(x) != str else x for x in distances]) + ' \\\\')
        print('\\midrule')
    if taskNum in [0,2]:
        print('Slots' + '\\\\')
    elif taskNum in [1,3]:
        print('Intents' + '\\\\')
    print('\\midrule')
    
    for row in table:
        print(' & '.join(row) + ' \\\\')

# the average scores:
print('\\toprule')
table('mbert', 0, True, True)
print('\\midrule')
table('mbert', 1, False, True)
print('\\bottomrule')
table('xlm15', 0, False, True)
print('\\midrule')
table('xlm15', 1, False, True)
print('\\bottomrule')

print('\n\n')
# stdevs:
print('\\toprule')
table('mbert', 2, True, False)
print('\\midrule')
table('mbert', 3, False, False)
print('\\bottomrule')
table('xlm15', 2, False, False)
print('\\midrule')
table('xlm15', 3, False, False)
print('\\bottomrule')

