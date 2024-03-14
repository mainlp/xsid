import myutils

for lang in myutils.getMtLangs:
    cmd = './scripts/1.mt.eval.sh ' + lang + ' 0'
    print(cmd)


