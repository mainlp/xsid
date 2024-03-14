# choose target language {ar, da, de, id, it, ja, kk, nl, sr, zh}, gpu id, vocab_size and seed
target_lang=$1
gpu=$2
seed=1111
vocab_size=32000

# setup files
FAIRSEQ_DIR=../fairseq/fairseq_cli              # path to fairseq
DATA_DIR=../nlu-data/tok/en-$target_lang        # path to bilingual data
BPE_DATA_DIR=../bpe_data/$target_lang           # save BPE-d outputs here
PREPROCESSED_DIR=../preprocessed/$target_lang   # save preprocessed files here
MODEL_DIR=../models/$target_lang                # save trained NMT models here

cpu_num=`grep -c ^processor /proc/cpuinfo`

if [ -e $PREPROCESSED_DIR ]; then
    echo Preprocessed files already exist
else
    mkdir -p $PREPROCESSED_DIR
    mkdir -p $BPE_DATA_DIR

    # create BPE-d outputs (train and dev) from concatenating train files of English and target languages
    cat $DATA_DIR/train.en $DATA_DIR/train.$target_lang > $BPE_DATA_DIR/en.$target_lang.txt
    subword-nmt learn-bpe -s $vocab_size < $BPE_DATA_DIR/en.$target_lang.txt > $BPE_DATA_DIR/vocab.en.$target_lang.code
    subword-nmt apply-bpe -c $BPE_DATA_DIR/vocab.en.$target_lang.code < $DATA_DIR/train.en > $BPE_DATA_DIR/train.bpe.en
    subword-nmt apply-bpe -c $BPE_DATA_DIR/vocab.en.$target_lang.code < $DATA_DIR/train.$target_lang > $BPE_DATA_DIR/train.bpe.$target_lang
    subword-nmt apply-bpe -c $BPE_DATA_DIR/vocab.en.$target_lang.code < $DATA_DIR/dev.en > $BPE_DATA_DIR/dev.bpe.en
    subword-nmt apply-bpe -c $BPE_DATA_DIR/vocab.en.$target_lang.code < $DATA_DIR/dev.$target_lang > $BPE_DATA_DIR/dev.bpe.$target_lang

    # preprocess the data
    python3 $FAIRSEQ_DIR/preprocess.py --source-lang en --target-lang $target_lang \
        --trainpref $BPE_DATA_DIR/train.bpe \
        --validpref $BPE_DATA_DIR/dev.bpe \
        --destdir $PREPROCESSED_DIR \
        --workers $cpu_num \
        --joined-dictionary \
        --nwordssrc $vocab_size \
        --nwordstgt $vocab_size \
        --seed $seed
fi

# train an NMT model
echo CUDA_VISIBLE_DEVICES=$gpu python3 -u $FAIRSEQ_DIR/train.py $PREPROCESSED_DIR \
    --save-dir $MODEL_DIR \
    --arch transformer_wmt_en_de \
    --max-tokens 4096 \
    --optimizer adam \
   --lr 0.0005 \
    -s en \
    -t $target_lang \
    --dropout 0.3 \
    --lr-scheduler inverse_sqrt \
    --min-lr '1e-09' \
    --warmup-updates 4000 \
    --warmup-init-lr '1e-07' \
    --adam-betas '(0.9, 0.98)' \
    --criterion label_smoothed_cross_entropy \
    --label-smoothing 0.1 \
    --max-epoch 20 \
    --log-format simple \
    --seed $seed
