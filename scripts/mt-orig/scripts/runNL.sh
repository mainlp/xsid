CUDA_VISIBLE_DEVICES=1 python3 -u ../fairseq/fairseq_cli/train.py ../preprocessed/nl --save-dir ../models/nl --arch transformer_wmt_en_de --max-tokens 4096 --optimizer adam --lr 0.0005 -s en -t nl --dropout 0.3 --lr-scheduler inverse_sqrt --min-lr 1e-09 --warmup-updates 4000 --warmup-init-lr 1e-07 --adam-betas '(0.9, 0.98)' --criterion label_smoothed_cross_entropy --label-smoothing 0.1 --max-epoch 20 --log-format simple --seed 1111
