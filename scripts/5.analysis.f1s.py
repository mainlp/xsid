import myutils
import os
import matplotlib.pyplot as plt

plt.style.use('scripts/rob.mplstyle')

def getF1scores(path):
    stricts = []
    looses = []
    unlabels = []
    for seed in myutils.seeds:
        path = path + '.' + seed + '.eval'
        if os.path.isfile(path):
            for line in open(path):
                if line.startswith('slot-f1'):
                    stricts.append(float(line.strip().split()[-1]))
                if line.startswith('ul_slot-f1'):
                    unlabels.append(float(line.strip().split()[-1]))
                if line.startswith('l_slot-f1'):
                    looses.append(float(line.strip().split()[-1]))
    print(path)
    print(stricts)
    print(unlabels)
    print(looses)
    return sum(stricts)/len(stricts), sum(unlabels)/len(unlabels), sum(looses)/len(looses)

fig, (ax1, ax2) = plt.subplots(2, 1, dpi=300)
for embedIdx, embed in enumerate(myutils.embeds):
    strict = []
    unlabel = []
    loose = []
    for model in myutils.models:
        strictF1s = []
        unlabelF1s = []
        looseF1s = []

        for lang in myutils.data2langs['xSID']:
            if lang == 'en':
                continue
            path = 'predictions/' + embed + '.xSID.' + lang + '.' + model 
            strictF1, unlabelF1, looseF1 = getF1scores(path)
            strictF1s.append(strictF1)
            unlabelF1s.append(unlabelF1)
            looseF1s.append(looseF1)
        # convert to averages
        strictAvg = sum(strictF1s)/len(strictF1s)
        unlabelAvg = sum(unlabelF1s)/len(unlabelF1s)
        looseAvg = sum(looseF1s)/len(looseF1s)
        strict.append(strictAvg)
        unlabel.append(unlabelAvg)
        loose.append(looseAvg)

    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    colors = colors + colors

    # plot
    x = range(len(strict))
    ax = ax1 if embedIdx == 0 else ax2
    ax.scatter(x, strict, s=175, marker='^', label='strict F1', color=colors[0])
    ax.scatter(x, unlabel, s=175, marker='o', label='unlabeled F1', color=colors[1])
    ax.scatter(x, loose, s=175, marker='+', label='loose F1', color= colors[3])
    ax.set_ylim((.2,.85))
    ax.set_xticks(x)
    convert = {'mbert':'mBERT', 'xlm15':'XLM15'}
    ax.set_title(convert[embed])

ax1.set_xticklabels([''] * len(x))
ax2.set_xticklabels(myutils.names)
leg = ax2.legend(bbox_to_anchor=(1, 1.7))
leg.get_frame().set_linewidth(1.5)

fig.savefig('f1s.pdf', bbox_inches='tight')

