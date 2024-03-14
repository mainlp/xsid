# choose target language {ar, da, de, id, it, ja, kk, nl, sr, zh}, gpu id, beam and seed
target_lang=$1 
gpu=$2
beam=4
seed=1111

# setup files
FAIRSEQ_DIR=./fairseq/fairseq_cli                # path to fairseq
MODEL_DIR=./data/mt.models/$target_lang                  # path to trained NMT models 
BPE_DATA_DIR=./data/mt.bpe_data/$target_lang             # path to BPE-d data 
PREPROCESSED_DIR=./data/mt.preprocessed/$target_lang     # path to preprocessed files 
OUTPUT_DIR=./data/xSID/mt.train.$target_lang                # save all outputs here


# You may change below variables
# E.g. below is for facebook's train-en.adapted.conll
#INPUT_DEV=../nlu-data/facebook/en/valid-en.txt # choose file to preprocess and translate from
#TARGET_DEV=../nlu-data/facebook/$target_lang/0.valid-"$target_lang".txt # choose the reference file
INPUT_DEV=./data/mt.tok/en-$target_lang/dev.en # choose file to preprocess and translate from
TARGET_DEV=./data/mt.tok/en-$target_lang/dev.$target_lang  # choose the reference file
BPE_OUTPUT_EN=$OUTPUT_DIR/dev_text.bpe.en                  # save preprocessed BPE here
TRANSLATION_OUTPUT=$OUTPUT_DIR/dev_text.best.$target_lang  # save translation output here


mkdir -p $OUTPUT_DIR

# create BPE-d input text ($BPE_OUTPUT_EN)
subword-nmt apply-bpe -c $BPE_DATA_DIR/vocab.en.$target_lang.code < $INPUT_DEV > $BPE_OUTPUT_EN

# translate
CUDA_VISIBLE_DEVICES=$gpu python3 -u $FAIRSEQ_DIR/interactive.py $PREPROCESSED_DIR \
     --path ${MODEL_DIR}/checkpoint_best.pt \
     --beam ${beam} \
     --seed $seed \
     -s en \
     --no-progress-bar \
     --buffer-size 1024 \
     --batch-size 32 \
     --log-format simple \
     --remove-bpe \
     < $BPE_OUTPUT_EN > $TRANSLATION_OUTPUT

# post-processing
cat $TRANSLATION_OUTPUT | grep "^H" | cut -f3 > $OUTPUT_DIR/dev.best.tok

# calculate BLEU score, which considers ngrams up to 4 (default) order
python3 $FAIRSEQ_DIR/score.py -s $OUTPUT_DIR/dev.best.tok -r $TARGET_DEV > $OUTPUT_DIR/eval
