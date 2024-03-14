import myutils

for lang in myutils.getMtLangs():
    cmd = './scripts/1.mt.prep.sh ' + lang
    print(cmd)


