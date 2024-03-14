import myutils
import os
import json

for model, modelName in zip(myutils.models, myutils.names):
    allTimes = []
    for embed in myutils.embeds:
        for dataset in myutils.datasets:
            for lang in myutils.data2langs[dataset]:
                lang = lang.lower()
                if lang in ['en', 'de-st']:
                    continue
                for seed in myutils.seeds:
                    name = '.'.join([embed, dataset, lang, model, seed])
                    if model == 'base':
                        name = '.'.join([embed, dataset, model, seed])
                    metricsFile = 'mtp/' + myutils.getModel(name).replace('model.tar.gz', 'metrics.json')
                    if not os.path.isfile(metricsFile):
                        print("ERROR", metricsFile, name)
                        continue
                    metricsData = json.load(open(metricsFile))
                    duration = metricsData['training_duration'].split('.')[0].split(':')
                    if len(duration) != 3:
                        print("ERROR", duration)
                        continue
                    if 'day' in duration[0]:
                        seconds = int(duration[2]) + 60 * int(duration[1]) + 60 * 60 * int(duration[0].split(' ')[-1])
                        seconds +=  int(duration[0].split(' ')[0]) * 24 * 60 * 60
                    else:
                        seconds = int(duration[2]) + 60 * int(duration[1]) + 60 * 60 * int(duration[0])
                    
                    if model == 'attent':
                        # average time for NMT
                        seconds += 5103*60
                    allTimes.append(seconds)
    if model == 'base':
        numLangs = []
        for dataset in myutils.datasets:
            numLangs.append(len(myutils.data2langs[dataset]))
        avgLangs = sum(numLangs)/len(numLangs)
        print(modelName, int((sum(allTimes)/len(allTimes)/60)/avgLangs))
    else:
        print(modelName, int(sum(allTimes)/len(allTimes)/60))

    
