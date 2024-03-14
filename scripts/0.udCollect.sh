wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3226/ud-treebanks-v2.6.tgz

tar -zxvf ud-treebanks-v2.6.tgz
mv ud-treebanks-v2.6 data/

python3 mtp/scripts/misc/cleanconl.py data/ud-treebanks-v2.6/*/*conllu


