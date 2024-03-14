# choose target language {ar, da, de, id, it, ja, kk, nl, sr, zh}, gpu id, vocab_size and seed
target_lang=$1
seed=1111
vocab_size=32000

# setup files
FAIRSEQ_DIR=fairseq/fairseq_cli              # path to fairseq
DATA_DIR=data/mt.tok/en-$target_lang        # path to bilingual data
BPE_DATA_DIR=data/mt.bpe_data/$target_lang           # save BPE-d outputs here
PREPROCESSED_DIR=data/mt.preprocessed/$target_lang   # save preprocessed files here
MODEL_DIR=data/mt.models/$target_lang                # save trained NMT models here

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

python3 $FAIRSEQ_DIR/preprocess.py --source-lang en --target-lang $target_lang \
        --trainpref $BPE_DATA_DIR/train.bpe \
        --validpref $BPE_DATA_DIR/dev.bpe \
        --destdir $PREPROCESSED_DIR \
        --workers $cpu_num \
        --joined-dictionary \
        --nwordssrc $vocab_size \
        --nwordstgt $vocab_size \
        --seed $seed

