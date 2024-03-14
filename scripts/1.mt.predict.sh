# choose target language {ar, da, de, id, it, ja, kk, nl, sr, zh}, gpu id, beam and seed
target_lang=$1 
gpu=$2
beam=4
seed=1111

# setup files
FAIRSEQ_DIR=fairseq/fairseq_cli                # path to fairseq
MODEL_DIR=data/mt.models/$target_lang                  # path to trained NMT models 
BPE_DATA_DIR=data/mt.bpe_data/$target_lang             # path to BPE-d data 
PREPROCESSED_DIR=data/mt.preprocessed/$target_lang     # path to preprocessed files 
OUTPUT_DIR=$4 #../outputs/$target_lang                # save all outputs here


# You may change below variables
# E.g. below is for facebook's train-en.adapted.conll
INPUT_CONLL=$3 #../data/facebook/en/train-en.adapted.conll # choose file to preprocess and translate from
TEXT_OUTPUT_EN=$OUTPUT_DIR/text.en                     # save preprocessed text here
LABEL_OUTPUT_EN=$OUTPUT_DIR/label.en                   # save preprocessed labels here
BPE_OUTPUT_EN=$OUTPUT_DIR/text.bpe.en                  # save preprocessed BPE here
TRANSLATION_OUTPUT=$OUTPUT_DIR/text.best.$target_lang  # save translation output here


mkdir -p $OUTPUT_DIR

# preprocess conll file to text (`$TEXT_OUTPUT_EN`) and label outputs (`$LABEL_OUTPUT_EN`)
python3 -u scripts/preprocess_conll.py --input $INPUT_CONLL --text_output $TEXT_OUTPUT_EN --label_output $LABEL_OUTPUT_EN

# create BPE-d input text ($BPE_OUTPUT_EN)
subword-nmt apply-bpe -c $BPE_DATA_DIR/vocab.en.$target_lang.code < $TEXT_OUTPUT_EN > $BPE_OUTPUT_EN

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
     --print-alignment \
     < $BPE_OUTPUT_EN > $TRANSLATION_OUTPUT


# align translated text (`$TRANSLATION_OUTPUT`) with preprocessed labels from conll (`$LABEL_OUTPUT_EN`) using attention scores (`$TRANSLATION_OUTPUT`)
# it will create translated text (`$OUTPUT_DIR/sys_text.$target_lang`) and it's aligned labels (`$OUTPUT_DIR/sys_label.$target_lang`)
python3 -u scripts/align.py --source $TEXT_OUTPUT_EN --predict $TRANSLATION_OUTPUT --label $LABEL_OUTPUT_EN --bpe_source $BPE_OUTPUT_EN --target_lang $target_lang --output $OUTPUT_DIR
