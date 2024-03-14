import sys

def fixBIO(sent):
    inSpan = False
    for lineIdx, line in enumerate(sent):
        bio = line[3][0]
        prevBio = 'O'
        if lineIdx > 0:
            prevBio = sent[lineIdx-1][3][0]
        if prevBio == 'O' and bio == 'I':
            words = sent[lineIdx]
            words[-1] = 'B' + words[-1][1:]
            sent[lineIdx] = words
    return sent

def readConll(path):
    allSents = []
    allComments = []
    curSent = []
    curComments = []
    for line in open(path):
        if line.strip() == '':
            allSents.append(fixBIO(curSent))
            allComments.append(curComments)
            curSent = []
            curComments = []
        else:
            if line[0] != '#':
                tok = line.strip().split('\t')
                if tok[-1] == 'NoLabel':
                    tok[-1] = 'O'
                curSent.append(tok)
            else:
                curComments.append(line.strip())
    return allSents, allComments

allSents, allComments = readConll(sys.argv[1])

for sent, comments in zip(allSents, allComments):
    inDomain = True
    for wordIdx, word in enumerate(sent):
        # annotate my/all in front of noun-tag
        if 'noun' in word[-1] or word[1] in ['alarm', 'alarms', 'reminder', 'reminders']:
            for i in reversed(range(max(0, wordIdx-3), wordIdx)):
                if sent[i][1] in ['my', 'all']:
                    sent[i][-1] = 'B-reference'
                    if sent[i+1][-1] == 'B-reference':
                        sent[i+1][-1] = 'I-reference'

        # remove noun-tags
        if 'noun' in word[-1]:
            sent[wordIdx][-1] = 'O'
        # fix weather specific tags
        if word[1] in ['temperature', 'high', 'low']:
            sent[wordIdx][-1] = 'B-weather/attribute'
            

        # replace noLabel with O
        if sent[wordIdx][-1] == 'NoLabel':
            sent[wordIdx][-1] = 'O'

        # remove `for' from datelabels
        if word[1] in ['for', 'on', 'at', 'to'] and word[-1] == 'B-datetime':
            sent[wordIdx][-1] = 'O'
            sent[wordIdx+1][-1] = 'B-datetime'

        if word[1] == 'the' and word[-1][0] == 'B':
            sent[wordIdx][-1] = 'O'
            sent[wordIdx+1][-1] = 'B' + sent[wordIdx+1][-1][1:]

        # rename labels: 
        #reminder/reference -> reference
        if 'reminder/reference' in word[-1]:
            sent[wordIdx][-1] = sent[wordIdx][-1][:2] + 'reference'
            sent[wordIdx][1] = 'test'
        #reminder/recurring_period -> recurring_datetime
        if 'reminder/recurring_period' in word[-1]:
            sent[wordIdx][-1] = sent[wordIdx][-1][:2] + 'recurring_datetime'

        if word[-1][1:] not in ['-datetime', '-location', '-recurring_datetime', '-reference', '-reminder/todo', '-weather/attribute', '']:
            inDomain = False

        # if datetime span contains every/daily -> recurring
        if word[1] in ['every', 'daily'] and word[-1][1:] == '-datetime':
            beg = wordIdx
            for i in reversed(range(0,beg)):
                if sent[i][-1][0] == 'B':
                    beg = i
                    break

            end = wordIdx
            for i in range(beg + 1, len(sent)):
                if sent[i][-1][0] != 'I':
                    break
            end = i +1 # bit hacky, also works when datetime is till the last word

            for i in range(beg, end):
                sent[i][-1] = sent[i][-1][:2] + 'recurring_datetime'
        

    #if inDomain == False:
    #    continue
    for com in comments:
        print(com)
    for word in sent:
        print('\t'.join(word))
    print()

