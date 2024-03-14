import myutils
import nluEval
import bootstrapSign
import os
from deepsig import aso


signScores = []
avgScores = []
for embeds in myutils.embeds:
    for model, name in zip(myutils.models, myutils.names):
        row = []
        signScores.append([])
        for dataset in myutils.datasets:
            intentScores = []
            slotScores = []
            signScores[-1].append([])
            signScores[-1].append([])

            for lang in myutils.data2langs[dataset]:
                lang = lang.lower()
                if lang == 'en':
                    continue
                name = embeds + '.' + dataset + '.'  + lang + '.' + model
                scores = myutils.getNLUscores(name)
    
                slotScores.append(scores[0])
                intentScores.append(scores[1])
                #if scores[0] == 0.0:
                #    print('WARNING slots ', name, '==0.0')
                #if scores[1] == 0.0:
                #    print('WARNING intents ', name, '==0.0')
                signScores[-1][-2].append(scores[4])
                signScores[-1][-1].append(scores[5])

            slotAvg = 100* sum(slotScores)/len(slotScores)
            intentAvg = 100* sum(intentScores)/len(intentScores)
            row.append(slotAvg)
            row.append(intentAvg)
        avgScores.append(row)


# shape: 10(rows) * 4 (columns) * 12 (models) * 5 (seeds)
print(len(signScores)) 
print(len(signScores[0]))
print(len(signScores[0][0]))
print(len(signScores[0][0][0]))
print()
#for rowIdx,row in enumerate(avgScores):
#    newRow = []
#    for columnIdx,column in enumerate(row):
#        newRow.append(str(column) + '$^1$')
#    print(' & '.join(newRow) + ' \\\\')
#exit(1)
significance = []
for rowIdx, row in enumerate(signScores):
    if rowIdx % 5 == 0:
        baseRow = row
        significance.append([0,0,0,0])
    else:
        significance.append([])
        for columnIdx, column in enumerate(row):
            eps_min = [aso(a, b, confidence_level=0.05) for a, b in zip(column, baseRow[columnIdx])]
            wins = [sum(model) > sum(base) for model, base in zip(column, baseRow[columnIdx])] 
            signs = sum([1 if (val < .5 and win) else 0 for val, win in zip(eps_min, wins)]) 
            significance[-1].append(signs)
            print(rowIdx, columnIdx)
            print(len(eps_min))
            print(wins)
            print(signs)

print(len(avgScores))
print(len(avgScores[0]))
print(avgScores[0])
print(len(significance))
print(len(significance[0]))
print(significance[0])
outFile = open('table.txt', 'w')
for rowIdx,row in enumerate(avgScores):
    newRow = []
    for columnIdx,column in enumerate(row):
        newRow.append('{:.2f}'.format(column) + '$^' + str(significance[rowIdx][columnIdx]) + '$')
    print(' & '.join(newRow) + ' \\\\')
    outFile.write(' & '.join(newRow) + ' \\\\ \n')
outFile.close()
