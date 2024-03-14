import myutils
import lang2vec.lang2vec as l2v
from scipy.spatial import distance
import matplotlib.pyplot as plt
import numpy as np

def table(embeds, taskNum, printDist=False):# 1 is intents, 0 is slots
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
                elif rows[j][i] == highest:
                    rows[j][i] = rows[j][i]
                else:
                    rows[j][i] = rows[j][i]
        for row in rows:
            table.append(row)#print(' & '.join(row) + '\\\\')
    return distances, table, orderedLangs

merge = False
smooth = False
linear = True
if not linear:
    merge=True

for embed in myutils.embeds:
    distances, mbertSlots, langs = table(embed, 0, True)
    #_, mbertIntents = table('mbert', 1, False)
    plt.style.use('scripts/rob.mplstyle')
    fig, ax = plt.subplots(figsize=(8,5), dpi=300)
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    colors = colors + colors
    markers = ["P", "o", "D"]
    markers = markers+markers
    langs = langs[2:]
    
    if merge:
        distances = [round(x,2) for x in distances[2:]]
    else:
        distances = [x for x in distances[2:]]
    for modelIdx in range(2,len(mbertSlots)):
        slots = []
        for modelSlot, baseSlot in zip(mbertSlots[modelIdx][3:-1], mbertSlots[0][3:-1]):
            slots.append(modelSlot-baseSlot)
    
        if merge:
            slots = [(slots[0] + slots[1] / 2)] + slots[2:]
            distanceUse = distances[1:]
        else:
            distanceUse = distances
    
        if not linear:
            distanceUse = [str(round(x, 2)) for x in distanceUse]
        else:
            ax.plot([.17,.43], [0,0], color='gray', zorder=1, alpha=.3)
        distanceUse[5] += .001

        if smooth:
            x = distanceUse
            y = slots
            #from scipy.interpolate import interp1d
            #f = interp1d(x, y, kind='cubic')
            #xnew = np.arange(min(x), max(x), 0.001)
            #ynew = f(xnew)   
    
            from scipy.interpolate import splev, splrep
            xnew = np.linspace(min(x), max(x), 3000) 
            spl = splrep(x, y, s=.5, k=.3, w=[.5] * len(x))
            ynew = splev(xnew, spl)
    
            #from scipy.interpolate import make_interp_spline, BSpline
            #xnew = np.linspace(min(x), max(x), 30000) 
            #spl = make_interp_spline(x, y, k=2)
            #ynew = spl(xnew)
            ax.plot(xnew, ynew, linestyle='dashed', color=colors[modelIdx], alpha=.3, zorder=2)
        else:
            ax.plot(distanceUse, slots, linestyle='dashed', color=colors[modelIdx], alpha=.3, zorder=2)
        ax.scatter(distanceUse, slots, s=175, label=myutils.names[modelIdx], color=colors[modelIdx], marker=markers[modelIdx], zorder=2)
        #print(distances, len(distances))
        #print(slots, len(slots))
    
    #ax.set_xticklabels([''] * len(x))
    ax.set_xticks(distanceUse)
    ax.set_xticklabels([''] + langs[1:], rotation=315)
    ax.text(.173, -21, langs[0], rotation=315)
    ax.set_ylabel('Difference in F1 to base')
    ax.set_xlabel('Language distance (lang2vec)')
    ax.set_ylim((-15,25))
    if linear:
        ax.set_xlim((.17, .43))
    leg = ax.legend()#loc = 'upper right')
    leg.get_frame().set_linewidth(1.5)
    
    fig.savefig(embed + '.slots.pdf', bbox_inches='tight')
    
