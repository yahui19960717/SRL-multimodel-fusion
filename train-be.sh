
CUDA_VISIBLE_DEVICES=2 python -m supar.cmds.vi_SRL train -b \
        --train data/BE-conll05/sc-conll5-train.conllu\
        --dev   data/BE-conll05/sc-conll5-dev.conllu\
        --test  data/BE-conll05/sc-conll5-wsj.conllu\
        --batch-size 3000 \
        --n-embed 100 \
        --feat lemma,char \
        --itp 0.06 \
        --embed data/glove.6B.300d.txt \
        --n_pretrained_embed 300\
        --min_freq 7 \
        --seed 1 \
        --schema BE \
        --unk "" \
        --train_given_prd \
        -p exp/BE-base-model-givenpred/model \
        -d 2