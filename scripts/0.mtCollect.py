# TODO there is way too much redundancy here

import sys
import os
import bert_tokenize
import myutils

def cmd(cmd):
    print(cmd)
    os.system(cmd)

def tok(path):
    tknzr = bert_tokenize.BasicTokenizer()
    tmpFile = open(path + '.tok', 'w')
    for line in open(path):
        tmpFile.write(' '.join(tknzr.tokenize(line.strip('\n'))) + '\n')
    tmpFile.close()
    cmd('mv ' + path + '.tok ' + path)

def getLang(lang):
    # collect ted
    if not os.path.isdir('multitarget-ted'):
        if not os.path.isfile('multitarget-ted.tgz'):
            cmd('wget http://www.cs.jhu.edu/~kevinduh/a/multitarget-tedtalks/multitarget-ted.tgz')
        cmd('tar -zxvf multitarget-ted.tgz')
    
    # collect opensubtitles
    langPair = 'en-' + lang
    if lang < 'en':
        langPair = lang + '-en'
    OSzipFile = 'download.php?f=OpenSubtitles%2Fv2018%2Fmoses%2F' + langPair + '.txt.zip'
    if not os.path.isfile(OSzipFile):
        cmd('wget http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/moses/' + langPair + '.txt.zip')
    OSfile = 'OpenSubtitles.' + langPair + '.' + lang
    if not os.path.isfile(OSfile):
        cmd('unzip -o ' + OSzipFile)
    
    # collect Tatoeba
    TATzipFile = 'download.php?f=Tatoeba%2Fv20190709%2Fmoses%2F' + langPair + '.txt.zip'
    if not os.path.isfile(TATzipFile):
        cmd('wget http://opus.nlpl.eu/download.php?f=Tatoeba/v20190709/moses/' + langPair + '.txt.zip')
    TATfile = 'Tatoeba.' + langPair + '.' + lang
    if not os.path.isfile(TATfile):
        cmd('unzip ' + TATzipFile)
    
    tedFolder = 'multitarget-ted/en-' + lang + '/'
    if not os.path.isdir('data/mt.tok/en-' + lang):
        os.mkdir('data/mt.tok/en-' + lang)

    if os.path.isdir(tedFolder):
        # combine training data
        cmdEn = 'cat '
        cmdTgt = 'cat '
        cmdEn += tedFolder + 'raw/ted_train_en-' + lang + '.raw.en'
        cmdTgt += tedFolder + 'raw/ted_train_en-' + lang + '.raw.' + lang
        cmdEn += ' OpenSubtitles.' + langPair + '.en'
        cmdTgt += ' OpenSubtitles.' + langPair + '.' + lang
    
        cmdEn += ' > data/mt.tok/en-' + lang + '/train.en'
        cmdTgt += ' > data/mt.tok/en-' + lang + '/train.' + lang
        cmd(cmdEn)
        cmd(cmdTgt)
    
        tok('data/mt.tok/en-' + lang + '/train.en')
        tok('data/mt.tok/en-' + lang + '/train.' + lang)
        cmdPaste = 'paste data/mt.tok/en-' + lang + '/train.en data/mt.tok/en-' + lang + '/train.' + lang + ' | grep -v "	$" | grep -v "^	" > data/mt.tok/en-' + lang + '/train.en' + lang
        cmd(cmdPaste)

        # get dev data
        cmdDevEn = 'cp ' + tedFolder + 'raw/ted_dev_en-' + lang + '.raw.en data/mt.tok/en-' + lang + '/dev.en'
        cmdDevTgt = 'cp ' + tedFolder + 'raw/ted_dev_en-' + lang + '.raw.' + lang + ' data/mt.tok/en-' + lang + '/dev.' + lang
        cmd(cmdDevEn)
        cmd(cmdDevTgt)
        tok('data/mt.tok/en-' + lang + '/dev.en')
        tok('data/mt.tok/en-' + lang + '/dev.' + lang)
        cmdPaste = 'paste data/mt.tok/en-' + lang + '/dev.en data/mt.tok/en-' + lang + '/dev.' + lang + ' | grep -v "	$" | grep -v "^	" > data/mt.tok/en-' + lang + '/dev.en' + lang
        cmd(cmdPaste)

    else:
        #train
        cmdEn = 'cp OpenSubtitles.' + langPair + '.en data/mt.tok/en-' + lang + '/train.en'
        cmdTgt = 'cp OpenSubtitles.' + langPair + '.' + lang + ' data/mt.tok/en-' + lang + '/train.' + lang
        cmd(cmdEn)
        cmd(cmdTgt)
        tok('data/mt.tok/en-' + lang + '/train.en')
        tok('data/mt.tok/en-' + lang + '/train.' + lang)
        cmdPaste = 'paste data/mt.tok/en-' + lang + '/train.en data/mt.tok/en-' + lang + '/train.' + lang + ' | grep -v "	$" | grep -v "^	" > data/mt.tok/en-' + lang + '/train.en' + lang
        cmd(cmdPaste)
    
        #dev
        cmdEn = 'cp Tatoeba.' + langPair + '.en data/mt.tok/en-' + lang + '/dev.en'
        cmdTgt = 'cp Tatoeba.' + langPair + '.' + lang + ' data/mt.tok/en-' + lang + '/dev.' + lang
        cmd(cmdEn)
        cmd(cmdTgt)
        tok('data/mt.tok/en-' + lang + '/dev.en')
        tok('data/mt.tok/en-' + lang + '/dev.' + lang)
        cmdPaste = 'paste data/mt.tok/en-' + lang + '/dev.en data/mt.tok/en-' + lang + '/dev.' + lang + ' | grep -v "	$" | grep -v "^	" > data/mt.tok/en-' + lang + '/dev.en' + lang
        cmd(cmdPaste)

if not os.path.isdir('data'):
    os.mkdir('data')
if not os.path.isdir('data/mt.tok'):
    os.mkdir('data/mt.tok')

for lang in myutils.getMtLangs():
    getLang(lang)
#TODO cleanup?

