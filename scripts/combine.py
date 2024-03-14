import sys

textFile = sys.argv[2] + '/sys_text.' + sys.argv[1]
enFile = sys.argv[2] + '/text.en'
labelFile = sys.argv[2] + '/sys_label.' + sys.argv[1]

for text, labels, text_en in zip(open(textFile), open(labelFile), open(enFile)):
    words = text.strip().split(' ')
    labels = labels.strip().split(' ')
    intent = labels[-1]
    labels = labels[:-1]

    print('# text: ' + text.strip())
    print('# text-en: ' + text_en.strip())
    print('# intent: ' + intent)
    for i in range(len(words)):
        print('\t'.join([str(i+1), words[i], intent, labels[i]]))
    print()

