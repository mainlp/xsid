# choose target language {ar, da, de, id, it, ja, kk, nl, sr, zh}, gpu id, vocab_size and seed
target_lang=$1
gpu=$2
seed=1111
vocab_size=32000

# setup files
FAIRSEQ_DIR=fairseq/fairseq_cli              # path to fairseq
DATA_DIR=data/mt.tok/en-$target_lang        # path to bilingual data
BPE_DATA_DIR=data/mt.bpe_data/$target_lang           # save BPE-d outputs here
PREPROCESSED_DIR=data/mt.preprocessed/$target_lang   # save preprocessed files here
MODEL_DIR=data/mt.models/$target_lang                # save trained NMT models here

cpu_num=`grep -c ^processor /proc/cpuinfo`

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
    --adam-betas '"(0.9, 0.98)"' \
    --criterion label_smoothed_cross_entropy \
    --label-smoothing 0.1 \
    --max-epoch 20 \
    --log-format simple \
    --seed $seed
