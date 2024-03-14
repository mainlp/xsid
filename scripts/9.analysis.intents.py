import myutils
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


def conll2intents(path):
    data = []
    for line in open(path):
        if line.startswith('# intent: '):
            data.append(line.strip().split(' ')[-1])
    return data

def getMatrix(embeds, model, subLangs):
    goldData = []
    predData = []
    numLangs = 0
    for lang in myutils.datasets['xSID']:
        if subLangs and lang in myutils.xlmLangs:
            continue
        numLangs += 1
        goldPath = 'data/xSID/' + lang + '.valid.conll'
        predPath = 'predictions/' + embeds[0] + '.xSID.' + lang + '.' + model
        goldData.extend(conll2intents(goldPath))
        predData.extend(conll2intents(predPath))
    allLabels = list(sorted(set(goldData)))
    print(allLabels)
    for label in ['alarm/time_left_on_alarm', 'RateBook']:
        if label in allLabels:
            allLabels.remove(label)
    matches = []
    for i in range(len(allLabels)):
        matches.append(len(allLabels) * [0])
    for goldLabel, predLabel in zip(goldData, predData):
        if goldLabel not in allLabels:
            continue
        goldIdx = allLabels.index(goldLabel)
        if predLabel in allLabels:
            predIdx = allLabels.index(predLabel)
            # R: now it skips correct ones
            #if predIdx != goldIdx:
            matches[goldIdx][predIdx]-=1

    # hardcoded redundantly now so that it eaily matches the allLabels
    goldData = []
    predData = []
    for lang in myutils.datasets['xSID']:
        if subLangs and lang in myutils.xlmLangs:
            continue
        goldPath = 'data/xSID/' + lang + '.valid.conll'
        predPath = 'predictions/' + embeds[1] + '.xSID.' + lang + '.' + model
        goldData.extend(conll2intents(goldPath))
        predData.extend(conll2intents(predPath))
    for goldLabel, predLabel in zip(goldData, predData):
        if goldLabel not in allLabels:
            continue
        goldIdx = allLabels.index(goldLabel)
        if predLabel in allLabels:
            predIdx = allLabels.index(predLabel)
            #if predIdx != goldIdx:
            matches[goldIdx][predIdx]+=1
    

    print(embeds, model)
    for name, row in zip(allLabels, matches):
        print(name, row)
    print()
    fig, ax = plt.subplots(figsize=(8,5), dpi=300)
    im = ax.imshow(matches)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
    fig.colorbar(im);
    ax.text(15.5,-.5,embeds[1])
    ax.text(15.5,14,embeds[0])

    ax.set_xticks(range(len(allLabels)))
    ax.set_yticks(range(len(allLabels)))
    ax.set_ylabel('Predicted')
    ax.set_xlabel('Gold')
    ax.set_xticklabels([x.split('/')[-1] for x in allLabels])
    ax.set_yticklabels([x.split('/')[-1] for x in allLabels])



    fig.savefig('intents.' + str(numLangs) + '.pdf', bbox_inches='tight')
    


getMatrix(['mbert', 'xlm15'], 'base', False)
getMatrix(['mbert', 'xlm15'], 'base', True)
