# install subword-nmt, numpy, torch
pip3 install subword-nmt

pip3 install numpy

pip3 install torch torchvision

# install fairseq
git clone https://github.com/pytorch/fairseq.git -b v0.9.0
cd fairseq
pip3 install --editable ./
pip3 install cython

pip3 install six

# for bert-tokenize
pip3 install tensorflow==1.14.0
