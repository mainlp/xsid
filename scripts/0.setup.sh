pip3 install --user -r requirements.txt

if [ ! -f mtp/train.py ]; then
    git clone https://github.com/machamp-nlp/machamp.git
    cd mtp
    git reset --hard 51ea716
    cd ..
fi

git clone https://github.com/pytorch/fairseq.git -b v0.9.0
cd fairseq
pip3 install --editable ./
cd ../
sed -i "s;div(;floor_divide(;g" fairseq/fairseq/search.py


